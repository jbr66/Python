'''
sequences stored in cdc_det

cdc_table = "tablename"
cdc_sequence = "sequence"
cdc_watermark = for callback only, stores downstream sequence high value processed
LastModifiedDateTime = datetime of update

Cannot handle tables with arrays or tables that are too long in name

YAML file contents (sample )

oe:
   db : mfgdb
   ldb : qaddb
   dlc : /tech/progress/dlc1175_004
   owner : CDC
   service:  22183
   user : mfg
   pass : mfgpro
   exclude_tables : 
       cdc_det,fcInstance,DistributedTransaction,DistributedTransactionData,
       DistributedTransactionResource,ItemStatusRestrictedTransaction
   large_clob_tables : Document,EntityMapping,EntityMetaData,EventHandler,
       ServerScript,StoredView,ViewMetaData,ViewResourceMetaData
   extent_fields : pt_same_days;10,pt_invent_days;10,ad_edi_ctrl;5,
       cm__qad04;3,cm_slspsn;4,abs_doc_data;5,AIMCharFld;15,
       AIMDecFld;15,AIMDateFld;4,ar_xcomm_pct;2,ar_comm_pct;4,ar_slspsn;4,
       ar_comm_amt;4,ar_base_comm_amt;4,aud_old_data;15,aud_new_data;15,
       calm_wdays;7,calm_hours;7,calm_shifts;7,cd_cmmt;15,cmt_cmmt;15,
       cph_qty;12,cph_sales;12,cph_cost;12,cph__dec01;12,cph__dec02;12,
       dep_canrun;15,dpc_acq_pct;4,dpc_rt_pct;4,dpr_eq;15,dss__qad05;2,
       ecm_cmmt;5,ega_calls;7,ega_hours;7,ega_avail_hours;7,egc__qadc05;4,
       egc__qadc06;4,egd_days;8,egd_end_time;8,egd_start_time;8,egd_mid_etime;8,
       egd_mid_stime;8,egw_calls;7,egw_avail_hours;7,egw_hours;7,es_doc_desc;7,
       es_doc_exec;7,es_doc_printed;7,es_doc_printit;7,es_doc_printer;7,
       es_doc_paged;7,esh_end_time;8,esh_start_time;8,esh_days;8,esh_mid_etime;8,
   esh_mid_stime;8,eus_etime;7,eus_stime;7,eus_mid_etime;7,eus_mid_stime;7,
   eus_days;7,fcs_fcst_qty;52,fcs_sold_qty;52,fcs_pr_fcst;52,fcs_abnormal;52,
   ff_his_yr;5,ff_orig_fc;24,ff_adj_fc;24,fh_rlup_pct;52,flp_prod_act;52,
   flp_prod_fcst;52,flp__dec03;52,flp__dec04;52,fp1_bklg_act;52,
   fp1_bklg_fcst;52,fp1_cost_act;52,fp1_cost_fcst;52,fp2_inv_act;52,
   fp2_inv_fcst;52,fp2_ord_act;52,fp2_ord_fcst;52,fp3_prod_act;52,
   fp3_prod_fcst;52,fp3_ship_act;52,fp3_ship_fcst;52,fpc_amt;15,
   fpc_max_price;15,fpc_min_qty;15,fslp_prod_fcst;52,fslp_prod_act;52,
   fslp__dec03;52,fslp__dec04;52,fsp1_bklg_act;52,fsp1_bklg_fcst;52,
   fsp1_cost_act;52,fsp1_cost_fcst;52,fsp2_inv_act;52,fsp2_inv_fcst;52,
   fsp2_ord_act;52,fsp2_ord_fcst;52,fsp3_prod_act;52,fsp3_prod_fcst;52,
   fsp3_ship_act;52,fsp3_ship_fcst;52,genfldd_charvalues;25,
   genfldd_decimalvalues;25,genfldd_integervalues;25,genfldd_datevalues;25,
   genfldd_logicalvalues;25,gr_qtr_lbl;4,grcd_label;3,grcd_calc;5,
   gri_text_ix;3,gri_ovr_code;5,gri_ovr_type;5,gric_label;3,grid_text;5,
   grrd_text;5,grrd_calc;5,grx_text_ix;3,idh_comment;5,idh_xslspsn;3,
   idh_xcomm_pct;2,idh_slspsn;4,idh_comm_pct;4,idh_cum_date;4,idh_cum_qty;4,idh_curr_rlse_id;3,idh_start_eff;4,idh_end_eff;4,ih_xslspsn;2,ih_xcomm_pct;2,ih_tax_pct;3,ih__qad05;2,ih_comm_pct;4,ih_slspsn;4,ItemOwner;4,Percentage;4,kbc_time_adj;5,knbdd_card_cmmt_page;5,MsgText;15,msg_explanation;11,pac_amt;4,pac_apr_by;4,SameDays;10,InventDays;10,pc_min_qty;15,pc_amt;15,pc_max_price;10,pcc_pco_pre;12,pcc_next_pco;12,pgm_cmmt;20,pjd_comm_pct;4,pjd_slspsn;4,mfgpost_com;5,po_tax_pct;3,pod__qad04;5,pod_cum_qty;4,pod_cum_date;4,pod_curr_rlse_id;3,pod_start_eff;4,pod_end_eff;4,pp_ship_fcst;12,pp_ship_act;12,pp_ord_fcst;12,pp_ord_act;12,pp_inv_act;12,pp_bklg_act;12,pp_cost_fcst;12,pp_cost_act;12,pp_prod_fcst;12,pp_prod_act;12,prh_curr_rlse_id;3,prj_comm_pct;4,prj_slspsn;4,pti_same_days;10,pti_invent_days;10,qad_charfld;15,qad_decfld;15,qad_datefld;4,qad_logfld;15,qad_charfld1;15,qad_intfld;15,qo_xslspsn;2,qo_xcomm_pct;2,qo_tax_pct;3,qo__qad05;2,qo_comm_pct;4,qo_slspsn;4,qod__qad01;5,qod_xslspsn;3,qod_comm_pct;2,qod_slspsn;4,rmd_comment;5,rqa_alt_apr;2,rqd_oot_extra;8,sa__qadc05;2,sa_xcomm_pct;2,sa_tax_pct;3,sa_comm_pct;4,sa_slspsn;4,sac_trl_tax;3,sac_trl_ntax;3,sad_comment;5,sad_xslspsn;3,sad_xcomm_pct;2,sad_slspsn;4,sad_comm_pct;4,sadh_comment;5,sadh_comm_pct;4,sadh_slspsn;4,sah_xcomm_pct;2,sah_xslspsn;2,sah_tax_pct;3,sah_comm_pct;4,sah_slspsn;4,sch_lr_asn;10,sch_lr_date;10,sch_lr_qty;10,sch_lr_cum_qty;10,sch_lr_time;10,shm_ship_day;7,shm_rec_day;7,shop_wdays;7,shop_hours;7,shop_shifts;7,shtr__qad05;2,sim_canrun;15,so_xslspsn;2,so_xcomm_pct;2,so_tax_pct;3,so__qad05;2,so_slspsn;4,so_comm_pct;4,soc_ntaxdesc;10,soc_trl_tax;3,soc_trl_ntax;3,sod_comment;5,sod_xslspsn;3,sod_xcomm_pct;2,sod_cum_qty;4,sod_cum_date;4,sod_slspsn;4,sod_comm_pct;4,sod_curr_rlse_id;3,sod_start_eff;4,sod_end_eff;4,sod_cum_time;4,sph_sales;12,sph_cost;12,sph_quota;12,sph__dec01;12,sph__dec02;12,sro_cmmt;16,sro_tax_pct;3,sv_days;7,sv_stime;8,sv_etime;8,sv_mid_etime;8,sv_mid_stime;8,tax_tax_pct;3,tax_acct;3,tax_cc;3,taxd_taxamt;3,taxd_ntaxamt;10,te_pgm_msgs;10,tr_slspsn;4,tx2__qadc01;2,tx2__qadc02;2,tx2d__qadd01;3,tx2d__qadd02;10,usrw_charfld;15,usrw_decfld;15,usrw_datefld;4,usrw_logfld;15,usrw_intfld;15,vo_tax_pct;3,AIMCharFld;15,aud_old_data;15,aud_new_data;15,cd_cmmt;15,cmt_cmmt;15,dep_canrun;15,dpr_eq;15,MsgText;15,msg_explanation;11,pcc_pco_pre;12,qad_charfld;15,qad_charfld1;15,sch_lr_asn;10,sim_canrun;15,soc_ntaxdesc;10,sro_cmmt;16,te_pgm_msgs;10,usrw_charfld;15,genfldd_charvalues;25,ih_xslspsn;2,pgm_cmmt;20,qo_xslspsn;2,rqa_alt_apr;2,sah_xslspsn;2,sa__qadc05;2,so_xslspsn;2,tx2__qadc01;2,tx2__qadc02;2,grcd_label;3,gric_label;3,idh_xslspsn;3,idh_curr_rlse_id;3,pod_curr_rlse_id;3,prh_curr_rlse_id;3,qod_xslspsn;3,sac_trl_tax;3,sac_trl_ntax;3,sad_xslspsn;3,soc_trl_tax;3,soc_trl_ntax;3,sod_xslspsn;3,sod_curr_rlse_id;3,tax_acct;3,tax_cc;3,ar_slspsn;4,cm_slspsn;4,egc__qadc06;4,gr_qtr_lbl;4,idh_slspsn;4,ih_slspsn;4,ItemOwner;4,pac_apr_by;4,pjd_slspsn;4,prj_slspsn;4,qod_slspsn;4,qo_slspsn;4,sad_slspsn;4,sadh_slspsn;4,sah_slspsn;4,sa_slspsn;4,sod_slspsn;4,so_slspsn;4,tr_slspsn;4,abs_doc_data;5,ad_edi_ctrl;5,ecm_cmmt;5,grcd_calc;5,grid_text;5,gri_ovr_code;5,gri_ovr_type;5,grrd_text;5,grrd_calc;5,idh_comment;5,kbc_time_adj;5,pod__qad04;5,mfgpost_com;5,qod__qad01;5,rmd_comment;5,sad_comment;5,sadh_comment;5,sod_comment;5 
   extent_special :
       qad_charfld1 : qad_charfld111,qad_charfld122,qad_charfld133,qad_charfld144,qad_charfld155,qad_charfld16,qad_charfld17,qad_charfld18,qad_charfld19,qad_charfld110,qad_charfld1116,qad_charfld112,qad_charfld113,qad_charfld114,qad_charfld115
   max_table_length : 29
   driverstring : com.ddtek.jdbc.openedge.OpenEdgeDriver
   initstring :
kafka:
   sendtopic : cdc
   server : localhost
   port : 9092
   user : username
   password : password
   headers :
      source : 'urn:system:cdc'
      specversion : 1.0
      type : cdc
      datacontenttype : application/sql
      qadsnkdb : mfgdb
      qadenvtype : production
      responsetopic : cdccallback
log:
   defaultlevel : INFO
   logfile : /dr01/cdc/extract.log
sql:
   quotefields : CHAR,DATE
   emptyToNull : False
fwd :
   flattenextents : True
   primarykey : recid
   seqval : p2j_id_generator_sequence
poller :
   sleeptime : 1

'''


import sys
# import os
import yaml
import argparse
import socket
# import tempfile
# import subprocess
import time
import signal
import logging
import uuid
import resource
from datetime import datetime
# from decimal import Decimal
import jaydebeapi
from confluent_kafka import Consumer, KafkaError, Producer

hostname = socket.gethostname()

'''
Set up Base Dictionaries
'''
# dictionaries are *insertion* ordered as of Python 3.6
tables = {}
# sequence number
seq = {}
# CDC keys 
keys = {}
# extents
extentdict = {}
# mandatory fields
# if key [tablename] == fieldname then field is mandatory.
# If dictionary key fails to resolve, then not mandatory
mandatorydict = {}

'''
get args
'''

# simply a session counter to ensure we don't have duplicates 
# based on two messages on the same microsecond.
# It could happen on fast processors.
globalseq = 0

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

def connoe ( host, service, db, dlc, username, password ) :

   #driverstring = "com.ddtek.jdbc.openedge.OpenEdgeDriver"
   driverstring = cfg['oe']['driverstring']
   initstring = cfg['oe']['initstring']
   # ;INITIALIZATIONSTRING=(SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED)
   connstring = "jdbc:datadirect:openedge://%s:%s;DatabaseName=%s[-mdbq:alldb]" % (host,service,db )
   dlcstring = dlc + "/java/openedge.jar" 
   credentials = []
   credentials.append(username)
   credentials.append(password)
   logging.info ('Connecting to OE using %s' % connstring)
   conn = jaydebeapi.connect(driverstring,connstring,credentials,dlcstring)
   logging.info(conn)
   
   return conn
   
def displayresult(result) :

   for line in result :
      logging.info (line )
      
   return
   
   
def gettables ( conn,curs, tables ) :

   '''
   gets list of tables for processing.  Once per session.
   '''
   
   owner = cfg['oe']['owner']
   
   qry = 'select f."_File-name", f."_File-number" from PUB."_File" f join PUB."_CDC-Table-Policy" tp on f.rowid = tp."_Source-File-Recid"'
   curs,result = runquery ( conn, curs, qry )
   
   for line in (list(result)) :
      if result :
         tables[line[0]] = line[1]
         seq[line[0]] = 0
   
   return tables,seq
   
def getsequence (  conn, curs, table, seq ) :

   owner = cfg['oe']['owner']
   
   thisseq = 0

   qry =  'select cdc_table,cdc_sequence from PUB.cdc_det where cdc_table = \'%s\'' % (table )
   curs,result = runquery ( conn, curs, qry )

   if result is False :
       return thisseq
       
   for line in (list(result)) :
      logging.info(line[1])
      thisseq = line[1]

   return thisseq
   
   
def getsequences ( conn,curs, seq ) :


   owner = cfg['oe']['owner']
    
   qry = 'select cdc_table, cdc_sequence from PUB.cdc_det'  
   curs,result = runquery ( conn, curs, qry )
     
   logging.info ('Sequences --> ')
   for line in (list(result)) :
      logging.info (line )
      seq[line[0]] = line[1]

   return (curs,seq)
   

def runquery(conn,curs,qry ) :

   try :
      if not curs :
         curs = conn.cursor()
   except :
      curs = conn.cursor()
      logging.info ('connected to cursor')

   try :
      curs.execute(qry)
      result = curs.fetchall()
   except Exception as e :
      logging.error ('ERROR running query %s' % qry )
      logging.error (e)
      return (curs, False )
      
   if type(result) is str :
      logging.error ('ERROR running query %s ( string returned, not cursor )' % qry )
      return (curs, False )
      
   return ( curs, result)   
   
def runupdate(conn,curs,qry ) :

   try :
      if not curs :
         curs = conn.cursor()
   except :
      curs = conn.cursor()
      logging.info ('connected to cursor')

   try :
      curs.execute(qry)
   except Exception as e :
      logging.error ('ERROR running query %s' % qry )
      logging.error (e)
      return (curs, False )
         
   return ( curs,True )      

   
def getkey (table, policyid, conn ):
   
   # new cursor
   
   key = ''
   owner = cfg['oe']['owner']
   
   try :
      if not kcurs :
         kcurs = conn.cursor()
   except :
      kcurs = conn.cursor()
      logging.info ('connected to kcursor')   
   
   qry = 'select k."_field-position", k."_identifying-field" from PUB."_cdc-field-policy" k where k."_policy-id" = \'%s\' and k."_identifying-field" > \'0\' order by k."_identifying-field"' % ( policyid )  
   logging.info('Get Key Query %s' % qry)
   kcurs,result = runquery ( conn,kcurs,qry )
   if result is False :
      logging.error ('Error getting key with %s' % qry)
      logging.error (result)
      key = ''
      
   for row in result :
    
      key = row
      break 
      # will this ever have more than one row?  test
    
   # release cursor
   logging.info ('close kcurs')
   kcurs.close()
   
   logging.info ('key is %s' % type(key))

   return key
   
def getMandatory(table,conn ) :

   mlist = []

   '''
   we have non unique key fields marked as MANDATORY in the QAD schema.  This is pretty haphazard so we want to insert empty strings instead of NULLs on the fields that are mandatory.  Note that FWD simply ignores NULLs altogether and always inserts a default value.
   '''
   try :
      if not kcurs :
         kcurs = conn.cursor()
   except :
      kcurs = conn.cursor()
      logging.info ('connected to kcursor')   


   # like this :   select "_field-name" from pub."_field" WHERE "_mandatory" = 1 and "_file-recid" = (SELECT ROWID FROM pub."_file" WHERE "_file-name" = 'tr_hist') ;
   qry = 'select "_field-name" from pub."_field" WHERE "_mandatory" = 1 and "_file-recid" = (SELECT ROWID FROM pub."_file" WHERE "_file-name" = \'%s\')' % table

   kcurs,result = runquery ( conn,kcurs,qry )
   logging.error(result)
   if result is False :
      logging.error ('Error getting mandatory fields with %s' % qry)
      logging.error (result)
      return False
      
      
   for row in result :
      mlist.append(row[0])


   if mlist :
      mandatorydict[table] = mlist
   return True
   
   
   
def trackchanges ( conn,curs,seq,table,tn, keys, p, extentdict ) :

   '''
   field map :
      _policy-id, _operation, _tran-id, _time-stamp, _change-sequence, _continuation_position, _arrayindex, _fragment
   '''

   first = 0
   count = 0
   owner = cfg['oe']['owner']
   
   # refresh sequence value for table
   try :
      chgseq = seq[table]
      
   except Exception as e :
      logging.error (e)
      chgseq = 0
      

   if chgseq > 0 :
      logging.info ('checking sequence current value for %s' % table)
      
      chgseq = getsequence ( conn, curs, table, seq )
      logging.info ('seq = %d' % chgseq )
           
   initchgseq = chgseq        
   logging.info ('tracking change for %s' % tn )
  
   

   qry = 'select ct."_policy-id",ct."_operation",c.* from PUB."_cdc-change-tracking" ct inner join %s.CDC_%s c ON ct."_Change-sequence" = c."_Change-sequence" where ct."_Change-Sequence" > %d and ct."_Source-Table-Number" = %s order by ct."_Source-Table-Number", ct."_Change-Sequence"' % (owner,table,chgseq,tn)
   curs,result = runquery ( conn, curs, qry )
   if result is False :
      logging.error ('ERROR running extraction')
      return ( seq,keys )
   else :
      #column_names = [table + '.' + i[0] for i in curs.description] 
      #column_types = [i[1].values[0] for i in curs.description]
      #fieldmap = dict(zip(column_names, column_types))
      
      for row in result :
         
         if count == 0 :
            # column_names = [table + '.' + i[0] for i in curs.description] 
            column_names = [i[0] for i in curs.description]
            column_types = [i[1].values for i in curs.description]
            fieldmap = dict(zip(column_names, column_types))    
            logging.info ('FIELDMAP')
            logging.info (fieldmap)

            # does key exist from field policies?  if not, go get it.  key needed for deletes and updates.
            # Note that we assume that every table has a key, so at this point if we are getting a new key, we can go and grab the mandatory fields as well
            try :
               key = keys[table]
            except Exception as e :
               logging.error (e) 
               policyid = row[0]
               logging.error ('key not found for %s , searching field policies to add using policy id %s' % (table,policyid))
               key = getkey(table, policyid, conn )
               logging.error ('inserting into keys[]' )
               keys[table] = key
               logging.error ('refreshing mandatory fields for %s' % table )
               mres = getMandatory(table,conn)
               if mres == False:
                  logging.error ('Could not load mandatory fields.  SQL inserts may fail')
                  
         count = count + 1       
         operation = row[8]
         changeseq = row[4]
         
         logging.info ('Operation is %s' % operation )
         # if operation is add
         if operation == 1 :
             pushadd ( changeseq, row, column_names, fieldmap, table, p, extentdict )   

         if operation == 2 :
             pushdelete ( changeseq, row, column_names, fieldmap, table, p, key )
             
         if operation == 4 :
             pushupdate ( changeseq, row, column_names, fieldmap, table, p, key , extentdict, conn, curs)         


      # finally update cdc_det with correct change sequence for the table      
       
      if count == 0 :
         #logging.info ('No changes')
         return ( seq,keys)
         
      else :
         logging.warning ('final change sequence is %d initial was %d' % (changeseq,initchgseq))
         if initchgseq < changeseq :

             # does record exist?
             qry = 'select cdc_sequence from PUB.cdc_det WHERE cdc_table = \'%s\'' % (  table )
             curs,result = runquery ( conn, curs, qry )

             if len(result) == 0 :
                 logging.info ( 'no record' )

                 qry = 'insert into PUB.cdc_det ( cdc_table, cdc_sequence ) VALUES (  \'%s\' , %d )' % (  table, changeseq )
             else :

                 qry = 'update PUB.cdc_det set cdc_sequence = \'%d\' where cdc_table = \'%s\'' % ( changeseq, table )
             

             logging.info ('Upsert sequence query : %s' % qry)
             curs,result = runupdate ( conn,curs,qry )
             if result is False :
                 logging.error ('ERROR UPDATING cdc_det ( trying to store updated change sequence with query %s' % qry)
             else :
                 conn.commit()
                 
         return ( seq,keys)         
       
  
   return ( seq, keys )


def pushadd(changeseq, row, column_names, fieldmap, table, p, extentdict):

    owner = cfg['oe']['owner']
    ncurs = conn.cursor()

    mlist = []
    try:
        mlist = mandatorydict[table]
    except Exception as e:
      logging.info ('No mandatory fields for table %s - %s' % (table, e))

    # kstring = 'INSERT INTO %s ( NEXT VALUE FOR %s,' % ( table, cfg['fwd']['seqval'] )
    kstring = 'INSERT INTO %s (recid,' % (table)

    # first data field
    columncount = -1
    for k in row:
        columncount = columncount + 1
        # QAD fields start at 9
        if columncount < 9:
            continue

        if k is None:
            continue

        # skip empty strings if emptyToNull is True *UNLESS* the field is marked mandatory in OE schema
        if fieldmap[column_names[columncount]][0] == 'CHAR' and cfg['sql']['emptyToNull'] == False:
            # fwd mode, do nothing
            pass
        elif fieldmap[column_names[columncount]][0] == 'CHAR' and k == '':
            # empty string, but we still need to send it if the field is mandatory
            if column_names[columncount] in mlist:
                logging.info('found %s in mlist' % column_names[columncount])
            else:
                # do not send empty string on non mandatory field
                continue

        ef = []
        ev = []
        ec = 1
        # handle extents
        try:
            ext = extentdict[column_names[columncount]]
            logging.info('% has %d extents' % (column_names[columncount], ext))

            for val in k.split(';'):

                if val == '' or val == '?':
                    break

                ev.append(val)

            # special case
            if column_names[columncount] == 'qad_charfld1':
                logging.info ('SPECIAL CASE qad_wkfl')
                qad_charfld1 = cfg['oe']['extent_special']['qad_charfld1']
                colname = qad_charfld1.split(',')[ec - 1]
            else:
                colname = column_names[columncount] + str(ec)
            ef.append(colname)
            ec = ec + 1

            logging.info('extent fields')
            logging.info(ef)
            logging.info('extent values')
            logging.info(ev)
            for extentfield in ef:
                kstring = kstring + extentfield + ','

        except Exception as e:
            # process normal on the exception
            kstring = kstring + column_names[columncount] + ','
            logging.info('%s->%s->%s' % (
                column_names[columncount],
                fieldmap[column_names[columncount]][0],
                k))

    # strip last comma
    kstring = kstring[:-1]
    # add bracket
    kstring = kstring + ') VALUES (NEXT VALUE FOR %s,' % cfg['fwd']['seqval']

    # now the field values
    # first data field
    columncount = -1
    for k in row:
        columncount = columncount + 1
        # QAD fields start at 9
        if columncount < 9:
            continue

        if k is None:
            continue

        # skip empty strings if emptyToNull is True *UNLESS* the field is marked mandatory in OE schema
        if fieldmap[column_names[columncount]][0] == 'CHAR' and cfg['sql']['emptyToNull'] is False:
            # fwd mode, do nothing
            pass
        elif fieldmap[column_names[columncount]][0] == 'CHAR' and k == '':
            # empty string, but we still need to send it if the field is mandatory
            if column_names[columncount] in mlist:
                logging.info('found %s in mlist' % column_names[columncount])
            else:
                # do not send empty string on non mandatory field
                continue

        # handle exents
        try:
            ext = extentdict[column_names[columncount]]
            # it is an extent field if it makes it this far in the try , so break it up
            extentk = k.split(';')
            for val in extentk:
                if val == '':
                    continue
                if fieldmap[column_names[columncount]][0] in cfg['sql']['quotefields']:
                    kstring = kstring + "'" + str(val) + "',"
                else:
                    kstring = kstring + str(val) + ','
        except Exception as e:

            # need to use the fieldmap to work out whether to quote the string
            if fieldmap[column_names[columncount]][0] in cfg['sql']['quotefields']:
                kstring = kstring + "'" + str(k) + "',"
            else:
                '''
                # kstring = kstring + str(k) + ','

                if fieldmap[column_names[columncount]][0] == 'DECIMAL':
                    kstring = kstring + str(f'{k:f}') + ','
                else:
                    kstring = kstring + str(k) + ','
                '''
                if fieldmap[column_names[columncount]][0] == 'DECIMAL':
                    if 'e+' in str(k):
                        nqry = 'select cast(%s as char(%d)) from %s.CDC_%s WHERE CDC_%s."_Change-sequence" = %d' % (
                            curs.description[columncount][0],
                            curs.description[columncount][2],
                            owner, table, table, changeseq)
                        ncurs,nres = runquery(conn, ncurs, nqry)
                        for n in nres:
                            n = n[0].rstrip()
                            kstring = kstring + n + ','
                    else:
                        kstring = kstring + str(f'{k:f}') + ','
                else:
                    kstring = kstring + str(k) + ','

        logging.info('%s->%s->%s' % (
            column_names[columncount],
            fieldmap[column_names[columncount]][0], k))

    # strip last comma
    kstring = kstring[:-1]
    # add bracket
    kstring = kstring + ')'
    logging.info(kstring)

    sendKafkaProducer(cfg, changeseq, kstring, p, table)

    return


def pushdelete(changeseq, row, column_names, fieldmap, table, p, key):

    owner = cfg['oe']['owner']
    ncurs = conn.cursor()

    # convert key to list
    keylist = list(key)
    logging.info(keylist)
    # identifying field + offset
    key = int(keylist[1] + 8)

    kstring = 'DELETE FROM %s WHERE ' % table

    columncount = -1
    for k in row:

        columncount = columncount + 1
        if columncount < 9:
            continue

        if columncount == key:
            logging.info('%s->%s->%s-->%d' % (
                column_names[columncount],
                fieldmap[column_names[columncount]][0],
                k, columncount))
            kstring = kstring + column_names[columncount] + ' = '

            # need to use the fieldmap to work out whether to quote the string
            if fieldmap[column_names[columncount]][0] in cfg['sql']['quotefields']:
                kstring = kstring + "'" + str(k) + "',"
            else:
                if fieldmap[column_names[columncount]][0] == 'DECIMAL':
                    if 'e+' in str(k):
                        nqry = 'select cast(%s as char(%d)) from %s.CDC_%s WHERE CDC_%s."_Change-sequence" = %d' % (
                            curs.description[columncount][0],
                            curs.description[columncount][2],
                            owner, table, table, changeseq)
                        ncurs, nres = runquery(conn, ncurs, nqry)
                        for n in nres:
                            n = n[0].rstrip()
                            kstring = kstring + n + ','
                    else:
                        kstring = kstring + str(f'{k:f}') + ','
                else:
                    kstring = kstring + str(k) + ','
    # strip last comma
    kstring = kstring[:-1]

    logging.info(kstring)

    sendKafkaProducer(cfg, changeseq, kstring, p, table)

    return


def pushupdate(changeseq, row, column_names, fieldmap, table, p, key, extentdict, conn, curs):

    owner = cfg['oe']['owner']
    ncurs = conn.cursor()

    # convert key to list
    keylist = list(key)
    logging.info(keylist)
    # identifying field + offset
    key = int(keylist[1] + 8)

    kstring = 'UPDATE %s SET ' % table

    # first data field
    columncount = -1
    for k in row :
        columncount = columncount + 1
        # QAD fields start at 9
        if columncount < 9:
            continue

        if k is None:
            continue

        # skip empty strings
        if fieldmap[column_names[columncount]][0] == 'CHAR':
            if k == '':
                continue
        kstring = kstring + column_names[columncount] + ' = '
        logging.info('%s->%s->%s' % (
            column_names[columncount],
            fieldmap[column_names[columncount]][0],
            k))
        # need to use the fieldmap to work out whether to quote the string
        if fieldmap[column_names[columncount]][0] in cfg['sql']['quotefields']:
            kstring = kstring + "'" + str(k) + "',"
        else:
            if fieldmap[column_names[columncount]][0] == 'DECIMAL':
                if 'e+' in str(k):
                    nqry = 'select cast(%s as char(%d)) from %s.CDC_%s WHERE CDC_%s."_Change-sequence" = %d' % (
                        curs.description[columncount][0],
                        curs.description[columncount][2],
                        owner, table, table, changeseq)
                    ncurs, nres = runquery(conn, ncurs, nqry)
                    for n in nres:
                        n = n[0].rstrip()
                        kstring = kstring + n + ','
                else:
                    kstring = kstring + str(f'{k:f}') + ','
            else:
                kstring = kstring + str(k) + ','

    # strip last comma
    kstring = kstring[:-1]
    # add bracket
    kstring = kstring + ' WHERE '

    columncount = -1

    for k in row:

        columncount = columncount + 1
        if columncount < 9:
            continue

        if columncount == key:
            logging.info('%s->%s->%s-->%d' % (
                column_names[columncount],
                fieldmap[column_names[columncount]][0],
                k, columncount))
            kstring = kstring + column_names[columncount] + ' = '

            # need to use the fieldmap to work out whether to quote the string
            if fieldmap[column_names[columncount]][0] in cfg['sql']['quotefields']:
                kstring = kstring + "'" + str(k) + "',"
            else:
                if fieldmap[column_names[columncount]][0] == 'DECIMAL':
                    if 'e+' in str(k):
                        nqry = 'select cast(%s as char(%d)) from %s.CDC_%s WHERE CDC_%s."_Change-sequence" = %d' % (
                            curs.description[columncount][0],
                            curs.description[columncount][2],
                            owner, table, table, changeseq)
                        ncurs, nres = runquery(conn, ncurs, nqry)
                        for n in nres:
                            n = n[0].rstrip()
                            kstring = kstring + n + ','
                    else:
                        kstring = kstring + str(f'{k:f}') + ','
                else:
                    kstring = kstring + str(k) + ','
    # strip last comma
    kstring = kstring[:-1]
    logging.info(kstring)

    sendKafkaProducer(cfg, changeseq, kstring, p, table)

    return


def connectKafkaProducer(cfg):

    try:
        kafka_server = cfg['kafka']['server']
    except Exception as e:
        logging.error('No [kakfa][server] in cfg file.  Exiting - %s' % e)
        sys.exit(2)

    try:
        kafka_port = cfg['kafka']['port']
    except Exception as e:
        logging.error('No [kafka][port] in cfg file.  Exiting - %s' % e)
        sys.exit(2)

    try:
        send_topic = cfg['kafka']['sendtopic']
    except Exception as e:
        logging.error('No kafka_topic in cfg file.  Exiting - %s' % e)
        sys.exit(2)

    # producer
    try:
        p = Producer({'bootstrap.servers': kafka_server})
    except confluent_kafka.KafkaError as e:
        logging.error(e)
        logging.error('Exiting')
        sys.exit(2)

    logging.info('Connected to %s' % kafka_server)
    return p


def sendKafkaProducer(cfg, changeseq, msg, p, table):

    hdict = {}

    # create headers
    hdict['id'] = str(uuid.uuid4())
    hdict['source'] = cfg['kafka']['headers']['source']
    hdict['specversion'] = str(cfg['kafka']['headers']['specversion'])
    hdict['type'] = cfg['kafka']['headers']['type']
    hdict['datacontenttype'] = cfg['kafka']['headers']['datacontenttype']
    hdict['time'] = str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    hdict['qadsrcdb'] = cfg['oe']['db']
    hdict['qadsnkdb'] = cfg['kafka']['headers']['qadsnkdb']
    hdict['qadenvtype'] = cfg['kafka']['headers']['qadenvtype']
    hdict['qadsequence'] = str(changeseq)
    hdict['host'] = hostname.split('.')[0]
    hdict['table'] = table

    try:
        logging.info('Producing %s' % msg)
        # p.produce( pubtopic, value=bytes(str(msg).encode()),
        # key=casskey, headers=hdict, callback=delivery_report)
        p.produce(cfg['kafka']['sendtopic'],
                  value=bytes(str(msg).encode()),
                  key='',
                  headers=hdict)
        # p.flush()
    except Exception as e:
        logging.error('Failed sending from Kafka - %s' % e)
        return False

    return True


if __name__ == '__main__':

    signal.signal(signal.SIGTERM, signal_term_handler)
    signal.signal(signal.SIGINT, signal_term_handler)
    signal.signal(signal.SIGSEGV, signal_term_handler)
    signal.signal(signal.SIGHUP, signal_term_handler)
    signal.signal(signal.SIGQUIT, signal_term_handler)

    cfg = _get_config(args.cfg)

    loglevel = cfg['log']['defaultlevel']
    logfile = cfg['log']['logfile']
    extents = cfg['oe']['extent_fields'].split(',')
    for line in extents:
        extentdict[line.split(';')[0]] = int(line.split(';')[1])

    # command override?
    if args.loglevel:
        loglevel = args.loglevel

    if loglevel == 'INFO':
        logging.basicConfig(
            filename=logfile,
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s')
    elif loglevel == 'WARNING':
        logging.basicConfig(
            filename=logfile,
            level=logging.WARNING,
            format='%(asctime)s [%(levelname)s] %(message)s')
    elif loglevel == 'ERROR':
        logging.basicConfig(
            filename=logfile,
            level=logging.ERROR,
            format='%(asctime)s [%(levelname)s] %(message)s')
    else:
        print('Cannot determine loglevel, setting to ERROR')
        logging.basicConfig(
            filename=logfile,
            level=logging.ERROR,
            format='%(asctime)s [%(levelname)s] %(message)s')

    print('Logfile is %s as specified in %s ( log: <CR>  logfile )' % (logfile, args.cfg))
    logging.info('Extract Begin')

    # Connect to the OE source
    conn = connoe(hostname,
                  cfg['oe']['service'],
                  cfg['oe']['db'],
                  cfg['oe']['dlc'],
                  cfg['oe']['user'],
                  cfg['oe']['pass'])

    try:
        if not curs:
            curs = conn.cursor()
    except Exception as e:
        curs = conn.cursor()
        logging.info('connected to cursor - %s' % e)

    # Test
    qry = 'Select cast(oid_dom_mstr as char(30)) from PUB.dom_mstr'
    curs, result = runquery(conn, curs, qry )
    if result is not False:
        displayresult(result)

    # Connect to Kafka Producer topic
    p = connectKafkaProducer(cfg)

    # get _file records and store in orderedDict which for each table also has a sequence number.  
    tables, seq = gettables(conn, curs, tables)
    if tables is False:
        logging.error('ERROR : Cannot retrieve table list from %s.  Exiting' % db)
        curs.close()
        sys.exit(2)

    #  get sequence starting values
    logging.info('getting sequence starting values from cdc_det')
    curs, seq = getsequences(conn, curs, seq)

    # now the main loop
    # we need to set this to run forever
    while True:
        for table, tn in tables.items():
            # print (table)
            # get tracking changes

            if table in cfg['oe']['exclude_tables']:
                logging.warning('WARNING TABLE IN EXCLUDE LIST %s' % table)
                continue

            if table in cfg['oe']['large_clob_tables']:
                logging.warning('WARNING TABLE IN CLOB LIST %s' % table)
                continue

            if len(table) > cfg['oe']['max_table_length']:
                logging.error('TABLE NAME %s too long' % table)
                continue

            seq, keys = trackchanges(conn, curs, seq, table, tn, keys, p, extentdict)
        logging.info('Sleeping %d seconds' % cfg['poller']['sleeptime'])
        time.sleep(cfg['poller']['sleeptime'])
        usage = resource.getrusage(resource.RUSAGE_SELF)
        for name, desc in [('ru_utime', 'User time'),]:
            logging.info('%-25s (%-10s) = %s' % (desc, name, getattr(usage, name)))

    sys.exit(0)
