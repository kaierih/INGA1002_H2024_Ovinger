from . import compare_type, compare_values, print2str, args2str, VariableTests
from unittest.mock import patch


class FunctionTests(VariableTests):
    """
    Class for use in generating feedback and score in an nbgrader task where student submission
    consists of a function declaration.

    Example usage: 
    ---------------------------------------------------------
    def solution_factorial(x):
        y = 1
        for i in range(x, 1, -1):
            y*=i
        return y

    test_obj = FunctionAutograder(solution_factorial, rtol=0.001)
    try:
        test_obj.add_test_func(factorial)
    except Exception as e:
        test_obj.log.append("Could not run tests, "+e.args[0], level="danger")
    else:
        for x in range(2, 8):
            test_obj.test_return_value(x)

    test_obj.get_summary()*cell_points # End of autograded cell. Outputs score to cell output.
    """

    def __init__(self, ref_func: callable, rtol=1e-2, atol=1e-8):
        super().__init__()
        # Register solution function
        self.ref_func = ref_func
        self.func_call_success = False
        self.return_type_verified = False
        self.usage_wgt = 0.2 # Should be configurable in config file
        #self.tests_wgt = 0.8 # Should be configurable in config file
        self.rtol = rtol
        self.atol = atol

    def add_test_func(self, test_func: callable):
        """
        Method to register student's solution to class instance.
        Raises an exception if parameter test_func is not callable.
        """
        assert callable(test_func), "entered solution is not identified as a callable function."
        self.test_func = test_func

    def test_new_func(self, test_func, ref_func, *args, **kwargs):
        self.ref_func = ref_func
        self.test_func = test_func
        self.func_call_success = False
        self.return_type_verified = False
        self.test_return_value(*args, **kwargs)

    def test_return_value(self, *args, **kwargs):
        """
        Method to run an inital test matching input parameters with arguments,
        and verifying return value type.
        Adds points for each success.
        Raises an exception upon failure.
        """
        # Compose string of input arguments
        arg_str = args2str(*args, **kwargs)

        try:
            # Attempt to call student submitted function with mocked print
            with patch(f'{__name__}.print') as mock_print:
                x = self.test_func(*args, **kwargs)
        except Exception as e:
            # If function could not execute, log error message and input arguments.
            msg_body = "test call "+str(self.test_func.__name__)+"("+arg_str+") exited with errors: " + str(e.args[0])
            self.add_result(False, msg_body, wgt=self.usage_wgt)
        else:
            if not self.func_call_success:
                msg_body = "test call "+str(self.test_func.__name__)+"("+arg_str+") completed without errors."
                self.add_result(True, msg_body, wgt=self.usage_wgt)
                self.func_call_success = True
            # Compile string of any printouts from student function
            x_print = ""
            for call in mock_print.mock_calls:
                x_print += print2str(*call.args, **call.kwargs)

            # Compile string of any printouts from solution function
            with patch(f'{__name__}.print') as mock_print:
                y = self.ref_func(*args, **kwargs)
            y_print = ""

            for call in mock_print.mock_calls:
                y_print += print2str(*call.args, **call.kwargs)

            # Check correct type
            if compare_type(x, y):
                # Compare returned values
                if not self.return_type_verified:
                    self.return_type_verified = True
                    self.add_result(True,
                                    "test call %s(%s) returned a value of the correct type (%s)."%
                                    (self.test_func.__name__, arg_str, type(x).__name__),
                                    wgt=self.usage_wgt)

                test_result, val_msg = compare_values(x, y)

                #func_msg = "test call %s(%s) returned %s"%(self.test_func.__name__, arg_str, val_msg)
                func_msg = "%scorrect return value for function call '%s(%s)': <div style='margin-left: 15px;'>%s</div>"%(
                    "" if test_result else "in", self.test_func.__name__, arg_str, val_msg)
                self.add_result(test_result, func_msg)
                
            elif len(x_print) > 0 and len(y_print) > 0 and y is None:
                # Compare prined output
                if not self.return_type_verified:
                    self.return_type_verified = True
                    self.add_result(True,
                                    "test call %s(%s) generated a printed message."%
                                    (self.test_func.__name__, arg_str),
                                    wgt=self.usage_wgt)
                test_result, val_msg = compare_values(x_print, y_print)
                func_msg = "test call %s(%s) printed %s"%(self.test_func.__name__, arg_str, val_msg)
                self.add_result(test_result, func_msg)
            elif x is None and len(x_print) > 0:
                # Alert student of printed message instead of returned value
                self.add_result(False, "test call %s(%s) did not return a value of type %s, but printed the following: %s"%
                                (self.test_func.__name__, arg_str, type(y).__name__, x_print))
            else:
                # Alert no match in types
                self.add_result(False, "test call %s(%s) returned a value of type %s and not %s."%
                                (self.test_func.__name__, arg_str, type(x).__name__, type(y).__name__))