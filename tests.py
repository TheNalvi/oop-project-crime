import unittest
from models import Theft, CyberCrime, FinancialFraud, PhysicalEvidence, DigitalEvidence
from factory import CrimeFactory
from court import Judge, LenientStrategy, StrictStrategy

class TestEncapsulation(unittest.TestCase):

    def test_severity_valid(self):
        c = Theft(case_id="T-1", severity=5)
        self.assertEqual(c.get_severity(), 5)

    def test_severity_out_of_bounds_raises(self):
        with self.assertRaises(ValueError):
            Theft(case_id="T-1", severity=11)

    def test_fraud_negative_amount_raises(self):
        with self.assertRaises(ValueError):
            FinancialFraud(case_id="F-1", severity=5, amount=-1)

    def test_close_without_evidence_fails(self):
        c = Theft(case_id="T-1", severity=5)
        self.assertFalse(c.close_case())

    def test_close_with_evidence_succeeds(self):
        c = Theft(case_id="T-1", severity=5)
        c.add_evidence(PhysicalEvidence("Watch"))
        self.assertTrue(c.close_case())


class TestFactory(unittest.TestCase):

    def test_creates_correct_type(self):
        c = CrimeFactory.create_crime("theft", {"case_id": "T-1", "severity": 3})
        self.assertIsInstance(c, Theft)

    def test_unknown_type_raises(self):
        with self.assertRaises(ValueError):
            CrimeFactory.create_crime("arson", {"case_id": "A-1", "severity": 5})


class TestStrategy(unittest.TestCase):

    def test_open_case_rejected(self):
        c = Theft(case_id="T-1", severity=5)
        judge = Judge(name="Marek", strategy=LenientStrategy())
        self.assertIn("open", judge.pass_judgment(c))

    def test_lenient_verdict_contains_fine(self):
        c = Theft(case_id="T-1", severity=5)
        c.add_evidence(PhysicalEvidence("Watch"))
        c.close_case()
        verdict = LenientStrategy().issue_verdict(c)
        self.assertIn("$", verdict)

    def test_strict_verdict_contains_years(self):
        c = Theft(case_id="T-1", severity=5)
        c.add_evidence(PhysicalEvidence("Watch"))
        c.close_case()
        verdict = StrictStrategy().issue_verdict(c)
        self.assertIn("years", verdict)


if __name__ == "__main__":
    unittest.main(verbosity=2)