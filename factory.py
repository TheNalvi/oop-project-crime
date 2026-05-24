from models import Crime, Theft, CyberCrime, FinancialFraud

class CrimeFactory:
    _registry = {
        "theft": Theft,
        "cyber": CyberCrime,
        "fraud": FinancialFraud
    }
    
    @staticmethod
    def create_crime(crime_type: str, data: dict) -> Crime:
        key = crime_type.strip().lower()
        crime_class = CrimeFactory._registry.get(key)
        if not crime_class:
            supported = ", ".join(CrimeFactory._registry.keys())
            raise ValueError(f"Unknown crime type '{crime_type}'. Supported: {supported}")
        return crime_class(**data)