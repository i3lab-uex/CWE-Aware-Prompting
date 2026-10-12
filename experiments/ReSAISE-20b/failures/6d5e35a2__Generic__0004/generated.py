import re
from typing import Any

# Dummy Patient model for demonstration. In a real system this would be an ORM or database model.
class Patient:
    _db = {
        "P001": {"name": "Alice Smith", "age": 34, "gender": "F",
                 "diagnosis": "Hypertension", "treatment_plan": "Medication A"},
        "P002": {"name": "Bob Jones", "age": 58, "gender": "M",
                 "diagnosis": "Diabetes", "treatment_plan": "Medication B"},
    }

    def __init__(self, pat_id: str):
        if pat_id not in self._db:
            raise ValueError(f"Patient ID {pat_id} does not exist.")
        self.pat_id = pat_id
        data = self._db[pat_id]
        for key, value in data.items():
            setattr(self, key, value)

    @property
    def patient_data(self) -> dict[str, Any]:
        """Return a dictionary of all public attributes."""
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

def create_patient_report(pat_id: str, layout: str) -> str:
    """
    Generate a patient report by replacing placeholders in the layout with actual patient data.

    Parameters
    ----------
    pat_id : str
        Unique identifier of the patient.
    layout : str
        Report template containing placeholders like '{patient.name}'.

    Returns
    -------
    str
        The formatted report with all placeholders replaced by patient data.

    Raises
    ------
    ValueError
        If the patient ID is invalid or if the template tries to access restricted information.
    """
    # Load patient data
    try:
        patient = Patient(pat_id)
    except ValueError as exc:
        raise ValueError(f"Invalid patient ID: {pat_id}") from exc

    # Define restricted fields
    restricted_fields = {"diagnosis", "treatment_plan"}

    # Find all placeholders in the layout
    placeholder_pattern = re.compile(r"{\s*patient\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")
    placeholders = placeholder_pattern.findall(layout)

    # Validate placeholders
    for field in set(placeholders):
        if field not in patient.patient_data:
            raise ValueError(f"Unknown placeholder '{{patient.{field}}}'")
        if field in restricted_fields:
            raise ValueError(f"Access to restricted field '{{patient.{field}}}' is not allowed")

    # Replace placeholders
    def replacer(match: re.Match) -> str:
        field_name = match.group(1).strip()
        value = getattr(patient, field_name)
        return str(value)

    formatted_report = placeholder_pattern.sub(replacer, layout)
    return formatted_report