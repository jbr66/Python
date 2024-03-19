"""
  qadcheckdata.py
    
  Supports Python3.7+
  not tested on Python3.6
  
  December 2022
  
  Rules :
     (1)  Assume default encoding is utf8mb4
          - 4 bytes per character
     (2)  If latin1 is explicit, then char is 1 byte per character
     (3)  Other storage requirements in YAML definition below
     (4)  Max index width is 3072 bytes : error
               warning over 2000
     (5)  If field contents > varchar width :  error
     
  This program checks the data extracted by the Python ETL extract functions in program qadoemdbetl.py to look for
  integrity issues that might prevent rows being loaded into MariaDB under strict mode  
  
  Usage notes :   python3.7 qadcheckdata.py --cfg /path/to/[yamlconfigfile].yaml --overrides
  
  requires qadoemdbetl.py
     
"""

import sys
import qadoemdbetl
import os
import yaml
import argparse
import socket
import logging

# Defaults
schemafile = 'dat'
idxfile = 'idx'
datafile = 'dump'
maxidxwidth = 3072

bytedict = {}
bytedict['character'] = 4
bytedict['latin1'] = 1
bytedict['tinyint'] = 1
bytedict['logical'] = 1
bytedict['int'] = 4
bytedict['int64'] = 8
bytedict['float'] = 4
bytedict['decimal'] = 8 
bytedict['date'] = 4
bytedict['time'] = 4
bytedict['datetime'] = 8
bytedict['datetime-tz'] = 8

exclude_tables = []
include_tables = []




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
       '''
       if 'pass' in arg :
          print ('Adding Argument %s with HIDDEN value' % ( arg))
       else :    
          print ('Adding Argument %s with default value: %s ' % ( arg, cfg[arg]))
       '''
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


'''
Functions Start Here
'''

def checkdata(datfn,schema,cfg,logger) :
  table = schema['table']
  print(table)
  
  #if not include_tables == [] :
  if len(include_tables) > 0 :
     if not table in include_tables :
        print ('Skipping %s' % table )
        return True
  
  if table in exclude_tables :
     print ('Skipping %s' % table)
     return True
  else :     
     logger.info ('Processing Data for table %s ' % table )
  
  try :
      f = open(datfn,'r')

  except Exception as e :
      logger.info (e)
      logger.info ('ERROR could not open %s' % datfn)
      return False
      
  # this is memory efficient

  count = 0
  for line in f :
    count += 1
    if count == 1 :
       continue
    tokens = line.split('^')
    logger.info(tokens)
    order = 1
    for token in tokens :
       #if order == 0 :
       #    order += 1
       #    continue
       
       try :
          logger.info(table + '.' + str(order))
          field = schema[table + '.' + str(order)]
          logger.info(field)
          # check type is character
          if schema[table + '.' + field + '.type'] == 'character' :
             logger.info('%s is %s' % (field, table + '.' + field + '.type'))
             logger.info(schema[table + '.' + field + '.type'])
             width = int(schema[table + '.' + field + '.width'])
             logger.info(width)
             # get the data
             o = order -1
             fv = tokens[o]
             fv = fv.strip()
             logger.info(fv)
             if fv != '' : 
                
                fvl = len(fv)
              
                #uncommenting this will cause the largest logfile you have ever seen
                #print ('field is %s with width %d and value %s with width %d' % ( field,width,fv,fvl))   
                if fvl > width :
                   logger.error('Table %s field %s with width %d and value %s with width %d' % ( table,field,width,fv,fvl))  
       except Exception as e :
          logger.info(e)
       order += 1   
          
  f.close()  
  

def checkindexes(idxfn,schema, cfg, logger) :

  table = schema['table']
  logger.info ('Processing indexes for table %s ' % table )

  try :
      f = open(idxfn,'r')
      lines = f.readlines()

  except Exception as e :
      logger.info (e)
      logger.info ('ERROR could not process %s' % idxfn)
      return False
  f.close()
  
  good = True
   
  istring = ''
  icount = 0
  for line in lines :
     line = line.strip()
    
     
     tokens = line.split(',')
     logger.info (tokens)
     
     if ',1' in line :
        logger.info('accumulated %d %s' % (icount,istring) )
        if istring != '' : 
           istring = istring + 'TOTAL WIDTH:%d' % icount

           if icount > maxidxwidth :
              good = False
              logger.error ('**** INDEX %s for table %s TOO WIDE %d is greater than max %d ****' % (tokens[0],table,icount,maxidxwidth))
        istring = 'Index:%s,' % tokens[0]
        icount = 0
        
        
     try :
        fld = tokens[3]

        key = table + '.' + fld + '.type'

        fldtype = schema[key] 

        wkey = table + '.' + fld + '.width'


        tkey = table + '.' + fld + '.type'
        fldtype = schema[tkey]
     except KeyError as e :
        logger.info (e)
        continue
     logger.info(fldtype)
     if fldtype == 'character' :

        try :
           w = int(schema[wkey])

       
           fldwidth = w * bytedict['character']
        except KeyError as e:
           logger.info(e)        
     else :

        try :
           fldwidth = bytedict[schema[tkey]]
        except KeyError as e:
           logger.info(e)         


     icount = icount + fldwidth

     istring = istring + '%s(%d),' % (fld,fldwidth) 
        
  if icount > maxidxwidth :
              good = False

              logger.error ('**** INDEX %s for table %s TOO WIDE %d is greater than max %d ****' % (tokens[0],table,icount,maxidxwidth))        

  return True

def processfile(filename, cfg, logger) :

   try :
       
       idxfn = filename.path.split('.')[0] + '.' + idxfile
       datfn = filename.path.split('.')[0] + '.' + datafile
       
       if os.path.isfile(idxfn) :
          logger.info ('Processing Schema %s with index file %s' % (filename.path,idxfn))
          
          schema = readschema(filename, cfg, logger)
          if schema == False :
             logger.error ('Cannot process schema for %s' % filename)
             return False
          logger.info (schema)
          
          result = checkindexes(idxfn,schema, cfg, logger)
          if not result :
              logger.error ('Cannot check index widths for %s' % filename)
         
       if os.path.isfile(datfn) :   
          logger.info ('Processing Dumpfile %s with data file %s' % (filename.path,datfn))
          result = checkdata(datfn,schema,cfg,logger)
         
   except Exception as e:
       logger.error(e)
       return False

   return True
    
def readschema(filename, cfg, logger) :

   schema = {}

   try :
      f = open(filename.path,'r')
      lines = f.readlines()

   except Exception as e :
      logger.error (e)
      logger.error ('ERROR could not process %s' % filename.path)
      return False
   f.close()

   try :
      order = 1
      for line in lines :
         line =  line.strip() 
         if line == '' : 
            continue
          
         tokens = line.split(';')
         table = tokens[0]
         field = tokens[1]
         
         schema['table'] = table
         schema[table + '.' + field + '.type'] = tokens[2]
         schema[table + '.' + str(order)] = field
         schema[table + '.' + field + '.width'] = tokens[7]
         schema[table + '.' + field + '.extent'] = tokens[4]
         schema[table + '.' + field + '.initial'] = tokens[5]
         schema[table + '.' + field + '.mandatory'] = tokens[6]
         order += 1
   except Exception as e :
      logger.error (e)
      return False      


   logger.info ('(*')
   return schema
   

if __name__ == '__main__' :

   '''
   requires AT LEAST the --cfg argument pointing to the YAML control file
   '''

   if len(sys.argv) < 3 :
       print ('Usage :  qadcheckdata.py --cfg cfgfile [--arg value --arg value]')
       print ('Missing cfgfile.  Exiting')
       sys.exit(2)

   if not sys.argv[1] == '--cfg' :
       print ('%s not recognized' % (sys.argv[1]))
       print ('Usage :  qadcheckdata.py --cfg cfgfile [--arg value --arg value]')
       sys.exit(2)
       
   cfgfile = sys.argv[2]
   cfg = _get_config(cfgfile)       
   hostname = socket.gethostname()

   parser = argparse.ArgumentParser()
   parser = add_arguments(parser,cfg)
   
   try :
      args = parser.parse_args()
   except SystemExit:
      sys.exit(2)

   cfg = process_overrides(args,cfg)

   # Setup logging
   logger = logging.getLogger(__name__)
   formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

   # Create console logger
   cl = logging.StreamHandler()
   cl.setLevel(logging.ERROR)
   cl_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
   cl.setFormatter(cl_format)
   logger.setLevel(logging.INFO)
   logger.addHandler(cl)

   print (cfg['loglevel'])
   if cfg['loglevel'] == 'ERROR' :
      error_handler = logging.FileHandler(cfg['check_log'])
      error_handler.setLevel(logging.ERROR)
      #logger.setLevel(logging.ERROR)
      error_handler.setFormatter(formatter)
      logger.addHandler(error_handler)
   else :
      logger.setLevel(logging.INFO)

      info_handler = logging.FileHandler(cfg['check_log'])
      info_handler.setFormatter(formatter)
      info_handler.setLevel(logging.INFO)
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

   try :
      exclude_tables = cfg['exclude_tables']
      include_tables = cfg['include_tables']
      max_table_length = cfg['max_table_length']
      maxidxwidth = int(cfg['maxindexwidth_error'])
      maxidxwidthwarn = int(cfg['maxindexwidth_warn'])
      dir = cfg['stage']
       

   except KeyError as e :
      logger.error(f'YAML file is missing key {e}')
      logger.error('Exiting')
      sys.exit(2)   
    
   logger.info('Checking data files in %s' % dir)
   
   # Check working directory / Dumppath
   if not os.path.isdir(dir) :
      logger.info ('ERROR: Cannot open directory specified by -d ( %s )' % dir)
      sys.exit(2)
 
   # Work through each schema file in directory, sort them first
   f = os.scandir(dir)
   files = list(f)
   files.sort(key=lambda x: x.name)
   logger.info (files)
   for filename in files :

      if filename.is_file()  :
         logger.info ('Process file: %s' % filename.name)
         # Is file size zero?

         try :
            
            if filename.name.split('.')[1] != schemafile :
               continue
         except Exception as e :
            pass # do not care
            
         table = filename.name.split('.')[0]
         logger.info('Found table %s' % table)
               

         if table in exclude_tables :
            logger.info('%s is excluded' % table)
            continue

         logger.info('Size of include_tables: %d' % len(include_tables))
         if len(include_tables) > 0 :
         #if include_tables != '' :
            if not table in include_tables :
               logger.debug('table %s not in include list, skipping' % table)
               continue               
            
         if os.stat(filename).st_size == 0 :
            logger.info ('Skipping empty structure file %s' % filename.name)
            continue

         logger.info ('Processing table %s' % table) 
         logger.info(filename)
         result = processfile(filename, cfg, logger)
         if not result :
            logger.error('Error procesing %s' % filename)
            

      
   sys.exit(0)      
