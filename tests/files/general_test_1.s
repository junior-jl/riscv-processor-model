addi x10, x0, 1
addi x20, x0, 2
jal x15, 28
beq x10, x20, 8
addi x3, x0, 10
bne x10, x20, 8
addi x4, x0, 20
blt x10, x20, 8
addi x5, x0, 30
bge x10, x20, 8
addi x6, x0, 40
bltu x10, x20, 8
addi x7, x0, 50
bgeu x0, x20, 8
addi x8, x0, 60
