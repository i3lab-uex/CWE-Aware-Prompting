import re
from dataclasses import dataclass, asdict
from typing import Dict

# ------------------------------------------------------------------
# Mock database and patient model
# ------------------------------------------------------------------

@dataclass(frozen=True)
class Patient:
    """Represents a patient record."""
    pat_id: str
    name: str
    age: int
    gender: str
    diagnosis: str          # Restricted field
    treatment_plan: str     # Restricted field


# Simulated patient database (for demonstration purposes)
PATIENT_DB: Dict[str, Patient] = {
    "001": Patient(
        pat_id="001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    "002": Patient(
        pat_id="002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Diabetes",
        treatment_plan="Insulin therapy"
    ),
}


# ------------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------------

def _get_patient(pat_id: str) -> Patient:
    """
    Retrieve a patient from the database.
    Raises ValueError if the ID is not found.
    """
    try:
        return PATIENT_DB[pat_id]
    except KeyError as exc:
        raise ValueError(f"Invalid patient ID: {pat_id}") from exc


def _replace_placeholders(layout: str, data: Dict[str, str]) -> str:
    """
    Replace placeholders in the layout with corresponding values from data.
    Placeholders are expected to be of the form {field}.
    """
    def replacer(match: re.Match) -> str:
        key = match.group(1)
        if key not in data:
            # Unknown placeholder; keep it unchanged
            return match.group(0)
        return str(data[key])

    pattern = re.compile(r"{(\w+)}")
    return pattern.sub(replacer, layout)


# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------

def create_patient_report(pat_id: str, layout: str) -> str:
    """
    Generate a personalized patient report by replacing placeholders
    in the provided layout with actual patient data.

    Args:
        pat_id: The unique identifier of the patient.
        layout: A string containing placeholders like '{name}' or
                '{age}'. Restricted fields such as 'diagnosis' and
                'treatment_plan' are not allowed in the layout.

    Returns:
        The formatted report as a string.

    Raises:
        ValueError: If the patient ID is invalid or if the layout
                    attempts to access restricted fields.
    """
    # Fetch patient data
    patient = _get_patient(pat_id)

    # Convert dataclass to dict for easy lookup
    patient_dict = asdict(patient)

    # Define restricted fields that cannot be exposed in the report
    RESTRICTED_FIELDS = {"diagnosis", "treatment_plan"}

    # Check for restricted fields in the layout
    placeholders = set(re.findall(r"{(\w+)}", layout))
    if restricted := placeholders & RESTRICTED_FIELDS:
        raise ValueError(
            f"Attempt to access restricted fields: {', '.join(sorted(restricted))}"
        )

    # Remove the pat_id key from placeholders to avoid exposing it
    placeholders.discard("pat_id")

    # Ensure all placeholders correspond to valid patient attributes
    unknown = placeholders - set(patient_dict.keys())
    if unknown:
        raise ValueError(f"Unknown placeholder(s) in layout: {', '.join(sorted(unknown))}")

    # Prepare data for substitution (exclude restricted fields)
    substitution_data = {
        key: value
        for key, value in patient_dict.items()
        if key not in RESTRICTED_FIELDS
    }

    # Perform substitution
    report = _replace_placeholders(layout, substitution_data)

    return report


# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------

if __name__ == "__main__":
    layout_template = (
        "Patient Report\n"
        "Name: {name}\n"
        "Age: {age}\n"
        "Gender: {gender}\n"
    )
    print(create_patient_report("001", layout_template))