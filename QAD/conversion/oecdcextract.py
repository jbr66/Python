'''
OpenEdge CDC Extractor for QAD to MariaDB
Project Inspiration

Written by Derek Bradley
Copyright QAD 2023

Requires Python3.6+ 
 
sequences stored in cdc_det

cdc_table = "tablename"
cdc_sequence = "sequence"
cdc_watermark = for callback only, stores downstream sequence high value processed
LastModifiedDateTime = datetime of update

Cannot handle tables that are too long in name ( more than 29 characters ) 
see cfg['exclude_tables']

Usage notes :   python3.7 oecdcextract.py --cfg /path/to/[yamlconfigfile].yaml --overrides

any entry in the YAML file can be overriden at runtime. 
Examples :

 python3.7 ./oecdcextract.py --cfg ./oemdbetl.yaml --loglevel INFO --send_topic cdc_test ==sql_pass S1xp0int@1

Requires that CDC is set up and enabled in the source openedge database.  The "cdc_owner" in the YAML config is the schema
the CDC is loaded into.

Requires that Kafka is up and running and listening on "send_topic"

This application monitors the source openedge database for changes and sends fully formed MariaDB DML statements to the Kafka topic

A separate downstream process will sink the data into a holding database such as Cassandra, or directly play the statements into the 
destination MariaDB database ( or whatever ... this program is really only concerned with getting the tracked changes onto the Kafka topic )

**** DOES NOT SUPPORT CLOBS **** 
Tables that are in cfg['cdc_clob_tables'] are currently excluded and should be ETL'd manually
**** DOES NOT SUPPORT CLOBS **** 

'''


import sys
import qadoemdbetl
import os
import yaml
import argparse
import socket
import logging
import time
import resource
import signal
from datetime import datetime
from decimal import Decimal
# pip3.7 install confluent_kafka
from confluent_kafka import Consumer, KafkaError, Producer

hostname = socket.gethostname()
process_functions = []

def _get_config(cfgfile):
   try :
      with open (cfgfile, 'r') as f :
         cfg = yaml.safe_load(f)
         return cfg
   except FileNotFoundError:
      print ('Cannot load YAML config file %s' % cfgfile)
   except yaml.YAMLError as e:
      print ('Error parsing YAML config file %s' % cfgfile,e)
   sys.exit(2)


def add_arguments(parser,cfg) :
    parser.add_argument('--cfg')
    for arg in cfg.keys() :
       if 'pass' in arg :
          print ('Adding Argument %s with HIDDEN value' % ( arg))
       else :    
          print ('Adding Argument %s with default value: %s ' % ( arg, cfg[arg]))
       parser.add_argument('--%s' % arg)
    return parser

def process_overrides(args,cfg) :

   for key,value in vars(args).items():
       if key == 'cfg' :
           continue
       if value == None :
           continue
       print ('Overriding %s setting to %s' % (key,value))
       cfg[key] = value
   return cfg

def elapsed_time(start_time) :
   elapsed_time = time.time() - start_time
   logger.debug (f"Loop Elapsed time: {elapsed_time} seconds")
   return
   
def signal_term_handler(signal, frame):

    usage = resource.getrusage(resource.RUSAGE_SELF)
    for name, desc in [
             ('ru_utime', 'User time'),
             ('ru_stime', 'System time'),
             ('ru_maxrss', 'Max. Resident Set Size'),
             ('ru_ixrss', 'Shared Memory Size'),
             ('ru_idrss', 'Unshared Memory Size'),
             ('ru_isrss', 'Stack Size'),
             ('ru_inblock', 'Block inputs'),
             ('ru_oublock', 'Block outputs'),
             ]:
               logging.error('%-25s (%-10s) = %s' % (desc, name, getattr(usage, name)))
    logging.error ('got signal %s , quitting' % signal)
    sys.exit(0)
    return False
   
 
if __name__ == '__main__' :

   '''
   requires AT LEAST the --cfg argument pointing to the YAML control file
   '''

   if len(sys.argv) < 3 :
       print ('Usage :  oecdcextract.py --cfg cfgfile [--arg value --arg value]')
       print ('Missing cfgfile.  Exiting')
       sys.exit(2)

   if not sys.argv[1] == '--cfg' :
       print ('%s not recognized' % (sys.argv[1]))
       print ('Usage :  oecdcextract.py --cfg cfgfile [--arg value --arg value]')
       sys.exit(2)

   start_time = time.time()

   cfgfile = sys.argv[2]
   cfg = _get_config(cfgfile)
   
   '''
   read in optional arguments and at runtime override the values stored in the YAML control file
   '''

   parser = argparse.ArgumentParser()
   parser = add_arguments(parser,cfg)

   try :
      args = parser.parse_args()
   except SystemExit:
      sys.exit(2)

   cfg = process_overrides(args,cfg)

   conn = False

   print ('*** Beginning CDC Poller ***')
   print ('Refer to %s for the CDC logs' % (cfg['cdc_log']))

   # Setup logging
   logger = logging.getLogger(__name__)
   formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

   print (cfg['loglevel'])
   if cfg['loglevel'] == 'ERROR' :
      error_handler = logging.FileHandler(cfg['cdc_log'])
      error_handler.setLevel(logging.ERROR)
      logger.setLevel(logging.ERROR)
      error_handler.setFormatter(formatter)
      logger.addHandler(error_handler)
   else :
      logger.setLevel(logging.INFO)

      info_handler = logging.FileHandler(cfg['cdc_log'])
      info_handler.setFormatter(formatter)
      logger.addHandler(info_handler)

   if cfg['loglevel'] == 'DEBUG' :
      logger.setLevel(logging.DEBUG)

   '''
   verify the logger is working
   '''
   
   logger.debug('Debug message Example')
   logger.info('Info message Example')
   logger.warning('Warning message Example')
   logger.error('Error message Example')
   logger.critical('Critical message Example')
   
   logger.info('Setting up base dictionaries')
   tables = {}
   # sequence number
   seq = {}
   # CDC keys
   keys = {}
   # extents
   extentdict = {}
   # mandatory fields
   # if key [tablename] == fieldname then field is mandatory.  If dictionary key fails to resolve, then not mandatory
   mandatorydict = {}

   # simply a session counter to ensure we don't have duplicates based on two messages on the same microsecond.  It could happen on fast processors.
   globalseq = 0

   logger.info('Setting up signal overrides')
   signal.signal(signal.SIGTERM, signal_term_handler)
   signal.signal(signal.SIGINT, signal_term_handler)
   signal.signal(signal.SIGSEGV, signal_term_handler)
   signal.signal(signal.SIGHUP, signal_term_handler)
   signal.signal(signal.SIGQUIT, signal_term_handler)   
   
   # connect to openedge and get the SQL cursor
   logger.info('Attempting to connect to source openedge')
   conn = qadoemdbetl.conn_oesql(cfg,logger)
   if conn == False :
      logger.error('Failed to connect to openedge SQL server.  Exiting')
      sys.exit(2)
   logger.info('Connected')

   try :
      maincurs = conn.cursor()
   except Exception as e :
     logger.error(f'Could not connect to cursor {e}')
     sys.exit(2)  
   
   # connect to Kafka producer
   logger.info('Attempting to connect to Kafka Producer')
   p = qadoemdbetl.conn_kafka_producer(cfg,logger)
   if p == False :
      logger.error('Failed to connect to Kafka Producer.  Exiting')
      sys.exit(2)
   logger.info('Connected')  
   
   # getting table list
   logger.info('Getting list of CDC tables')
   tables,seq = qadoemdbetl.cdc_get_tables( conn, tables, seq, cfg, logger)
   if tables == False :
      logger.error('Failed to get CDC table list.  Exiting')
      sys.exit(2)
   logger.info('Got table list')   
  
   # get sequence start values
   # we do not want to read all CDC records, only read them from the last one previously processed
   
   logger.info('Getting sequence starting values from cdc_det')
   # Polling 
   seq = qadoemdbetl.cdc_sequence_start( conn, seq, cfg, logger)
   if seq == False :
      logger.error('Failed to get CDC start sequences.  Exiting')
      sys.exit(2)
   logger.info('Got starting sequences')   
    
   try :
      exclude_tables = cfg['cdc_exclude_tables']
      clob_tables = cfg['cdc_clob_tables']
      max_table_length = cfg['max_table_length']
      sleeptime = cfg['poller_sleeptime']
   except KeyError as e :
      logger.error(f'YAML file is missing key {e}')
      logger.error('Exiting')
      sys.exit(2)
   
   logger.info('Starting Loop')
   while True:
      loop_time = time.time()
      
      for table, tn in tables.items():
         if table in exclude_tables :
            logger.info('Skipping table %s' % table)
            continue
         if table in clob_tables :
            logger.debug('Skipping table with clob %s' % table)     
            continue            
         if len(table) > int(max_table_length) :
            logger.info('Skipping table with %s name length %d' % (table, len(table)))
            continue
                   
         logger.debug('Processing %s' % table)
         
         '''
         main tracking function
         '''
         
         seq,keys = qadoemdbetl.cdc_track_changes( conn, maincurs, p, table, keys, tn, seq, cfg, mandatorydict, logger)
         
      elapsed_time(loop_time)   
      time.sleep(int(sleeptime))
      
     
   print ('Finished')
   elapsed_time = time.time() - start_time
   print (f"Total Elapsed time: {elapsed_time} seconds")

   sys.exit(0)



