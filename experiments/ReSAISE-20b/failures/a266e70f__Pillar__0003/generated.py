import re
from typing import Dict

# --------------------------------------------------------------------------- #
# Patient model and in‑memory registry
# --------------------------------------------------------------------------- #

class Patient:
    """
    A simple patient data model. Only a subset of attributes are
    considered public; the rest are restricted and cannot be exposed via
    report templates.
    """
    def __init__(self, id: str, name: str, age: int, gender: str,
                 diagnosis: str = None, treatment_plan: str = None):
        self.id = id
        self.name = name
        self.age = age
        self.gender = gender

        # Restricted data – should not be exposed through templates
        self._diagnosis = diagnosis
        self._treatment_plan = treatment_plan

    @property
    def public(self) -> Dict[str, str]:
        """
        Return a dictionary of attributes that are safe to expose.
        """
        return {
            "name": self.name,
            "age": str(self.age),
            "gender": self.gender
        }

    @property
    def private(self) -> Dict[str, str]:
        """
        Return a dictionary of restricted attributes.
        """
        return {
            "diagnosis": self._diagnosis or "",
            "treatment_plan": self._treatment_plan or ""
        }

# In‑memory patient registry (simulate a database)
PATIENT_REGISTRY: Dict[str, Patient] = {}


# --------------------------------------------------------------------------- #
# Utility functions
# --------------------------------------------------------------------------- #

def _extract_placeholders(template: str) -> set:
    """
    Extract all placeholder names from the template.
    Example: '{patient.name} {patient.age}' -> {'name', 'age'}
    """
    pattern = r"{patient\.([a-zA-Z_][a-zA-Z0-9_]*)}"
    return set(re.findall(pattern, template))


def _validate_template(placeholders: set) -> None:
    """
    Ensure the template does not reference restricted data.
    Raises ValueError if a restricted field is used.
    """
    restricted = {"diagnosis", "treatment_plan"}
    intersection = placeholders & restricted
    if intersection:
        raise ValueError(
            f"Attempt to access restricted patient data: {', '.join(intersection)}"
        )


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def create_patient_report(id: str, report_template: str) -> str:
    """
    Generate a patient report by filling in placeholders from the template.

    Parameters
    ----------
    id : str
        Unique patient identifier.
    report_template : str
        Template string containing placeholders like '{patient.name}'.

    Returns
    -------
    str
        The report with all placeholders replaced by actual patient data.

    Raises
    ------
    ValueError
        If the patient ID is unknown or if restricted data is requested.
    """
    # 1. Validate patient existence
    patient = PATIENT_REGISTRY.get(id)
    if not patient:
        raise ValueError(f"Invalid patient ID: {id}")

    # 2. Parse placeholders
    placeholders = _extract_placeholders(report_template)

    # 3. Ensure no restricted data is requested
    _validate_template(placeholders)

    # 4. Build a mapping for formatting
    context = patient.public

    # 5. Perform safe formatting
    try:
        report = report_template.format(patient=patient, **context)
    except KeyError as exc:
        # This should not happen due to prior validation, but we guard anyway
        raise ValueError(f"Unknown placeholder: {exc}") from None

    return report


# --------------------------------------------------------------------------- #
# Example usage (for testing purposes)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Populate registry with a sample patient
    PATIENT_REGISTRY["p001"] = Patient(
        id="p001",
        name="Alice Smith",
        age=29,
        gender="Female",
        diagnosis="Hypertension",
        treatment_plan="Medication A"
    )

    # Create a report
    template = (
        "Patient Report\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    print(create_patient_report("p001", template))

    # Attempt to access restricted data – should raise ValueError
    try:
        bad_template = "Diagnosis: {patient.diagnosis}"
        print(create_patient_report("p001", bad_template))
    except ValueError as e:
        print(f"Error: {e}")