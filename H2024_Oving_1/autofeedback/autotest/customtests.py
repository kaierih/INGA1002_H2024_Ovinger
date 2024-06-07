from . import TestClass


class CustomTests(TestClass):
    """
    Test class for custom grading tests.
    Will keep a log of test results, as well as appropriate feedback messages.

    Example Usage:

    grading_tests = CustomTests()
    grading_tests.record(isInstance(student_answer, float),
                         success = "Variable 'student_answer' is the correct type",
                         fail = f"'student_answer' is of type {type(student_answer)} and not 'float'",
                         wgt = 0.2)
    grading_tests.record(student_answer == 42.0,
                         success = "'student_answer' has the value {student_answer}, which is accepted!",
                         fail = "'student_answer' has the value {student_answer}, which deviates from the correct value!"
                         )
    grading_tests.get_results()*total_points
    )
    """

    def test(self, result: bool, success: str, fail: str, wgt=1.0):
        if result:
            self.add_result(result, success)
        else:
            self.add_result(result, fail)