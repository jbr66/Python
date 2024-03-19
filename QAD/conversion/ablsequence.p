OUTPUT TO  #PATH#/#DBNAME#.sequences. DEFINE VARIABLE hBuffer        AS HANDLE      NO-UNDO.
DEFINE VARIABLE hQuery         AS HANDLE      NO-UNDO.
DEFINE VARIABLE cErrorMessage  AS CHARACTER   NO-UNDO.
DEFINE VARIABLE l_filename     AS CHARACTER   NO-UNDO.
DEFINE VARIABLE l_CurValue     AS INT64       NO-UNDO.
DEFINE VARIABLE l_max          AS INT64       NO-UNDO.
DEFINE VARIABLE l_min          AS INT64       NO-UNDO.
DEFINE VARIABLE iFilePointer   AS INT64       NO-UNDO.
DEFINE VARIABLE iCount         AS INTEGER     NO-UNDO.

    /* p2j_id_generator_sequence */
    put unformatted "999,#FWD_SEQUENCE#,1,1,99933720368547758" skip.


    CREATE BUFFER hBuffer FOR TABLE "_Sequence":U.
    CREATE QUERY hQuery.

    hQuery:SET-BUFFERS ( hBuffer ).
    hQuery:QUERY-PREPARE ( "FOR EACH _Sequence NO-LOCK" ).
    hQuery:QUERY-OPEN ( ).
    hQuery:GET-FIRST ( NO-LOCK ).
    REPEAT WHILE NOT hQuery:QUERY-OFF-END:

        ASSIGN l_CurValue = DYNAMIC-CURRENT-VALUE ( hBuffer:BUFFER-FIELD ( "_Seq-Name":U ):BUFFER-VALUE, "DICTDB" )
               iCount     = iCount + 1.
        if hBuffer:BUFFER-FIELD("_Seq-Max":U):BUFFER-VALUE = ? then l_max = 999999999999999999.
        else l_max =   hBuffer:BUFFER-FIELD("_Seq-Max":U):BUFFER-VALUE.
        if hBuffer:BUFFER-FIELD("_Seq-Min":U):BUFFER-VALUE = ? then l_min = 1.
        else l_min =   hBuffer:BUFFER-FIELD("_Seq-Min":U):BUFFER-VALUE.
        PUT UNFORMATTED hBuffer:BUFFER-FIELD("_Seq-Num":U):BUFFER-VALUE ","  hBuffer:BUFFER-FIELD ( "_Seq-Name":U ):BUFFER-VALUE "," l_CurValue "," l_min "," l_max skip.

        hQuery:GET-NEXT ( NO-LOCK ).
    END.  
OUTPUT CLOSE. 

