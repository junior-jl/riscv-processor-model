from classes.RegisterFiles import RegisterFiles

def test_register_files():
    # Create an instance of RegisterFiles with 10 registers
    rf = RegisterFiles(10)
    rf.set_write_enable(True)
    rf.set_addresses(5, 3, 1)

    # Test writing to a register
    rf.write(100)
    assert rf.get_value(5) == 100

    rf.set_addresses(0, 10, 1)
    # Test writing to a register with key = 0
    rf.write(200)
    assert rf.get_value(0) == 0

    # Test getting the value of all registers
    rf.print_all()


    # Test getting the value of all registers after writing to some
    rf.set_addresses(1, 10, 1)
    rf.write(50)
    rf.set_addresses(2, 1, 3)
    rf.write(60)
    rf.set_addresses(3, 1, 0)
    rf.write(70)
    assert rf.get_value(1) == 50
    assert rf.get_value(2) == 60
    assert rf.get_value(3) == 70
    rf.print_all()

    rf.set_write_enable(False)
    assert rf.write(10) == 'Write Enable is unset!'
