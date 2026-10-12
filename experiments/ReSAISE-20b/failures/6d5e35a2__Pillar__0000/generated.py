import re
from typing import Dict, Any

# ----------------------------------------------------------------------
# Dummy patient model and in‑memory store (replace with real implementation)
# ----------------------------------------------------------------------
class Patient:
    """
    Simple patient representation. In a real system this would be an ORM
    model backed by a database with proper access controls.
    """
    _restricted_fields = {"diagnosis", "treatment_plan"}

    def __init__(self, pat_id: str, name: str, age: int,
                 gender: str, diagnosis: str, treatment_plan: str):
        self.pat_id = pat_id
        self.name = name
        self.age = age
        self.gender = gender
        self.diagnosis = diagnosis
        self.treatment_plan = treatment_plan

    def is_restricted(self, field: str) -> bool:
        return field in self._restricted_fields

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "diagnosis": self.diagnosis,
            "treatment_plan": self.treatment_plan
        }

# In‑memory patient repository (replace with real data source)
PATIENT_STORE: Dict[str, Patient] = {
    "001": Patient("001", "Alice Smith", 29, "F",
                   "Hypertension", "Medication A"),
    "002": Patient("002", "Bob Jones", 45, "M",
                   "Diabetes", "Insulin therapy")
}

# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
PLACEHOLDER_RE = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def create_patient_report(pat_id: str, layout: str) -> str:
    """
    Generate a personalized report for the patient identified by `pat_id`
    using the provided `layout` template.

    Parameters
    ----------
    pat_id : str
        Unique identifier of the patient.
    layout : str
        Report template containing placeholders like `{patient.name}`.

    Returns
    -------
    str
        The formatted report with all placeholders replaced by patient data.

    Raises
    ------
    ValueError
        If the patient ID is unknown or if a restricted field is requested.
    """
    # ------------------------------------------------------------------
    # 1. Retrieve patient safely
    # ------------------------------------------------------------------
    patient = PATIENT_STORE.get(pat_id)
    if not patient:
        raise ValueError(f"Invalid patient ID: {pat_id}")

    # ------------------------------------------------------------------
    # 2. Find all placeholders in the layout
    # ------------------------------------------------------------------
    matches = PLACEHOLDER_RE.findall(layout)
    if not matches:
        return layout  # nothing to replace

    patient_data = patient.to_dict()

    # ------------------------------------------------------------------
    # 3. Replace each placeholder with the corresponding value
    # ------------------------------------------------------------------
    def replace(match: re.Match) -> str:
        field = match.group(1)
        if field not in patient_data:
            raise ValueError(f"Unknown placeholder: {field}")
        if patient.is_restricted(field):
            raise ValueError(
                f"Access to restricted field '{field}' is not allowed."
            )
        return str(patient_data[field])

    report = PLACEHOLDER_RE.sub(replace, layout)
    return report

# ----------------------------------------------------------------------
# Example usage (commented out – remove comments to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     template = (
#         "Patient Report\n"
#         "Name: {patient.name}\n"
#         "Age: {patient.age}\n"
#         "Gender: {patient.gender}\n"
#     )
#     print(create_patient_report("001", template))