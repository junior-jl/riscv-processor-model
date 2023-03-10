import argparse
import re

from classes.Processor import Processor

import PySimpleGUI as sg

from utils.get_instructions_asm_file import get_instructions_asm_file


def interface():
    sg.theme("DarkGrey14")

    layout = [
        [sg.Text("RV32I Processor Model", font="Any 15")],
        [
            sg.Text("Assembly File"),
            sg.Input(
                key="-sourcefile-",
                size=(45, 1),
                tooltip="Insert the file with the Assembly instructions.",
            ),
            sg.FileBrowse(file_types=(("Assembly Files", "*.s"),)),
        ],
        [
            sg.Text("Binary File"),
            sg.Input(
                key="-sourcefilebin-",
                size=(45, 1),
                tooltip="Insert the file with the Machine Code instructions.",
            ),
            sg.FileBrowse(file_types=(("Binary Files", "*"),)),
        ],
        [
            sg.Checkbox(
                "Print Memory",
                key="-mem-",
                tooltip="Check if you want to print the contents on the data memory.",
            ),
            sg.Checkbox(
                "Print Registers",
                key="-reg-",
                tooltip="Check if you want to print the contents on the register files.",
            ),
        ],
        [
            sg.Text("Specify registers: "),
            sg.Input(
                key="-registers-",
                tooltip="Insert the registers you want to print separated by commas.",
            ),
            sg.Text("Memory addresses: "),
            sg.Input(
                key="-addresses-",
                tooltip="Insert the registers you want to print separated by commas.",
            ),
        ],
        [
            sg.Frame(
                "Output",
                font="Any 15",
                layout=[[sg.Output(size=(65, 15), font="Courier 10")]],
            )
        ],
        [
            sg.Button("Run", bind_return_key=True),
            sg.Button("Quit", button_color=("white", "firebrick3")),
        ],
    ]

    window = sg.Window(
        "RV32I Processor Model",
        layout,
        auto_size_text=False,
        auto_size_buttons=False,
        default_element_size=(20, 1),
        text_justification="right",
    )
    # ---===--- Loop taking in user input --- #
    while True:
        event, values = window.read()
        if event in ("Quit", sg.WIN_CLOSED):
            window.close()
            break
        registers_to_print = [
            int(i[1:]) if i.startswith('x') else int(i) for i in re.split("[ ,]", values["-registers-"]) if i
        ]
        addresses_to_print = [
            int(i, 16) if i.startswith('0x') else int(i) for i in re.split("[ ,]", values["-addresses-"]) if i
        ]
        source_file = values["-sourcefile-"] if values["-sourcefile-"] else values["-sourcefilebin-"]
        cpu = Processor()

        if event == "Run":
            invalid_regs = [x for x in registers_to_print if x < 0 or x > 31]
            if invalid_regs:
                sg.Popup(f"Invalid register(s): {invalid_regs}")
                registers_to_print = [item for item in registers_to_print if item not in invalid_regs]
            invalid_addr = [y for y in addresses_to_print if y < 0 or y >= (cpu.datapath.data_mem.words * 4)]
            if invalid_addr:
                sg.Popup(f"Invalid address(es): {invalid_addr}")
                addresses_to_print = [item for item in addresses_to_print if item not in invalid_addr]
            if not source_file:
                sg.Popup("No Assembly or Binary file added! Please choose a file.")
            else:
                print(source_file)
                print("*------------------*")
                print("Instructions")
                instructions = get_instructions_asm_file(source_file)
                print("*------------------*")
                for i in range(len(instructions)):
                    print(f"{i}: {instructions[i]}") if values["-sourcefile-"] else \
                        print("{}: 0x{:08X}".format(i, int(instructions[i])))
                cpu.run(source_file)
                if values["-reg-"]:
                    print("*------------------*")
                    print("Register Files")
                    print("*------------------*")
                    cpu.print_registers()
                    print("*------------------*")
                if values["-mem-"]:
                    print("*------------------*")
                    print("Data Memory")
                    print("*------------------*")
                    cpu.print_data_memory()
                    print("*------------------*")
                if registers_to_print:
                    list(map(cpu.print_reg, registers_to_print))
                if addresses_to_print:
                    list(map(cpu.print_data_address, addresses_to_print))
            window.refresh()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", help="file to run", default="tests/files/gen_test.s"
    )
    parser.add_argument("-r", help="print specified register value", type=int)
    parser.add_argument(
        "-d", help="print value on specified data memory address", type=int
    )
    parser.add_argument("-reg", help="print register values", action="store_true")
    parser.add_argument("-mem", help="print data memory values", action="store_true")
    parser.add_argument("-inst", help="print instruction memory values", action="store_true")
    parser.add_argument("-gui", help="open simple GUI", action="store_true")
    args = parser.parse_args()
    if not args.gui:
        cpu = Processor()
        cpu.run(args.file)
        if args.r:
            cpu.print_reg(args.r)
        if args.d:
            cpu.print_data_address(args.d)
        if args.reg:
            cpu.print_registers()
        if args.mem:
            cpu.print_data_memory()
        if args.inst:
            cpu.print_instructions()
    else:
        interface()
