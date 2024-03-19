/* FWD overrides the primary index , so ingore p on vIdxflags here */
OUTPUT TO #PATH#/#TABLE#.idx. 
DEFINE VARIABLE vIdxflags    AS CHARACTER          NO-UNDO. 
/* add FWD primary */
put unformatted "#FWD_INDEX_NAME#,1,p,#FWD_INDEX_KEY#" skip.
FOR FIRST _file NO-LOCK WHERE _file-name = "#TABLE#": 
for each _index of _file, each _index-field OF _index NO-LOCK: 
FIND _field OF _index-field NO-ERROR.  IF AVAILABLE (_field) THEN  ASSIGN vIdxflags = (IF _Index._Unique       THEN "u" ELSE "")   + (IF _Index._Wordidx EQ 1 THEN "w" ELSE "").  put unformatted _index-name "," _index-seq "," vIdxflags "," _field-name skip. end. 
release _file. end. 
OUTPUT CLOSE.
