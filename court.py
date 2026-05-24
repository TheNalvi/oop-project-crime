from abc import ABC, abstractmethod
from models import Crime, FinancialFraud

class SentencingStrategy(ABC):
    @abstractmethod
    def issue_verdict(self, crime: Crime) -> str:
        pass
    
class LenientStrategy(SentencingStrategy):
    def issue_verdict(self, crime: Crime) -> str:
        base_fine = crime.get_severity() * 2500
        modifier = crime.compute_evidence_modifier()
        final_fine = int(base_fine * modifier)
        return (f"Lenient verdict: probation and a ${final_fine:,} fine "
                f"(base ${base_fine:,} × evidence modifier {modifier:.2f}).")
        
class StrictStrategy(SentencingStrategy):
    def issue_verdict(self, crime: Crime) -> str:
        base_years = crime.get_severity() * 2
        modifier = crime.compute_evidence_modifier()
        bonus = 4 if isinstance(crime, FinancialFraud) else 0
        years = int((base_years + bonus) * modifier)
        return (f"Strict verdict: {years} years in prison "
                f"(base {base_years}y + fraud bonus {bonus}y) "
                f"× evidence modifier {modifier:.2f}).")
        
class Judge:
    def __init__(self, name: str, strategy: SentencingStrategy):
        self.__name = name
        self.__strategy = strategy
        
    def get_name(self) -> str:
        return self.__name
    
    def get_strategy(self) -> SentencingStrategy:
        return self.__strategy
    
    def set_strategy(self, strategy: SentencingStrategy):
        if not isinstance(strategy, SentencingStrategy):
            raise TypeError("Expected a SentencingStrategy instance.")
        self.__strategy = strategy
    
    def pass_judgment(self, crime: Crime) -> str:
        print(f"\n  Judge {self.__name} reviewing case {crime.get_case_id()} "
              f"[{crime.get_crime_category()}]")
        if not crime.is_closed():
            return f"  Rejected: case {crime.get_case_id()} is still open."
        return f"  {self.__strategy.issue_verdict(crime)}"

    def __repr__(self):
        return f"Judge(name={self.__name!r}, strategy={self.__strategy.__class__.__name__})"