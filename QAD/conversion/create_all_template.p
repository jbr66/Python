/*
**  Create CDC for all tables and all fields
**  Writes temporary files to /tmp/CDC_[tablename].p
**  You will need to run those files separately through a higher level driver program
*/

DEFINE VARIABLE x as INTEGER NO-UNDO.
DEFINE VARIABLE y as INTEGER NO-UNDO.
DEFINE VARIABLE z as INTEGER NO-UNDO.
DEFINE VARIABLE cFields AS CHARACTER NO-UNDO.
DEFINE VARIABLE fn as CHARACTER NO-UNDO.
DEFINE VARIABLE foundOID as INTEGER NO-UNDO.
DEFINE VARIABLE OID as CHARACTER NO-UNDO.

y = 0.


for each _file NO-LOCK where _file-num > 0 and _file-num < 32000 :

   ASSIGN fn = '#TMPDIR#/#SERVICENAME#CDC_' + _file._file-name + '.p'.
   OUTPUT TO value(fn).

   put unformatted 'using Progress.Lang.Error.' skip.
   put unformatted 'using OpenEdge.DataAdmin.DataAdminService.' skip.
   put unformatted 'using OpenEdge.DataAdmin.Error.DataAdminErrorHandler.' skip.
   put unformatted 'using OpenEdge.DataAdmin.ICdcTablePolicy.' skip.
   put unformatted 'using OpenEdge.DataAdmin.ICdcFieldPolicy.' skip.
   put unformatted 'using OpenEdge.DataAdmin.CdcTablePolicyStateEnum.' skip.
   put unformatted 'using OpenEdge.DataAdmin.CdcTablePolicyLevelEnum.' skip.
   put unformatted ' ' skip.
   put unformatted 'define variable service as DataAdminService no-undo.' skip.
   put unformatted 'define variable cdcTablePolicy as ICdcTablePolicy no-undo.' skip.
   put unformatted 'define variable cdcFieldPolicy as ICdcFieldPolicy no-undo.' skip. 
   put unformatted skip.
   put unformatted 'service = new DataAdminService("#SERVICENAME#"). ' skip(2).


   cFields = "".

   FIND FIRST _index NO-lOCK WHERE RECID(_index) EQ _file._prime-index.
   FOR EACH _index-field WHERE _index-field._index-recid EQ RECID(_index) NO-LOCK:

      FIND FIRST _field NO-LOCK WHERE RECID(_field) EQ _index-field._field-recid.
      cFields = cFields + (IF (cFields GT "") EQ TRUE THEN "," ELSE "") + _field._field-name.
      
   END.

   /* put unformatted cFields skip. */

   put unformatted
   'cdcTablePolicy = service:NewCdcTablePolicy("' + _file._file-name + '").' skip(1).

   put unformatted
   'assign ' skip
   ' cdcTablePolicy:Description = "' + _file._file-name + '"' skip
   ' cdcTablePolicy:State = CdcTablePolicyStateEnum:Active ' skip
   ' cdcTablePolicy:ChangeTableOwner = "#OWNER#" ' skip
   ' cdcTablePolicy:EncryptPolicy = NO ' skip
   ' cdcTablePolicy:IdentifyingField = YES ' skip
   ' cdcTablePolicy:Level = CdcTablePolicyLevelEnum:#LEVEL# ' skip
   ' cdcTablePolicy:DataArea = service:GetArea("#DATA#") ' skip
   ' cdcTablePolicy:IndexArea = service:GetArea("#INDEX#") ' skip
   ' cdcTablePolicy:Table = service:GetTable("' + _file._file-name + '","PUB"). ' skip(2).

   y = 1.

   foundOID = 0.
   OID = 'oid_' + _file._file-name.
   
   FOR EACH _field of _file NO-LOCK:
      /* IF OID = _field._field-name THEN PUT UNFORMATTED "FOUND " + _field._field-name skip. */
      IF OID = _field._field-name THEN foundOID = 1.
   END.
   
   /* do legacy ERP first, ignore primary index and look for OID tracking */
   if foundOID = 1 THEN DO:
      FOR EACH _field of _file NO-LOCK:
          put unformatted 'cdcFieldPolicy = service:NewCdcFieldPolicy(). ' skip
          'assign' skip
          ' cdcFieldPolicy:Field = cdcTablePolicy:Table:Fields:Find("' + _field._field-name + '")' skip.
          IF _field._field-name = "oid_" + _file-name THEN put unformatted ' cdcFieldPolicy:IdentifyingField = 1.' skip.
          ELSE put unformatted ' cdcFieldPolicy:IdentifyingField = ?.' skip.
          put unformatted 'cdcTablePolicy:FieldPolicies:Add(cdcFieldPolicy). ' skip(3).
      END.
      
   END.
   ELSE DO :
      /* no OID field */
      FOR EACH _field of _file NO-LOCK:
          put unformatted 'cdcFieldPolicy = service:NewCdcFieldPolicy(). ' skip
          'assign' skip
          ' cdcFieldPolicy:Field = cdcTablePolicy:Table:Fields:Find("' + _field._field-name + '")' skip.
          if not can-do(cFields,_field-name) then put unformatted ' cdcFieldPolicy:IdentifyingField = ?.' skip.
          else DO:
             y = lookup(_field._field-name,cFields).
             put unformatted ' cdcFieldPolicy:IdentifyingField = ' + string(y) + '.' skip(2).
          END.
          put unformatted 'cdcTablePolicy:FieldPolicies:Add(cdcFieldPolicy). ' skip(3).   
      END.     
   END.   

 
   put unformatted 'service:CreateCdcTablePolicy(cdcTablePolicy).' skip.
   put unformatted ' ' skip
   'finally: ' skip
   ' delete object service no-error.' skip
   'end finally.' skip. 

   OUTPUT CLOSE.
   put unformatted fn skip.
 
end. /* EACH TABLE */

