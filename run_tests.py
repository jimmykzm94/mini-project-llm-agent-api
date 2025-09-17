import unittest
import json
from pathlib import Path

class JSONTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_results = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.test_results.append({"name": str(test), "status": "passed"})

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.test_results.append({"name": str(test), "status": "failed"})

class JSONTestRunner(unittest.TextTestRunner):
    resultclass = JSONTestResult

    def run(self, test):
        result = super().run(test)
        self._write_json(result)
        return result

    def _write_json(self, result):
        summary = {
            "total": result.testsRun,
            "failures": len(result.failures),
            "successes": result.testsRun - len(result.failures),
            "tests": result.test_results
        }
        output_file = Path("test_results.json")
        output_file.write_text(json.dumps(summary, indent=2))

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover("", pattern="test_*.py")
    runner = JSONTestRunner(verbosity=2)
    runner.run(suite)
