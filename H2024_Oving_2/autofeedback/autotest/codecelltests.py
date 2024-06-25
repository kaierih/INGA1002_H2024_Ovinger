from . import VariableTests, print2str
import re
from unittest.mock import patch


class CodeCellTests(VariableTests):
    """
    Test class to check execution and output of code cell.
    """

    def __init__(self, code_cell_contents: str, init_wgt=1.0, globals=None, locals=None):
        super().__init__()
        self.source = code_cell_contents
        self.globals = globals
        self.locals = locals
        self.test_exec(wgt=init_wgt)

    def test_exec(self, wgt=1.0):
        _, N_tests = self.score.get_ratio()
        msg_intro = f"Test {N_tests + 1}"
        self.student_print = ""
        scope_name = __name__ if self.globals is None else self.globals["__name__"]
        try:
            with patch(f'{scope_name}.print') as mock_print:
                exec(self.source, self.globals, self.locals)
            for call in mock_print.mock_calls:
                self.student_print += print2str(*call.args, **call.kwargs)
        except Exception as e:
            feedback = "answer cell could not execute: " + e.args[0]
            self.score.process_result(False, wgt)
            self.log.append(msg_intro + " failed: " + feedback)
        else:
            if wgt != 0.0:
                feedback = "answer cell executed without errors"
                self.score.process_result(True, wgt)
                self.log.append(msg_intro + " passed: " + feedback)

    def test_output(self, desired_output: str, sample=None, wgt=1.0, ignore_code_match=True):
        passed = False
        content_match = re.search(desired_output, self.source)

        if content_match is not None and ignore_code_match == False:
            feedback = f"code cell appears to contain an explicit declaration of {sample if sample is not None else 'solution'}, indicating output is not the result of calculations using python"
        else:
            output_match = re.search(desired_output, self.student_print)
            if output_match is not None:
                feedback = f"'{output_match.group()}' in printed message matches desired output."
                passed = True
            else:
                feedback = f"no match for '{sample if sample is not None else desired_output}' found in printed message."

        _, N_tests = self.score.get_ratio()
        msg_intro = f"Test {N_tests + 1}"

        self.score.process_result(passed, wgt)
        if passed:
            self.log.append(msg_intro + " passed: " + feedback)
        else:
            self.log.append(msg_intro + " failed: " + feedback)

    def replace(self, pattern: str, replacement: str):
        self.source = re.sub(pattern, replacement, self.source)
        self.test_exec(wgt=0.0)
        self.score.pop(-1)
        self.log.clear(start=-1)
        self.log.append(f"Making adjustment to code: {replacement}")
        # add code to remove logged score/message
        # add check to see if code executed successfully        

    def insert_top(self, new_code):
        self.source = new_code + "\n" + self.source
        self.test_exec(wgt=0.0)
        self.log.append(f"Adding new code: {new_code}")