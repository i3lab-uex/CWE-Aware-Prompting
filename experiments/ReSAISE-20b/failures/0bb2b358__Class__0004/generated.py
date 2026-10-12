import re
from dataclasses import dataclass, asdict
from typing import Dict

# ------------------------------------------------------------------
# Domain model – patient information
# ------------------------------------------------------------------

@dataclass(frozen=True)
class Patient:
    """Represents a patient record."""
    id: str
    name: str
    age: int
    gender: str
    diagnosis: str          # Sensitive
    treatment_plan: str     # Sensitive

# ------------------------------------------------------------------
# In‑memory store – replace with real DB in production
# ------------------------------------------------------------------

class PatientStore:
    """Simple patient lookup service."""
    _patients: Dict[str, Patient] = {}

    @classmethod
    def add_patient(cls, patient: Patient) -> None:
        cls._patients[patient.id] = patient

    @classmethod
    def get_patient(cls, patient_id: str) -> Patient:
        try:
            return cls._patients[patient_id]
        except KeyError as exc:
            raise ValueError(f"Patient with id '{patient_id}' not found") from exc

# ------------------------------------------------------------------
# Utility – safe placeholder extraction
# ------------------------------------------------------------------

_ALLOWED_PLACEHOLDERS = {"name", "age", "gender"}

_PLACEHOLDER_RE = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def _extract_placeholders(template: str) -> set:
    """Return the set of placeholder names found in *template*."""
    return {match.group(1) for match in _PLACEHOLDER_RE.finditer(template)}

# ------------------------------------------------------------------
# Core function – generate_user_report
# ------------------------------------------------------------------

def generate_user_report(patient_id: str, template: str) -> str:
    """
    Generate a report string for *patient_id* using *template*.

    The template may contain placeholders of the form `{patient.attribute}`.
    Only a limited set of attributes (`name`, `age`, `gender`) are allowed
    to prevent accidental exposure of sensitive data such as diagnosis or
    treatment_plan.

    Raises:
        ValueError: If the patient cannot be found, if the template is
                    malformed, or if it attempts to access disallowed data.
    """
    # 1. Retrieve patient record
    patient = PatientStore.get_patient(patient_id)

    # 2. Validate template placeholders
    placeholders = _extract_placeholders(template)
    if not placeholders:
        # No placeholders – return template unchanged
        return template

    disallowed = placeholders - _ALLOWED_PLACEHOLDERS
    if disallowed:
        raise ValueError(
            f"Template attempts to access disallowed attributes: {', '.join(disallowed)}"
        )

    # 3. Prepare safe mapping
    patient_dict = {k: getattr(patient, k) for k in placeholders}

    # 4. Render the template
    try:
        report = template.format(patient=patient_dict)
    except KeyError as exc:
        # This should not happen due to prior validation, but guard anyway
        raise ValueError(f"Missing placeholder data: {exc}") from exc

    return report

# ------------------------------------------------------------------
# Example usage (remove or comment out in production)
# ------------------------------------------------------------------

if __name__ == "__main__":
    # Add a sample patient
    p = Patient(
        id="12345",
        name="Jane Doe",
        age=29,
        gender="Female",
        diagnosis="Hypertension",
        treatment_plan="Medication A, lifestyle changes"
    )
    PatientStore.add_patient(p)

    # Valid template
    tmpl = "Patient Report:\nName: {patient.name}\nAge: {patient.age}\nGender: {patient.gender}"
    print(generate_user_report("12345", tmpl))

    # Attempt to access sensitive data – should raise ValueError
    bad_tmpl = "Diagnosis: {patient.diagnosis}"
    try:
        print(generate_user_report("12345", bad_tmpl))
    except ValueError as e:
        print(f"Error: {e}")