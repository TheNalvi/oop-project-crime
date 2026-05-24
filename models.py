from abc import ABC, abstractmethod

class Evidence(ABC):
    def __init__(self, description: str):
        self.__description = description
    
    def get_description(self) -> str:
        return self.__description
    
    @abstractmethod
    def get_legal_status(self) -> str:
        pass
    
    @abstractmethod
    def get_weight_modifier(self) -> float:
        pass
    
    def __repr__(self):
        return f"{self.__class__.__name__}('{self.__description}')"
    
class PhysicalEvidence(Evidence):
    def get_legal_status(self) -> str:
        return f"[Physical] {self.get_description()} - sealed in evidence vault."

    def get_weight_modifier(self) -> float:
        return 1.3

class DigitalEvidence(Evidence):
    def __init__(self, description: str, hash_verified: bool):
        super().__init__(description)
        self.__hash_verified = hash_verified
        
    def is_hash_verified(self) -> bool:
        return self.__hash_verified
    
    def get_legal_status(self) -> str:
        status = "hash verified" if self.__hash_verified else "hash UNVERIFIED"
        return f"[Digital] {self.get_description()} - {status}."
    
    def get_weight_modifier(self) -> float:
        return 1.2 if self.__hash_verified else 0.8
    
class TestimonyEvidence(Evidence):
    def __init__(self, description: str, is_expert: bool):
        super().__init__(description)
        self.__is_expert = is_expert
        
    def get_legal_status(self) -> str:
        kind = "Expert" if self.__is_expert else "Witness"
        return f"[{kind} testimony] {self.get_description()}."

    def get_weight_modifier(self) -> float:
        return 1.15 if self.__is_expert else 0.9
    
    
class Crime(ABC):
    def __init__(self, case_id: str, severity: int):
        self.__case_id = case_id
        self.__severity = None
        self.set_severity(severity)
        self.__evidence_list = []
        self.__is_closed = False
    
    def get_case_id(self) -> str:
        return self.__case_id
    
    def get_severity(self) -> int:
        return self.__severity
    
    def get_evidence_list(self) -> list:
        return list(self.__evidence_list)
    
    def is_closed(self) -> bool:
        return self.__is_closed
    
    def set_severity(self, value: int):
        if not isinstance(value, int) or not (1 <= value <= 10):
            raise ValueError(f"Severity must be an integer 1-10")
        self.__severity = value
        
    def add_evidence(self, evidence: Evidence):
        if not isinstance(evidence, Evidence):
            raise TypeError(f"Expected Evidence, got {type(evidence).__name__}")
        self.__evidence_list.append(evidence)
    
    def close_case(self) -> bool:
        if not self.__evidence_list:
            print(f"Cannot close case {self.__case_id}: no evidence on file.")
            return False
        self.__is_closed = True
        return True
    
    def compute_evidence_modifier(self) -> float:
        if not self.__evidence_list:
            return 1.0
        return sum(e.get_weight_modifier() for e in self.__evidence_list) / len(self.__evidence_list)
    
    @abstractmethod
    def investigate(self) -> str:
        pass
    
    @abstractmethod
    def get_crime_category(self) -> str:
        pass
    
    def __repr__(self):
        return (f"{self.__class__.__name__}(case={self.__case_id!r}, "
                f"severity={self.__severity}, closed={self.__is_closed})")

class Theft(Crime):
    def investigate(self) -> str:
        return f"Scanning pawn shop databases and CCTV footage for case {self.get_case_id()}."

    def get_crime_category(self) -> str:
        return "Property Crime"
    

class CyberCrime(Crime):
    def investigate(self) -> str:
        return f"Analysing server logs and network packets for case {self.get_case_id()}."

    def get_crime_category(self) -> str:
        return "Digital Crime"

class FinancialFraud(Crime):
    def __init__(self, case_id: str, severity: int, amount: float):
        super().__init__(case_id, severity)
        self.__amount = None
        self.set_amount(amount)
    
    def get_amount(self) -> float:
        return self.__amount

    def set_amount(self, value: float):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Fraud amount must be a non-negative number.")
        self.__amount = float(value)
   
    def investigate(self) -> str:
        return (f"Auditing bank transactions for case {self.get_case_id()}. "
                f"Estimated loss: ${self.__amount:,.2f}.")

    def get_crime_category(self) -> str:
        return "Financial Crime"
        