# RISCV Single Cycle Processor model - RV32I

## Steps of a cycle

1. Instruction Fetch
2. Instruction Decode
3. Execute
4. Memory
5. Write Back

### Minor features

- [x] Support for instructions with or without commas
- [x] Support for register API names
- [x] Support for parenthesis notation, e.g. `sw x3, 0(x4)` instead of `sw x3, x4, 0`
- [ ] Support for other representations of immediates (hex, bin)
- [ ] Support for comments
- [ ] Support for pseudo-instructions
- [ ] Support for labels
- [ ] CLI execution and flags
- [ ] Simple GUI

### Current Status of Instructions

| **R Type**                               | **mnemonic** |     |     |       | **STATUS** | **NOTE**                              |
|------------------------------------------|--------------|-----|-----|-------|------------|---------------------------------------|
| ADD                                      | add          | rd  | rs1 | rs2   | OK         |                                       |
| AND                                      | and          | rd  | rs1 | rs2   | OK         |                                       |
| OR                                       | or           | rd  | rs1 | rs2   | OK         |                                       |
| SET IF LESS THAN                         | slt          | rd  | rs1 | rs2   | OK         |                                       |
| SET IF LESS THAN UNSIGNED                | sltu         | rd  | rs1 | rs2   | OK         |                                       |
| SHIFT LEFT                               | sll          | rd  | rs1 | rs2   | OK         |                                       |
| SHIFT RIGHT                              | srl          | rd  | rs1 | rs2   | OK         |                                       |
| SHIFT RIGHT ARITHMETIC                   | sra          | rd  | rs1 | rs2   | OK         |                                       |
| SUBTRACT                                 | sub          | rd  | rs1 | rs2   | OK         | NEGATIVE NUMBERS WORKING PROPERLY NOW |
| XOR                                      | xor          | rd  | rs1 | rs2   | OK         |                                       |
| **I Type**                               |              |     |     |       |            |                                       |
| ADD IMMEDIATE                            | addi         | rd  | rs1 | imm   | OK         |                                       |
| AND IMMEDIATE                            | andi         | rd  | rs1 | imm   | OK         |                                       |
| JUMP AND LINK REGISTER                   | jalr         | rd  | rs1 | imm   | OK         |                                       |
| LOAD BYTE                                | lb           | rd  | rs1 | imm   | OK         |                                       |
| LOAD BYTE UNSIGNED                       | lbu          | rd  | rs1 | imm   | OK         |                                       |
| LOAD HALF UNSIGNED                       | lhu          | rd  | rs1 | imm   | OK         |                                       |
| LOAD HALFWORD                            | lh           | rd  | rs1 | imm   | OK         |                                       |
| LOAD WORD                                | lw           | rd  | rs1 | imm   | OK         |                                       |
| OR IMMEDIATE                             | ori          | rd  | rs1 | imm   | OK         |                                       |
| SET IF LESS THAN IMM                     | slti         | rd  | rs1 | imm   | OK         |                                       |
| SET IF LESS THAN IMM UNS                 | sltiu        | rd  | rs1 | imm   | OK         |                                       |
| SHIFT LEFT IMMEDIATE                     | slli         | rd  | rs1 | shamt | OK         |                                       |
| SHIFT RIGHT ARITH IMM                    | srai         | rd  | rs1 | shamt | OK         |                                       |
| SHIFT RIGHT IMMEDIATE                    | srli         | rd  | rs1 | shamt | OK         |                                       |
| XOR IMMEDIATE                            | xori         | rd  | rs1 | imm   | OK         |                                       |
| **S Type**                               |              |     |     |       |            |                                       |
| STORE BYTE                               | sb           | rs1 | rs2 | imm   | OK         |                                       |
| STORE HALFWORD                           | sh           | rs1 | rs2 | imm   | OK         |                                       |
| STORE WORD                               | sw           | rs1 | rs2 | imm   | OK         |                                       |
| **U Type**                               |              |     |     |       |            |                                       |
| ADD UPPER IMM TO PC                      | auipc        | rd  | imm |       | OK         |                                       |
| LOAD UPPER IMMEDIATE                     | lui          | rd  | imm |       | OK         |                                       |
| **SB Type**                              |              |     |     |       |            |                                       |
| BRANCH IF EQUAL                          | beq          | rs1 | rs2 | imm   | OK         |                                       |
| BRANCH IF GREATER OR EQUAL THAN          | bge          | rs1 | rs2 | imm   | OK         |                                       |
| BRANCH IF GREATER OR EQUAL THAN UNSIGNED | bgeu         | rs1 | rs2 | imm   | OK         |                                       |
| BRANCH IF LESS THAN                      | blt          | rs1 | rs2 | imm   | OK         |                                       |
| BRANCH IF LESS THAN UNSIGNED             | bltu         | rs1 | rs2 | imm   | OK         |                                       |
| BRANCH IF NOT EQUAL                      | bne          | rs1 | rs2 | imm   | OK         |                                       |
| **UJ Type**                              |              |     |     |       |            |                                       |
| JUMP AND LINK                            | jal          | rd  | imm |       | OK         |                                       |

### Diagram of the processor

![](D:\GitHub\riscv-processor-model\utils\diagram.png)

### Problems

- [x] Negative sums and subs
- [x] Negative jumps