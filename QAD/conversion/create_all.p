/*
define variable tableList as character initial "ad_mstr,cm_mstr,so_mstr" no-undo.
*/

define variable x as integer no-undo.
define variable y as integer no-undo.
define variable z as integer no-undo.
DEFINE VARIABLE cFields AS CHARACTER NO-UNDO.


output to "/tmp/cdc.p".

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
put unformatted 'service = new DataAdminService("qaddb"). ' skip(2).

x = 0.
y = 0.
z = 0.
repeat x = 1 to num-entries(tableList):

for each qaddb._file where _file-name = entry(x,tableList):

cFields = "".

FIND FIRST qaddb._index WHERE RECID(_index) EQ qaddb._file._prime-index.
FOR EACH qaddb._index-field WHERE _index-field._index-recid EQ RECID(_index):


FIND qaddb._field WHERE RECID(_field) EQ _index-field._field-recid.
cFields = cFields + (IF (cFields GT "") EQ TRUE THEN "," ELSE "") +_field._field-name.


END.

put unformatted
'cdcTablePolicy = service:NewCdcTablePolicy("' + _file-name + '").' skip(1).


put unformatted


'assign ' skip
' cdcTablePolicy:Description = ""' skip
' cdcTablePolicy:State = CdcTablePolicyStateEnum:Active ' skip
' cdcTablePolicy:ChangeTable = "CDC-' + _file-name + '" ' skip
' cdcTablePolicy:ChangeTableOwner = "" ' skip
' cdcTablePolicy:EncryptPolicy = no ' skip
' cdcTablePolicy:IdentifyingField = yes ' skip
' cdcTablePolicy:Level = CdcTablePolicyLevelEnum:Medium ' skip
' cdcTablePolicy:DataArea = service:GetArea("CDC") ' skip
' cdcTablePolicy:IndexArea = service:GetArea("CDC_IDX") ' skip
' cdcTablePolicy:Table = service:GetTable("' + _file-name + '","PUB"). ' skip(2).

y = 1.

for each qaddb._field of _file:


put unformatted 'cdcFieldPolicy = service:NewCdcFieldPolicy(). ' skip
'assign' skip

' cdcFieldPolicy:Field = cdcTablePolicy:Table:Fields:Find("' + _field._field-name + '")' skip.

if not can-do(cFields,_field-name) then
if _field._field-name = "oid_" + _file-name then do:


put unformatted ' cdcFieldPolicy:IdentifyingField = 1.' skip.


end.
else


put unformatted ' cdcFieldPolicy:IdentifyingField = ?.' skip.


else do:


y = lookup(_field._field-name,cFields) + 1.
put unformatted ' cdcFieldPolicy:IdentifyingField = ' + string(y) + '.' skip(2).


end.
put unformatted 'cdcTablePolicy:FieldPolicies:Add(cdcFieldPolicy). ' skip(3).


end. /* EACH _FIELD */

put unformatted 'service:CreateCdcTablePolicy(cdcTablePolicy).' skip.


end. /* EACH TABLE */


end. /* NUM-ENTRIES */

put unformatted
' ' skip
'finally: ' skip
' delete object service no-error.' skip
'end finally.' skip.