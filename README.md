# RISCV Single Cycle Processor model - RV32I

## Usage

```bash
usage: main.py [-h] [-f FILE] [-reg] [-mem]

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  file to run
  -reg                  print register values
  -mem                  print data memory values
```

## Steps of a cycle

1. Instruction Fetch
2. Instruction Decode
3. Execute
4. Memory
5. Write Back

### Improvements and features

- [x] Support for instructions with or without commas
- [x] Support for register API names
- [x] Support for parenthesis notation, e.g. `sw x3, 0(x4)` instead of `sw x3, x4, 0`
- [x] Support for other representations of immediates (hex, bin)
- [x] Support for comments (Not with pseudoinstructions yet)
- [x] Support for pseudo-instructions (except `la`)
- [ ] Support for labels
- [ ] Support for 'pseudo' `jal` and `jalr`. Ex: `jal offset` -> `jal ra offset`
- [x] CLI execution and flags
- [ ] Simple GUI
- [ ] Make it a Python Package

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

### Current Status of Pseudoinstructions

| Instruction                 | **mnemonic** |        |        |     | **STATUS** | **NOTE** |
|-----------------------------|--------------|--------|--------|-----|------------|----------|
| NO OPERATION                | nop          |        |        |     | OK         |          |
| LOAD IMMEDIATE              | li           | rd     | imm    |     | OK         |          |
| COPY REGISTER               | mv           | rd     | rs     |     | OK         |          |
| ONE'S COMPLEMENT            | not          | rd     | rs     |     | OK         |          |
| TWO'S COMPLEMENT            | neg          | rd     | rs     |     | OK         |          |
| BRANCH IF EQUAL TO ZERO     | beqz         | rs     | offset |     | OK         |          |
| BRANCH IF NOT EQUAL TO ZERO | bnez         | rs     | offset |     | OK         |          |
| JUMP                        | j            | offset |        |     | OK         |          |
| JUMP REGISTER               | jr           | rs     |        |     | OK         |          |
| RETURN FROM SUBROUTINE      | ret          |        |        |     | OK         |          |
| LOAD ADDRESS                | la           | rd     | symbol |     | TODO       |          |

### Diagram of the processor

![diagram](https://user-images.githubusercontent.com/69206952/215910571-19ea05a2-a4a4-4091-8b83-9e2aad815697.png)

### Problems

- [x] Negative sums and subs
- [x] Negative jumps
- [ ] Comments on pseudoinstructions
- [ ] Tests not passing together when running `pytest` on terminal, but pass on Pycharm. Also, all tests pass individually.
