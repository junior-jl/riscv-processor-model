addi x1, x9, -55
add x2, x1, x0
sw x2, x3, 40
lui, x5, 65535
bne x1, x2, -50
jal x1, -500
sltu x3, x5, x6
xor x7, x8, x9
bne x1, x2, 0
lui, x5, 65535
srl x2, x3, x5
slli x6, x7, 2