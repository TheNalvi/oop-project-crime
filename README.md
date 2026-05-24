# Justicia Management System
> An Object-Oriented Police Investigation & Court Sentencing Simulator in Python

---

## Overview
Justicia models a simplified legal workflow: crimes are investigated, evidence is collected, and a judge issues a verdict. The type and quality of evidence directly affects the final sentence.

---

## Project Structure

| File | Purpose |
|---|---|
| `models.py` | Evidence and Crime class hierarchies |
| `factory.py` | Factory pattern — creates Crime objects by type |
| `court.py` | Strategy pattern — sentencing algorithms and Judge |
| `main.py` | Demo run |
| `tests.py` | Unit tests |

---

## OOP Concepts Used

**Abstraction & Polymorphism** — `Evidence` and `Crime` are abstract base classes. Each subclass overrides `get_weight_modifier()` and `investigate()` with its own behaviour. Evidence modifiers aggregate into a score that changes the verdict calculation.

**Encapsulation** — all class fields are private (`__attr`). External access is only through explicit getters and setters (`get_severity()`, `set_severity()`, etc.).

**Inheritance** — `Theft`, `CyberCrime`, `FinancialFraud` inherit from `Crime`. `PhysicalEvidence`, `DigitalEvidence`, `TestimonyEvidence` inherit from `Evidence`.

**Factory Method** — `CrimeFactory.create_crime("fraud", {...})` instantiates the correct subclass without exposing constructors to the caller.

**Strategy Pattern** — `Judge` holds a `SentencingStrategy` that can be swapped at runtime (`LenientStrategy` / `StrictStrategy`).

---

## Running

```bash
python main.py
python tests.py
```