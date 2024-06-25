import re
from io import StringIO
import numpy as np


def print2str(*args, **kwargs):
    """
    Function to print to string instead of stdout.
    """
    with StringIO() as output:
        print(*args, file=output, **kwargs)
        contents = output.getvalue()
    return contents


def args2str(*args, **kwargs):
    """
    Function to compile a readable string from function arguments.
    """
    arg_str = ""
    for arg in args:
        arg_str += str(arg) + ", "
    for kw, arg in kwargs.items():
        arg_str += str(kw) + " = " + str(arg) + ", "
    if len(arg_str) > 1:
        arg_str = arg_str[:-2]
    return arg_str


def compare_type(x, y):
    """
    Function to check if two values have roughly equivalent type.
    Tuple, list and array count as equivalent
    Numerical types (float, int) count as equivalent
    Returns false for NoneType variables
    """
    passed = False
    if type(x) is type(y) and y is not None:
        passed = True
    else:
        sequences = (tuple, list, np.ndarray)
        if isinstance(x, sequences) and isinstance(y, sequences):
            passed = True
        elif isinstance(x, (int, float)) and isinstance(y, (int, float)):
            passed = True
        else:
            passed = False
    return passed


def get_deviation(x, y, rtol=1e-2, atol=1e-8):
    """
    Function to return largest absolute error and largest relative error
    when comparing two array-like inputs 'x' and 'y'.
    """
    err = np.abs(np.subtract(x, y))
    err_loc = np.where(err > atol + np.multiply(rtol, np.abs(y)))
    err = np.take(err, err_loc).flatten()

    with np.errstate(divide='ignore'):
        rel_err = err/np.take(np.abs(y), err_loc).flatten()

    return np.max(err), np.max(rel_err)


def compare_values(x, y, rtol=1e-2, atol=1e-8):
    """
    Function to compare two variables, and return both a test result and a message.
    Numerical types will produce a feedback message with relative and absolute error.
    To be used AFTER type compatability is verified using 'compare_type(x, y)'.
    """

    passed = False
    if isinstance(y, (int, float)):
        try:
            passed = np.allclose(x, y, rtol=rtol, atol=atol)
        except Exception as e:
            msg = "value comparison failed: " + e.args[0]
        else:
            if passed:
                msg = f"value {x} is correct within tolerance."
            else:
                err, rel_err = get_deviation(x, y, rtol=rtol, atol=atol)
                msg = f"value {x} is incorrect... absolute error = {err}, relative error = {rel_err}."

    elif isinstance(y, (tuple, list, np.ndarray)):
        if len(x) != len(y):
            msg = f"array has length {len(x)} and not {len(y)}."
        else:
            try:
                passed = np.allclose(x, y, rtol=rtol, atol=atol)
            except Exception as e:
                msg = "array verification failed: " + e.args[0]
            else:
                if passed:
                    msg = "array values are correct within tolerance."
                else:
                    err, rel_err = get_deviation(x, y, rtol=rtol, atol=atol)
                    msg = f"array contains one or more incorrect values; max abslute error = {err}, max relative error = {rel_err:.3f}."

    elif isinstance(y, str):
        string_match = re.search(y, x)
        if string_match is not None:
            msg = f"string content '{string_match.group()}' is correct."
            passed = True
        else:
            msg = "string does not contain desired pattern."
    else:
        try:
            assert x == y, "value is incorrect."
        except Exception as e:
            msg = e.args[0]
        else:
            passed = True
            msg = "value is correct."
    return passed, msg