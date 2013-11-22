from unittest import TestCase
from restructuredtext_lint import restructuredtext_lint


class TestRunFunction(TestCase):
    def test_run_exists(self):
        self.assertTrue(bool(restructuredtext_lint.run))
