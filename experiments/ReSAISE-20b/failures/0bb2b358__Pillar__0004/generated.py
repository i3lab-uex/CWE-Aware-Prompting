import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------
# Domain model
# --------------------------------------------------------------------

@dataclass
class Patient:
    """Represents a patient record."""
    id: str
    name: str
    age: int
    gender: str
    diagnosis: str  # sensitive
    treatment_plan: str  # sensitive

# --------------------------------------------------------------------
# Repository (simulated for this example)
# --------------------------------------------------------------------

class PatientRepository:
    """
    A very small in‑memory repository that mimics access to a persistent store.
    In a real system this would be backed by a database or secure storage.
    """
    _storage: Dict[str, Patient] = {}

    @classmethod
    def add_patient(cls, patient: Patient) -> None:
        cls._storage[patient.id] = patient

    @classmethod
    def get_patient(cls, patient_id: str) -> Patient:
        try:
            return cls._storage[patient_id]
        except KeyError as exc:
            raise ValueError(f"Patient with id '{patient_id}' not found") from exc

# --------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------

_ALLOWED_ATTRIBUTES = {"name", "age", "gender"}

_PLACEHOLDER_RE = re.compile(r"{patient\.([a-zA-Z_][a-zA-Z0-9_]*)}")

def _safe_format(patient: Patient, template: str) -> str:
    """
    Replace placeholders in the form `{patient.<attr>}` with actual patient data.
    Only attributes listed in _ALLOWED_ATTRIBUTES are permitted; any other
    placeholder results in a ValueError.
    """
    def replace(match: re.Match) -> str:
        attr = match.group(1)
        if attr not in _ALLOWED_ATTRIBUTES:
            raise ValueError(f"Access to disallowed attribute '{attr}' is prohibited")
        return str(getattr(patient, attr))

    return _PLACEHOLDER_RE.sub(replace, template)

# --------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------

def generate_user_report(patient_id: str, template: str) -> str:
    """
    Generate a report for the specified patient by applying the given template.
    
    Parameters
    ----------
    patient_id : str
        The unique identifier of the patient whose data should be inserted.
    template : str
        A string containing placeholders in the form `{patient.<attr>}`.
    
    Returns
    -------
    str
        The fully rendered report string.
    
    Raises
    ------
    ValueError
        If the patient cannot be found, if an unknown or disallowed placeholder is present,
        or if any other error occurs during rendering.
    """
    try:
        # Load patient data (resource acquisition)
        patient = PatientRepository.get_patient(patient_id)

        # Render template safely
        report = _safe_format(patient, template)

        return report

    except Exception as exc:
        # Ensure no sensitive information leaks in the exception message
        raise ValueError("An error occurred while generating the report") from exc

# --------------------------------------------------------------------
# Example usage (for testing purposes only)
# --------------------------------------------------------------------

if __name__ == "__main__":
    # Populate the repository with a sample patient
    PatientRepository.add_patient(
        Patient(
            id="12345",
            name="John Doe",
            age=42,
            gender="Male",
            diagnosis="Hypertension",
            treatment_plan="Medication A"
        )
    )

    tmpl = "Patient Report:\nName: {patient.name}\nAge: {patient.age}\nGender: {patient.gender}"
    print(generate_user_report("12345", tmpl))