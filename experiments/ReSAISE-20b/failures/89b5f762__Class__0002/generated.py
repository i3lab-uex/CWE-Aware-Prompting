import re
from dataclasses import dataclass, field
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# 1. Domain model – Patient
# --------------------------------------------------------------------------- #

@dataclass
class Patient:
    """
    Represents a patient record in the system.

    Only the attributes listed in `ALLOWED_FIELDS` may be exposed to
    unauthorized users.  Attempting to access any other attribute will
    raise a ValueError.
    """
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str

    # Attributes that are *not* allowed to be exposed.
    _restricted_fields = {"diagnosis", "treatment_plan"}

    def __post_init__(self) -> None:
        # Validate that patient_id is a non-empty string.
        if not isinstance(self.patient_id, str) or not self.patient_id.strip():
            raise ValueError("patient_id must be a non-empty string")

    @property
    def allowed_fields(self) -> set[str]:
        """Return the set of attributes that can be safely exposed."""
        return {
            attr for attr in self.__dict__
            if not attr.startswith("_") and attr not in self._restricted_fields
        }

# --------------------------------------------------------------------------- #
# 2. In‑memory patient store (for demo purposes)
# --------------------------------------------------------------------------- #

_patient_store: Dict[str, Patient] = {}

def _seed_demo_data() -> None:
    """Populate the store with a few demo patients."""
    global _patient_store
    _patient_store = {
        "p001": Patient(
            patient_id="p001",
            name="Alice Smith",
            age=30,
            gender="F",
            diagnosis="Hypertension",
            treatment_plan="Medication A, Lifestyle changes"
        ),
        "p002": Patient(
            patient_id="p002",
            name="Bob Jones",
            age=45,
            gender="M",
            diagnosis="Diabetes",
            treatment_plan="Insulin therapy"
        ),
    }

_seed_demo_data()

# --------------------------------------------------------------------------- #
# 3. Core function – generate_patient_summary
# --------------------------------------------------------------------------- #

PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z_][\w\.]*)\}")

def generate_patient_summary(patient_id: str, report_template: str) -> str:
    """
    Return a string with patient data filled into the provided template.

    Parameters
    ----------
    patient_id : str
        The unique identifier for the patient.
    report_template : str
        A string containing placeholders like '{patient.name}' or
        '{patient.age}'.  The template must reference only allowed fields.

    Returns
    -------
    str
        The fully rendered report.

    Raises
    ------
    ValueError
        If the patient_id is not found, or if the template attempts to
        access a restricted field.
    """
    # --------------------------------------------------------------------- #
    # 1. Retrieve patient
    # --------------------------------------------------------------------- #
    patient = _patient_store.get(patient_id)
    if not patient:
        raise ValueError(f"Patient ID '{patient_id}' is invalid.")

    # --------------------------------------------------------------------- #
    # 2. Find placeholders
    # --------------------------------------------------------------------- #
    placeholders = PLACEHOLDER_RE.findall(report_template)

    # If no placeholders, just return the template unchanged
    if not placeholders:
        return report_template

    # --------------------------------------------------------------------- #
    # 3. Resolve each placeholder
    # --------------------------------------------------------------------- #
    resolved_values: Dict[str, Any] = {}
    for ph in placeholders:
        # The placeholder is expected to be of the form 'patient.<attr>'
        if not ph.startswith("patient."):
            raise ValueError(f"Unsupported placeholder '{ph}'. Only patient attributes are allowed.")
        attr_name = ph.split(".", 1)[1]

        # Check that the attribute is allowed
        if attr_name not in patient.allowed_fields:
            raise ValueError(f"Access to restricted attribute '{attr_name}' is not permitted.")

        # Retrieve the value
        try:
            value = getattr(patient, attr_name)
        except AttributeError:
            raise ValueError(f"Attribute '{attr_name}' does not exist on patient.")

        resolved_values[ph] = str(value)

    # --------------------------------------------------------------------- #
    # 4. Replace placeholders in the template
    # --------------------------------------------------------------------- #
    def _replace(match: re.Match) -> str:
        key = match.group(1)
        return resolved_values.get(key, match.group(0))

    rendered_report = PLACEHOLDER_RE.sub(_replace, report_template)
    return rendered_report

# --------------------------------------------------------------------------- #
# 4. Example usage (commented out – remove comments to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     template = "Patient Report:\nName: {patient.name}\nAge: {patient.age}\nGender: {patient.gender}"
#     print(generate_patient_summary("p001", template))