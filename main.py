from classes.Processor import Processor

# TODO: Support comments
# TODO: Support immediates in other representations

if __name__ == '__main__':
    cpu = Processor()
    cpu.run('tests/files/gen_test.s')

