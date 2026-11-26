// Capstone Project - Part C
// K = 56
// Start row: K = 56 -> SCREEN (16384) + 32 * 56 = 18176
// Height: 20 rows (rows 56 to 75)
// Width: 16 * ((56 mod 4) + 1) = 16 * (0 + 1) = 16 pixels (1 word from left edge)

(LOOP)
    @KBD
    D=M
    @DRAW
    D;JNE           // Any key pressed -> draw black (-1)

    @color
    M=0             // No key pressed -> clear white (0)
    @START_BOX
    0;JMP

(DRAW)
    @color
    M=-1

(START_BOX)
    @18176          // Row 56, word 0: 16384 + 32 * 56 = 18176
    D=A
    @addr
    M=D

    @20             // Height = 20 rows
    D=A
    @count
    M=D

(ROW_LOOP)
    @color
    D=M
    @addr
    A=M
    M=D             // Write 16-pixel word (1 word wide)

    @addr
    D=M
    @32             // Next row = current address + 32 words
    D=D+A
    @addr
    M=D

    @count
    MD=M-1
    @ROW_LOOP
    D;JGT

    @LOOP
    0;JMP
