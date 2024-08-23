from . import TestClass, compare_type, compare_values


class VariableTests(TestClass):
    """
    Example usage:
    ----------------------------------
    test_obj = VariableTests()
    test_obj.compare(x1, y1, rtol=?, atol=?)
    test_obj.compare(x2, y2, rtol=?, atol=?)
    etc...
    test_obj.get_summary()*cell_points
    """

    def compare_values(self, x, y, name: str = None, rtol=1e-2, atol=1e-8):
        same_type = compare_type(x, y)
        if not same_type:
            msg = "variable '%s' is type %s and not %s."%(name, type(x).__name__, type(y).__name__)
            self.add_result(False, msg)
        else:
            #msg = "variable '%s' is the correct type (%s)."%(name, type(x).__name__)
            #self.add_result(True, msg, wgt=self.type_wgt)

            same_value, compare_msg = compare_values(x, y, rtol=rtol, atol=atol)
            msg = f'variable {"" if name is None else name} is a '+compare_msg
            self.add_result(same_value, msg)