from classes.Processor import Processor

# TODO: Accept format with parenthesis
# TODO: Communication between Datapath and Control Unit
# TODO: Update Datapath to properly change signals in different operations
# TODO: Dealing with numbers as bytes
# TODO: Support comments
# TODO: Support immediates in other representations
# TODO: Check if negative number affects the functionality (-1 is being represented as 0x-0000001 not 0xFFFFFFFF)

if __name__ == '__main__':
    cpu = Processor()
    cpu.run('tests/files/test_loads_stores.s')

