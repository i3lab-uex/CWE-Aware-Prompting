from dataclasses import dataclass, asdict
import re

# --------------------------------------------------------------------------- #
# Mock data and classes (replace with real implementations in production)
# --------------------------------------------------------------------------- #

@dataclass
class Patient:
    """Simple patient record."""
    code: str          # unique identifier (e.g., MRN)
    name: str
    age: int
    gender: str
    diagnosis: str     # sensitive
    treatment_plan: str  # sensitive


# In-memory patient store (replace with DB access in real system)
PATIENT_DB = {
    "001": Patient(
        code="001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    "002": Patient(
        code="002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Asthma",
        treatment_plan="Inhaler B, Avoid triggers"
    ),
}


# --------------------------------------------------------------------------- #
# Utility functions
# --------------------------------------------------------------------------- #

def _get_patient_by_code(code: str) -> Patient:
    """Retrieve a patient record by code or raise ValueError."""
    patient = PATIENT_DB.get(code)
    if not patient:
        raise ValueError(f"Patient with code '{code}' not found.")
    return patient


def _extract_placeholders(template: str) -> set:
    """
    Extract placeholder names from a format string.
    Supports nested attributes like {patient.name}.
    Returns a set of attribute names (e.g., {'name', 'age'}).
    """
    # Regex matches {something} but ignores escaped braces
    pattern = r"{([^{}]+)}"
    placeholders = set(re.findall(pattern, template))
    # Only keep the last attribute after dot if nested
    return {p.split(".")[-1] for p in placeholders}


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def create_person_report(patient_code: str, report_template: str) -> str:
    """
    Generate a patient report based on the provided template.

    Parameters
    ----------
    patient_code : str
        The unique identifier for the patient.
    report_template : str
        A format string containing placeholders such as '{patient.name}'.

    Returns
    -------
    str
        The formatted report string containing only non-sensitive data.

    Raises
    ------
    ValueError
        If the patient code is not found, or if the template attempts to
        access sensitive information (diagnosis or treatment_plan).
    """
    # Retrieve patient record
    patient = _get_patient_by_code(patient_code)

    # Determine allowed attributes (non-sensitive)
    allowed_attrs = {"name", "age", "gender"}

    # Inspect placeholders in template
    placeholders = _extract_placeholders(report_template)

    # Check for disallowed fields
    if not placeholders.issubset(allowed_attrs):
        disallowed = placeholders.difference(allowed_attrs)
        raise ValueError(
            f"Template contains disallowed fields: {', '.join(disallowed)}"
        )

    # Build a mapping for formatting
    patient_dict = asdict(patient)
    context = {"patient": {k: v for k, v in patient_dict.items() if k in allowed_attrs}}

    # Perform formatting
    try:
        report = report_template.format(**context)
    except KeyError as e:
        # This should not happen if placeholders were validated
        raise ValueError(f"Missing placeholder in context: {e}") from e

    return report


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = "Patient {patient.name} (Age: {patient.age}) is a {patient.gender}."
    print(create_person_report("001", template))