; **** FILE INFORMATION ************************************************************************************************
;       File:     Implementation of multiplication (8-bit) in assembly
;       Website:  https://brookshear.jfagerberg.me/#
;       Date:     19-09-2020
;       Author:   Kian Banke Larsen
; **** CODE ************************************************************************************************************
211F    ;Copy bit-string 03 to register 1                                 MULTIPLICATOR;
2204    ;Copy bit-string 05 to register 2                                 MULTIPLIER;
2301    ;Copy bit-string 01 to register 3                                 CONSTANT == 1;
2400    ;Copy bit-string 00 to register 4                                 SUM;
25FE    ;Copy bit-string FE to register 5                                 CONSTANT == 11111110;
8023    ;Bitwise AND bits in registers 2 and 3, put in register 0         CHECKS LEAST SIGNIFICANT BIT;
D310    ;Jump to cell 16 if register 3 is greater than register 0         CONTINUES IF LEAST SIGNIFICANT BIT IS FLAGGED;
5414    ;Add bits in registers 1 and 4 (two's-complement), put in 4       ADDS MULTIPLICATOR AND SUM;
A107    ;Rotate bits in register 1 cyclically right 7 steps               ROTATE MULTIPLICATOR 1 TO THE LEFT;
A201    ;Rotate bits in register 2 cyclically right 1 steps               ROTATE MULTIPLIER 1 TO THE RIGHT;
8115    ;Bitwise AND bits in registers 1 and 5, put in register 1         THROWS DUPLICATED BIT AFTER ROT;
5F3F    ;Add bits in registers 3 and F (two's-complement), put in F       COUNT OF ROTATION;
2008    ;Copy bit-string 08 to register 0                                 PUTS 8 IN REGISTER F;
BF22    ;Jump to cell 2C if register F equals register 0                  IF ROTATED 8 TIMES CALL STOPCODE;
8023    ;Bitwise AND bits in registers 2 and 3, put in register 0         CHECKS LEAST SIGNIFICANT BIT;
B30E    ;Jump to cell 0C if register 3 equals register 0                  IF ROTATED 8 TIMES CALL STOPCODE;
DF10    ;Jump to cell 16 if register F is greater than register 0         USE THE FORCE TO RIGHT FLIP EM BITS;
C000    ;Halt                                                             STOPCODE;
