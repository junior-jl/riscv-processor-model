from classes.RegisterFiles import RegisterFiles


def test_register_files():
    # Create an instance of RegisterFiles with 10 registers
    rf = RegisterFiles(10)

    # Test writing to a register
    rf.write(5, 100)
    assert rf.get_value(5) == 100

    # Test writing to a register with key = 0
    rf.write(0, 200)
    assert rf.get_value(0) == 0

    # Test getting the value of all registers
    rf.print_all()

    # Test getting the value of all registers after writing to some
    rf.write(1, 50)
    rf.write(2, 60)
    rf.write(3, 70)
    assert rf.get_value(1) == 50
    assert rf.get_value(2) == 60
    assert rf.get_value(3) == 70
    rf.print_all()
