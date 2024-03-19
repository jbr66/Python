'''
push fully formed SQL from Cassandra to MariaDB.

Optionally stop on Error.  
DaemonMode means run forever, sleeping for daemonPoll
After Sweep, store the highwater mark.  Store record in new Cassandra table as "sunk"

YAML Config ( sample )


MariaDB :
   database : mfgdb
   user : root
   password : 1Adelaide01
   port : 3306
   host : localhost
   stopOnDuplicate : False
   stopOnError : True   
Cassandra :
   host : localhost
   keyspace : cdc
   port : 9042   
   username :
   password :
   ignoreHighWater : False   
source :
   host : ip-10-0-0-187
   qadenv : production
   qadsrcdb : mfgdb
log:
   defaultlevel : INFO
   logfile : /dr01/cdc/push.log
runlimit : 1000
daemonMode : True
daemonPoll : 10
'''
import sys
import socket
import os
import yaml
import argparse
import time
import signal
import logging
import resource
from datetime import datetime
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import mariadb

hostname = socket.gethostname()
parser = argparse.ArgumentParser(description='Extract CDC')

parser.add_argument("--cfg", help = "YAML cfg file location")
parser.add_argument("--loglevel", help = "Default Error.  Also supports warning, info")

try :
   args = parser.parse_args()
except SystemExit:
   print (__doc__)
   sys.exit(2)

if args.cfg is None :
   print ('ERROR : --cfg not specified.  Please use --cfg to point to YAML config file.')
   sys.exit(2)   
   
def _get_config(cfgfile):
   try :
      with open (cfgfile, 'r') as f :
         cfg = yaml.safe_load(f)
   except Exception as e :
      print ('Cannot find or load yaml cfg file %s' % cfgfile)
      print (e)
      print ('...exiting')
      sys.exit(2)

   return cfg

def connectCassandra(cfg) :

  print ('...')
  hosts = []
  try :
  
  
     hostlist = cfg['Cassandra']['host']
     for line in hostlist.split(',') :
         hosts.append(line)
     logging.info (hosts)    
     if cfg['Cassandra']['username'] != None :
        auth_provider = PlainTextAuthProvider(username=cfg['Cassandra']['username'], password=cfg['Cassandra']['password'])
        cluster = Cluster(hosts,cfg['Cassandra']['port'], auth_provider= auth_provider)  
     else :        
        cluster = Cluster(hosts,cfg['Cassandra']['port'])
     logging.info (cluster)
     session = cluster.connect(cfg['Cassandra']['keyspace'])     
     logging.info (session)
  
  except Exception as e :
     logging.error (e)
     return False,False
     
  logging.warning ('Connected to Cassandra on host %s keyspace %s' % (cfg['Cassandra']['host'],cfg['Cassandra']['keyspace']))
  
  return (cluster,session)
  
def connectMariaDB(cfg) :  

   try :
      conn = mariadb.connect(user="%s" % cfg['MariaDB']['user'], password="%s" % cfg['MariaDB']['password'], host="%s" % cfg['MariaDB']['host'], port=cfg['MariaDB']['port'], database="%s" % cfg['MariaDB']['database'])
      curs = conn.cursor()
   except Exception as error :
      logging.error  ("Error while connecting to MariaDB on host %s with user %s and port %d" % ( cfg['MariaDB']['host'],cfg['MariaDB']['user'],cfg['MariaDB']['port']))
      logging.error (error)
      return False,False

   logging.warning ('Connected to %s' % conn)
   
   return conn,curs
  
def getHighWater(session,cfg) :

    hw = datetime.fromtimestamp(0)
    seq = 0
    qry = "select hw from %s.highwater where host = '%s' and qadenv = '%s' and qadsrcdb = '%s'" % ( cfg['Cassandra']['keyspace'],cfg['source']['host'],cfg['source']['qadenv'],cfg['source']['qadsrcdb'])
    logging.info(qry)
    try :
       rows = session.execute(qry)
       if not rows :
          logging.warning ('No highwater record, inserting')
          qry = "insert into %s.highwater (host,qadenv,qadsrcdb,hw,seq) values ( '%s','%s','%s','%s',0 ) " %  (cfg['Cassandra']['keyspace'],cfg['source']['host'],cfg['source']['qadenv'],cfg['source']['qadsrcdb'], hw.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
          logging.info(qry)
          rows = session.execute(qry)
          
          return hw
       else :
          for line in rows :
             hw = line[0]
             
             return hw
    except Exception as e :
       logging.error (e)
       logging.error ('Error getting high water mark')
    
    return hw 
     
def setHighWater(session,cfg,hw) :

    qry = "update %s.highwater set hw = '%s' where host = '%s' and qadenv = '%s' and qadsrcdb = '%s'" % (  cfg['Cassandra']['keyspace'],hw.strftime( '%Y-%m-%d %H:%M:%S.%f')[:-3],cfg['source']['host'],cfg['source']['qadenv'],cfg['source']['qadsrcdb'])
    logging.info(qry)
    try :
       rows = session.execute(qry)

    except Exception as e :
       logging.error(e)
       logging.error('Error setting highwater mark with %s' % qry)
       return False
    
    return True      
     
def readDML(session,cursor,cfg,conn) :

    hw = getHighWater(session,cfg)
    logging.info ('Highwater is %s' % hw.strftime( '%Y-%m-%d %H:%M:%S.%f')[:-3])
    
    now = datetime.now()
    
    # DML
    qry = "select * from %s.dml_mariadb where host = '%s' and qadenv = '%s' and qadsrcdb = '%s' and qaddt > '%s' LIMIT %d "  % (cfg['Cassandra']['keyspace'],cfg['source']['host'],cfg['source']['qadenv'],cfg['source']['qadsrcdb'],hw.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] , cfg['runlimit'])
    logging.info (qry)
    rows = session.execute(qry)
    
    if rows :
      hw = pushDML ( rows, cursor, conn, hw) 
    
      # update HWM
      res = setHighWater ( session,cfg,hw)
      if not res :
         return False

    now = datetime.now() - now
    logging.error ('Time to process:')
    logging.error(now)
    return True     
   
def pushDML ( rows,cursor,conn,hw) :

    found = False
    # sink rows into MariaDB, return last row as hw mark
    for line in rows :
       found = True
       hw = line[3]
       seq = line[4]
       payload = line[6]
       try :
          logging.info(payload)
          cursor.execute(payload)
          conn.commit()
       except mariadb.IntegrityError as e :
   
          logging.error ('Error inserting %s ' % qry)  
          if cfg['MariaDB']['stopOnDuplicate'] == True :
             logging.error ('Stop on Duplicate.  Exiting')
             conn.rollback()
             
             return False
          else :
          
             logging.error ('Ignoring Duplicate %s ' % qry)
             conn.rollback()
       except mariadb.Warning as e1 :
          logging.error ('Warning %s' % qry)
          logging.error ('Data may be truncated or incorrect on row')
          if cfg['MariaDB']['stopOnError'] == True :
            logging.error('stopOnError is True so exiting')
            conn.rollback()
            return False

       except mariadb.DataError as e2 :
          logging.error ('DataError %s' % qry)    
          if cfg['MariaDB']['stopOnError'] == True :
            logging.error('stopOnError is True so exiting')
            conn.rollback()
            return False        
       except Exception as e3 :
          logging.error ('General Exception Error %s' % qry)    
          if cfg['MariaDB']['stopOnError'] == True :
            logging.error('stopOnError is True so exiting')
            conn.rollback()
            return False   

    if found == False :
       logging.info ('No Rows')
    return hw
   
   
def signal_term_handler(signal, frame):
    time.sleep(10)
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
    #sys.exit(0)
    return False
    
    
if __name__ == '__main__': 

   
   cfg = _get_config(args.cfg)   

   loglevel = cfg['log']['defaultlevel']
   logfile = cfg['log']['logfile']
   
   
   # command override?
   if args.loglevel :
       loglevel = args.loglevel


   if loglevel == 'INFO' :
      logging.basicConfig(filename=logfile,level=logging.INFO,format='%(asctime)s [%(levelname)s] %(message)s')
   elif loglevel == 'WARNING' :
      logging.basicConfig(filename=logfile,level=logging.WARNING,format='%(asctime)s [%(levelname)s] %(message)s')
   elif loglevel == 'ERROR' :
      logging.basicConfig(filename=logfile,level=logging.ERROR,format='%(asctime)s [%(levelname)s] %(message)s')
   else :
      print ('Cannot determine loglevel, setting to ERROR')
      logging.basicConfig(filename=logfile,level=logging.ERROR,format='%(asctime)s [%(levelname)s] %(message)s')
      
   print ('Logfile is %s as specified in %s ( log: <CR>  logfile )' % ( logfile, args.cfg ))  
   
   logging.warning ('Connecting to Cassandra')
   cluster,session = connectCassandra(cfg)
   if cluster is False :
      logging.error ('Could not connect to Cassandra, exiting')
      sys.exit(2)
      
   logging.warning('Connecting to MariaDB')
   conn,cursor = connectMariaDB(cfg)
   if conn is False :
      logging.error ('Could not connect to MariaDB, exiting')
      sys.exit(2)   
   
   while True :
      result = readDML (session, cursor, cfg, conn)
      if result == False and cfg['MariaDB']['stopOnError'] == True:
         logging.error ('Exiting with Errors.')
         break
      elif result == False :
         logging.error ('Continuing past Error as stopOnError set to False')

      if cfg['daemonMode'] == False :
         break
      time.sleep(cfg['daemonPoll'])   
         
         
   conn.close()
   cluster.shutdown()
   print ('Connection to Cassandra shut down')
   
   logging.warning ('Connection to Cassandra shut down')
   sys.exit(0)
   