import re
from dataclasses import dataclass, fields
from typing import Dict

# ------------------------------------------------------------------
# Mocked Patient model and data store
# ------------------------------------------------------------------

@dataclass(frozen=True)
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str          # Sensitive information
    treatment_plan: str

# In a real system this would be replaced with database access logic.
_PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient(
        patient_id="P001",
        name="Alice Smith",
        age=29,
        gender="Female",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle modification, medication A",
    ),
    "P002": Patient(
        patient_id="P002",
        name="Bob Johnson",
        age=45,
        gender="Male",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Insulin therapy, diet plan",
    ),
}

# ------------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------------

_RE_PLACEHOLDER = re.compile(r"\{([^{}]+)\}")

def _get_patient(patient_id: str) -> Patient:
    """
    Retrieve a patient instance from the data store.
    Raises ValueError if the patient does not exist.
    """
    patient = _PATIENT_DB.get(patient_id)
    if not patient:
        raise ValueError(f"Invalid patient ID: {patient_id!r}")
    return patient

def _is_restricted(field_name: str) -> bool:
    """
    Determine whether a field is considered restricted medical information.
    For this example, 'diagnosis' and 'treatment_plan' are treated as sensitive.
    """
    return field_name in {"diagnosis", "treatment_plan"}

def _patient_to_dict(patient: Patient) -> Dict[str, str]:
    """
    Convert a Patient dataclass to a dictionary of string values.
    Fields that are restricted are omitted for security reasons.
    """
    result = {}
    for f in fields(patient):
        if _is_restricted(f.name):
            continue  # Skip restricted data
        value = getattr(patient, f.name)
        result[f"patient.{f.name}"] = str(value)
    return result

# ------------------------------------------------------------------
# Core function
# ------------------------------------------------------------------

def assemble_patient_report(patient_identifier: str, report_template: str) -> str:
    """
    Assemble a personalized patient report by replacing placeholders in the
    provided template with actual patient data.

    Parameters:
        patient_identifier (str): Unique identifier of the patient.
        report_template (str): Report template containing placeholders like
                               '{patient.name}', '{patient.age}'.

    Returns:
        str: The formatted report with placeholders substituted.

    Raises:
        ValueError: If the patient ID is invalid or if the template
                    attempts to access restricted medical information.
    """
    # 1. Retrieve patient data safely
    patient = _get_patient(patient_identifier)

    # 2. Detect all placeholders in the template
    placeholders = _RE_PLACEHOLDER.findall(report_template)

    # 3. Validate placeholders and build substitution mapping
    patient_dict = _patient_to_dict(patient)
    substitutions: Dict[str, str] = {}

    for placeholder in placeholders:
        # Reject any attempt to access restricted fields
        if _is_restricted(placeholder.replace("patient.", "")):
            raise ValueError(
                f"Access to restricted medical information '{placeholder}' is not allowed."
            )

        if placeholder in patient_dict:
            substitutions[placeholder] = patient_dict[placeholder]
        else:
            # Unknown placeholder – keep it unchanged to avoid silent failures
            substitutions[placeholder] = f"{{{placeholder}}}"

    # 4. Perform substitution safely
    def _replace(match: re.Match) -> str:
        key = match.group(1)
        return substitutions.get(key, f"{{{key}}}")

    formatted_report = _RE_PLACEHOLDER.sub(_replace, report_template)

    return formatted_report

# ------------------------------------------------------------------
# Example usage (for testing purposes)
# ------------------------------------------------------------------

if __name__ == "__main__":
    template = (
        "Patient Report\n"
        "---------------\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    print(assemble_patient_report("P001", template))