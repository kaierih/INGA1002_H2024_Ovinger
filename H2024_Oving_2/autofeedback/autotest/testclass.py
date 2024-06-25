from string import Template
from IPython.display import HTML, display


class FeedbackLogger:
    """
    Class to log feedback messages from test results,
    and present end result using HTML formatting.
    """

    def __init__(self, init_log=[]):
        """
        Creates a new instance of FeedbackLogger with the option
        to pass initial message lines to @log.
        """
        self.message_log = [] + init_log
        self.log_template = Template('<div class = "alert alert-$level">$msg</div>')

    def append(self, msg: str):
        """
        Adds feedback message @msg to end of log
        """
        self.message_log.append(msg)

    def insert(self, index: int, msg: str):
        """
        Inserts feedback message @msg with index @index
        """
        self.message_log.insert(index, msg)

    def display(self, level: str):
        """ 
        Displays message using HTML formatting and color alert scheme controlled by 
        @level.
        """
        output = "<br>".join(self.message_log)
        display(HTML(self.log_template.substitute({"level":level,"msg":output})))

    def clear(self, start: int = 0, stop: int = -1, step: int = 1):
        """
        Removes a slice of the log messages.
        No input arguments clears the entire list.
        """
        if stop < -0:
            stop = len(self.message_log) + 1 + stop
        if start < -0:
            start = len(self.message_log) + start
        index = list(range(start, stop, step))
        index.reverse()
        for i in index:
            self.message_log.pop(i)


class ScoreCalculator:
    """
    Class to keep track of test score.
    Test results are accumulated over time, and finally returned as a value between 
    0.0 and 1.0.
    """

    def __init__(self):
        self.test_results = []
        self.weights = []

    def process_result(self, result: bool, wgt: float = 1.0):
        """
        Add a test result @result to the score sheet with optional wieght @wgt.
        @wgt weight is relative, with default of 1.0 attributing equal amount
        of points per test.
        """
        self.weights.append(wgt)
        self.test_results.append(result)

    def get_ratio(self):
        """
        Returns ratio of tests passed to total number of tests.
        """
        return sum(self.test_results), len(self.test_results)

    def get_score(self):
        """
        Returns final score as a number 0.0 <= score <= 1.0.
        """
        score = 0.0
        wgt_sum = sum(self.weights)
        # Distribute remaining score difference evenly among remaining tests
        # Calculate score
        for i in range(len(self.weights)):
            score += self.weights[i]*self.test_results[i]/wgt_sum
        # Constrain score to number between 0.0 and 1.0
        score = max(score, 0.0)
        score = min(score, 1.0)
        return score # Higher precision not relevant, 

    def pop(self, n: int):
        """
        Remove test results at index 'n' from calculated score.
        """
        self.test_results.pop(n)
        self.weights.pop(n)

class TestClass:
    """
    Base class for autograded tests with feedback
    Will keep a log of test results, as well as appropriate feedback messages.

    Example Usage:
    ----------------------
    grading_tests = CustomTests()
    if student_answer == 42:
        grading_tests.add_result(True, f"'student_answer' has the value {student_answer}, which is accepted!")
    else:
        grading_tests.add_result(False, f"'student_answer' has the value {student_answer}, which deviates from the correct value!")
    grading_tests.get_results()*total_points
    ----------------------
    """

    def __init__(self):
        self.log = FeedbackLogger()
        self.score = ScoreCalculator()

    def add_result(self, result: bool, msg: str, wgt=1.0):
        _, N_tests = self.score.get_ratio()
        msg_intro = f"Test {N_tests + 1}"
        self.score.process_result(result, wgt)
        if result:
            self.log.append(msg_intro + " passed: " + msg)
        else:
            self.log.append(msg_intro + " failed: " + msg)

    def get_results(self):
        score = self.score.get_score()
        if round(score, 3) >= 1.0:
            self.log.clear()
            self.log.append("All tests passed!")
            level = "success"
        elif score == 0.0:
            if len(self.score.test_results) > 1:
                self.log.clear(start=1)
                self.log.insert(0, "No tests passed, displaying only first test result: ")
            level = "danger"
        else:
            passed, total = self.score.get_ratio()
            self.log.insert(0, f"{passed} of {total} tests passed:")
            level = "warning"
        self.log.display(level)
        return score