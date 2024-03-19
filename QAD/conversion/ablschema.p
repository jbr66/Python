OUTPUT TO #PATH#/#TABLE#.dat. 
FOR FIRST _file NO-LOCK WHERE _file-name = "#TABLE#".  
/* put the FWD recid field*/
put unformatted _file._file-name ";#FWD#" SKIP.
for each _field where _field._file-recid = recid(_file) no-lock BY _field._order : 
put unformatted _file._file-name ";"  _field._field-name ";"  _field._data-type ";" _field._format ";" _field._extent ";" _field._initial ";" _field._mandatory ";" _field._width SKIP. END. END.
 OUTPUT CLOSE.
