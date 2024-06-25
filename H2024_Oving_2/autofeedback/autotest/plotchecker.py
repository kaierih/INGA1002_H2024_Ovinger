from . import TestClass, compare_type, compare_values


class VariableTests(TestClass):
    def __init__(self, line):
        self.line = line
        super().__init__()

    def test_function(self, func: callable):
        result, msg = compare_values(self.line.get_ydata(), func(self.line.get_xdata()))
        self.add_result(result, msg)
    def test_x(self, x_vals):
        pass
    def test_y(self, y_vals):
        pass