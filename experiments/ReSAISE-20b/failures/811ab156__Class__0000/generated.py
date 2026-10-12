import re
from dataclasses import dataclass, asdict

# ----------------------------------------------------------------------
# Mock patient registry (in a real system this would be a database lookup)
# ----------------------------------------------------------------------
_PATIENT_REGISTRY = {
    "P001": {"name": "Alice Smith",   "age": 29, "gender": "F",
             "diagnosis": "Hypertension", "treatment_plan": "Medication A"},
    "P002": {"name": "Bob Johnson",   "age": 45, "gender": "M",
             "diagnosis": "Diabetes",     "treatment_plan": "Insulin therapy"},
    # Add more patients as needed
}

# ----------------------------------------------------------------------
# Patient data model
# ----------------------------------------------------------------------
@dataclass
class Patient:
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str

# ----------------------------------------------------------------------
# Helper to safely format strings with patient data
# ----------------------------------------------------------------------
class SafeFormatter:
    """
    A formatter that raises a ValueError if a placeholder is missing
    from the mapping or refers to restricted data.
    """
    # Fields that are considered sensitive (should not be exposed)
    _RESTRICTED_FIELDS = {"diagnosis", "treatment_plan"}

    def __init__(self, mapping: dict):
        self.mapping = mapping

    def format(self, template: str) -> str:
        # Find all placeholders in the template
        placeholder_pattern = r"\{([^{}]+)\}"
        placeholders = re.findall(placeholder_pattern, template)

        for placeholder in placeholders:
            # Allow only the 'patient.<field>' syntax
            if not placeholder.startswith("patient."):
                raise ValueError(f"Unsupported placeholder '{placeholder}'")

            field_name = placeholder.split(".", 1)[1]
            if field_name in self._RESTRICTED_FIELDS:
                raise ValueError(f"Access to restricted field '{field_name}' is denied")

            if field_name not in self.mapping:
                raise ValueError(f"Patient data does not contain field '{field_name}'")

        # Perform formatting
        try:
            return template.format(**{f"patient.{k}": v for k, v in self.mapping.items()})
        except KeyError as exc:
            raise ValueError(f"Missing field in patient data: {exc}") from None

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def assemble_patient_report(patient_identifier: str, report_template: str) -> str:
    """
    Generates a personalized patient report by replacing placeholders in the
    provided template with actual patient data.

    Parameters:
        patient_identifier (str): Unique ID of the patient.
        report_template (str): Report template containing placeholders like
                               '{patient.name}', '{patient.age}', etc.

    Returns:
        str: The fully formatted report string.

    Raises:
        ValueError: If the patient ID is invalid, if a restricted field
                    is accessed, or if placeholders are malformed.
    """
    # 1. Validate patient identifier
    patient_data = _PATIENT_REGISTRY.get(patient_identifier)
    if not patient_data:
        raise ValueError(f"Invalid patient identifier: {patient_identifier}")

    # 2. Construct Patient object
    patient = Patient(**patient_data)

    # 3. Prepare data mapping for formatting
    mapping = asdict(patient)

    # 4. Format the template safely
    formatter = SafeFormatter(mapping)
    return formatter.format(report_template)

# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Patient Report\n"
        "==============\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    try:
        report = assemble_patient_report("P001", template)
        print(report)
    except ValueError as e:
        print(f"Error: {e}")