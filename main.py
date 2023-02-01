import argparse

from classes.Processor import Processor

# TODO: Support comments
# TODO: Support immediates in other representations

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", help="file to run", default="tests/files/gen_test.s"
    )
    parser.add_argument("-reg", help="print register values", action="store_true")
    parser.add_argument("-mem", help="print data memory values", action="store_true")
    args = parser.parse_args()

    cpu = Processor()
    cpu.run(args.file)
    if args.reg:
        cpu.print_registers()
    if args.mem:
        cpu.print_data_memory()
