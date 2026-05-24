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