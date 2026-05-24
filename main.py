from models import PhysicalEvidence, DigitalEvidence, TestimonyEvidence
from court import Judge, LenientStrategy, StrictStrategy
from factory import CrimeFactory


def section(title: str):
    print(f"\n{'─'*55}")
    print(f"  {title}")
    print('─'*55)


if __name__ == "__main__":
    section("1. Creating cases via Factory")

    fraud = CrimeFactory.create_crime("fraud", {
        "case_id": "FRAUD-2024-07",
        "severity": 7,
        "amount": 840_000
    })
    theft = CrimeFactory.create_crime("theft", {
        "case_id": "THEFT-2024-31",
        "severity": 4
    })
    cyber = CrimeFactory.create_crime("cyber", {
        "case_id": "CYBER-2024-15",
        "severity": 6
    })

    for crime in (fraud, theft, cyber):
        print(f"  {crime}")
        print(f"    {crime.investigate()}")

    section("2. Attempting verdict on an open case")
    judge_marek = Judge(name="Marek Rogalski", strategy=LenientStrategy())
    print(judge_marek.pass_judgment(fraud))

    section("3. Collecting evidence")

    fraud.add_evidence(PhysicalEvidence("Forged wire-transfer documents"))
    fraud.add_evidence(DigitalEvidence("Offshore account export", hash_verified=True))
    fraud.add_evidence(TestimonyEvidence("Forensic accountant report", is_expert=True))
    fraud.close_case()
    print(f"  {fraud.get_case_id()} evidence modifier: {fraud.compute_evidence_modifier():.2f}")

    theft.add_evidence(PhysicalEvidence("Fingerprints on stolen laptop"))
    theft.add_evidence(TestimonyEvidence("Shop owner saw the suspect", is_expert=False))
    theft.close_case()
    print(f"  {theft.get_case_id()} evidence modifier: {theft.compute_evidence_modifier():.2f}")

    cyber.add_evidence(DigitalEvidence("Server access logs", hash_verified=False))
    cyber.close_case()
    print(f"  {cyber.get_case_id()} evidence modifier: {cyber.compute_evidence_modifier():.2f}")

    section("4. Lenient verdict (fraud)")
    judge_marek.set_strategy(LenientStrategy())
    print(judge_marek.pass_judgment(fraud))

    section("5. Strict verdict (fraud) + fraud bonus")
    judge_marek.set_strategy(StrictStrategy())
    print(judge_marek.pass_judgment(fraud))

    section("6. Strict verdict (cyber) — unverified evidence weakens sentence")
    print(judge_marek.pass_judgment(cyber))

    section("7. Lenient verdict (theft)")
    judge_marek.set_strategy(LenientStrategy())
    print(judge_marek.pass_judgment(theft))