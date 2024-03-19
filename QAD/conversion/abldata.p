OUTPUT TO #PATH#/#TABLE#.dump. 

ASSIGN SESSION:DATE-FORMAT = "ymd".  DEFINE VARIABLE vWHTable AS WIDGET-HANDLE      NO-UNDO.
DEFINE VARIABLE ri AS ROWID NO-UNDO.
CREATE BUFFER vWHTable FOR TABLE "#TABLE#".

/* lob */
DEFINE variable fn as character no-undo.


FIND FIRST #TABLE# NO-LOCK NO-ERROR.
IF NOT AVAILABLE #TABLE#
THEN DO:
   OUTPUT CLOSE.
   QUIT.
END.

vWHTable:FIND-FIRST().

DEFINE VARIABLE i AS INTEGER     NO-UNDO.
DEFINE VARIABLE j as INTEGER NO-UNDO.
define variable k as integer no-undo.
DEFINE VARIABLE b AS CHARACTER NO-UNDO.
define variable n as integer no-undo.
define variable c as character no-undo.

define variable s as character no-undo.
define variable x as character no-undo.


define variable newx as character no-undo.
define variable gcounter as int64 init 1.
define variable myUUID as RAW NO-UNDO.
define variable charkey as character no-undo.
define variable Base64UUID as CHARACTER NO-UNDO.
define variable clobtables as character NO-UNDO INITIAL "#LARGECLOB#".


define variable lcVariable as longchar no-undo.

/* first line are the fields so downstream programs can match the field names and order */
put unformatted "#FWD_INDEX_KEY#^".

DO i = 1 TO vwhtable:NUM-FIELDS:
   /* handle extent fields */
   if vWHTable:BUFFER-FIELD(i):EXTENT > 0 then do:
      /* qad_charfld1 FWD hack */
      if vwhtable:BUFFER-FIELD(i):NAME = "qad_charfld1" then 
         put unformatted "qad_charfld111^qad_charfld122^qad_charfld133^qad_charfld144^qad_charfld155^qad_charfld16^qad_charfld17^qad_charfld18^qad_charfld19^qad_charfld110^qad_charfld1116^qad_charfld112^qad_charfld113^qad_charfld114^qad_charfld115^".
      else 
      do j = 1 to vWHTable:BUFFER-FIELD(i):EXTENT :
         put unformatted vwhtable:BUFFER-FIELD(i):NAME + string(j) + "^".
      end.   
   end.
   else do :
      /* normal fields */
      put unformatted vwhtable:BUFFER-FIELD(i):NAME + "^".
      /* add additional offset field for datetime timezone offset */
      if vWHTable:BUFFER-FIELD(i):data-type = "datetime-tz" then put unformatted vwhtable:BUFFER-FIELD(i):NAME + "#OFFSET#^".
   end.
END.
put skip.

/* define a query to extract the data */
DEFINE VARIABLE hQuery AS HANDLE NO-UNDO.
CREATE QUERY hQuery.
hQuery:SET-BUFFERS((BUFFER #TABLE#:HANDLE)).  /* associate the dynamic query with the static buffer */
hQuery:QUERY-PREPARE("FOR EACH #TABLE# NO-LOCK").
hQuery:QUERY-OPEN().
hQuery:GET-FIRST().

DO WHILE hQuery:QUERY-OFF-END = FALSE:
   s = "".
   /* EXPORT #TABLE#.  */
   ri = ROWID(#TABLE#).
   
   vWHTable:FIND-By-ROWID(ri).
   charkey = string(gcounter).
   gcounter = gcounter + 1.
   

   DO i = 1 TO vWHTable:NUM-FIELDS:

      /* extents */
      if vWHTable:BUFFER-FIELD(i):EXTENT > 0 then do:
           
           do j = 1 to vWHTable:BUFFER-FIELD(i):EXTENT :
              if vWHTable:BUFFER-FIELD(i):BUFFEr-VALUE(j) <> ? then do:
                 if vWHTable:BUFFER-FIELD(i):data-type = "date" then
                    s = s +  string(ISO-DATE(vWHTable:BUFFER-FIELD(i):BUFFEr-VALUE(j))).
                 else do :
                   /* logicals must be 1 or 0 */
                   if vWHTable:BUFFER-FIELD(i):data-type = "logical" then do:
                      if vWHTable:BUFFER-FIELD(i):BUFFER-VALUE = yes then s = s + "1". else s = s + "0".
                   end.                 
                   s = s + string(vWHTable:BUFFER-FIELD(i):BUFFEr-VALUE(j)).
                 end.
              end.
              s = s +  "^".
           end.

      end.
      else do:
         /* non extent fields */
         
         x = "".
         if vWHTable:BUFFER-FIELD(i):BUFFEr-VALUE = ? or vWHTable:BUFFER-FIELD(i):data-type = "raw" or vWHTable:BUFFER-FIELD(i):data-type = "blob" then x = "".
         else if vWHTable:BUFFER-FIELD(i):data-type = "date" or vWHTable:BUFFER-FIELD(i):data-type = "datetime" or vWHTable:BUFFER-FIELD(i):data-type = "timestamp" or vWHTable:BUFFER-FIELD(i):data-type = "datetime-tz" then do:
           x = string(ISO-DATE(vWHTable:BUFFER-FIELD(i):BUFFER-VALUE)).
           if vWHTable:BUFFER-FIELD(i):data-type = "datetime-tz" then x = x + "^" + string(timezone).
         end.  
         else do:
             if lookup("#TABLE#", clobtables) > 0 and vWHTable:BUFFER-FIELD(i):data-type = "clob" then do:
                
               
                fn = "#PATH#/#TABLE#_" + vwhtable:BUFFER-FIELD(i):NAME + "_" + charkey + ".clob". 
                x = fn.

                copy-lob from vWHTable:BUFFER-FIELD(i):BUFFER-VALUE to file fn. 
                              
                
             end.
             else do:
                /* logicals must be 1 or 0 */
                if vWHTable:BUFFER-FIELD(i):data-type = "logical" then do:
                   if vWHTable:BUFFER-FIELD(i):BUFFER-VALUE = yes then x = "1". else x = "0".
                end.
                else do:
                   /* fix oid - remove left ten characters and leading zeroes */
                   if vwhtable:BUFFER-FIELD(i):NAME BEGINS "oid_" then do :
                       if length(vWHTable:BUFFER-FIELD(i):BUFFER-VALUE) > 15 then do:
                          x = vWHTable:BUFFER-FIELD(i):BUFFER-VALUE.
                          SUBSTRING(x,1,8) = "00000000".
                          x = LEFT-TRIM(x,"0").
                       end.
                       else do:  x = vWHTable:BUFFER-FIELD(i):BUFFER-VALUE.  end.
                   end.
                   else do : x = vWHTable:BUFFER-FIELD(i):BUFFER-VALUE.
                   end.
                end.
             end.
         end.
         
         if length(x) > 0 then do:
            /* remove newline and carriage return */
            x = replace(x,CHR(13),"").
            x = replace(x,CHR(10),"").
            /* field delimiter */
            s = s +  x + "^".
         end. 
         else  s = s + "^".

      end.
     
   END.
   
   /* remove last ^ */
   s = substring(s,1,length(s) - 1).

   /* this prints the row */
   if substring(s,1,1) <> "?" then do:
      /* just put a zero for recid - this will be handled on the insert side of things */
       put unformatted  "0^"  s skip.   

   end.

   hQuery:GET-NEXT().
END.
DELETE WIDGET vWHTable.
OUTPUT CLOSE.
