addi x8, x9, -12
sltu x3, x5, x6
jal x1, address
lb x10, 24(x11)
sw x2, 40(x3)
xor x7, x8, x9
bne x1, x2, label
lui, x5, 65535
srl x2, x3, 5
slli x6, x7, 2