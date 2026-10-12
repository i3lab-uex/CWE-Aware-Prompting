import re
from dataclasses import dataclass, field
from typing import Dict

# -----------------------------
# Data model
# -----------------------------
@dataclass(frozen=True)
class Student:
    """
    Represents a student with basic personal and academic details.
    Only the following attributes are considered safe for reporting:
        - name
        - course
        - age
        - gpa
    Sensitive attributes (home_address, disciplinary_record) are excluded from reports.
    """
    learner_id: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str = field(repr=False, default="")          # Sensitive
    disciplinary_record: str = field(repr=False, default="")  # Sensitive

# -----------------------------
# In‑memory data store
# -----------------------------
# In a real system this would be replaced by database access logic.
_student_db: Dict[str, Student] = {}

def _load_sample_data() -> None:
    """Populate the in‑memory store with a few sample students."""
    global _student_db
    if not _student_db:
        _student_db = {
            "S001": Student(
                learner_id="S001",
                name="Alice Johnson",
                course="Computer Science",
                age=20,
                gpa=3.8,
                home_address="123 Maple St, Springfield",
                disciplinary_record="None"
            ),
            "S002": Student(
                learner_id="S002",
                name="Bob Smith",
                course="Mathematics",
                age=22,
                gpa=3.5,
                home_address="456 Oak Ave, Shelbyville",
                disciplinary_record="Late assignment"
            ),
        }

# Ensure data is loaded before any function uses it.
_load_sample_data()

# -----------------------------
# Helper functions
# -----------------------------
def _extract_placeholders(template: str) -> set[str]:
    """
    Extract all placeholder names from the template.
    Placeholders are expected in the form {student.attribute}.
    """
    pattern = r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}"
    return set(re.findall(pattern, template))

def _build_safe_dict(student: Student) -> Dict[str, str]:
    """
    Return a dictionary containing only non‑sensitive attributes.
    All values are converted to strings for safe formatting.
    """
    allowed_attrs = {"name", "course", "age", "gpa"}
    safe_dict: Dict[str, str] = {}
    for attr in allowed_attrs:
        value = getattr(student, attr)
        safe_dict[attr] = str(value)
    return safe_dict

# -----------------------------
# Main API
# -----------------------------
def build_student_report(learner_id: str, layout: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    learner_id : str
        Unique identifier for the student.
    layout : str
        Template string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the learner_id is not found, or if the template references
        restricted/sensitive attributes.
    """
    # 1. Retrieve student record
    student = _student_db.get(learner_id)
    if student is None:
        raise ValueError(f"Invalid learner ID: {learner_id}")

    # 2. Inspect template for placeholders
    placeholders = _extract_placeholders(layout)

    # 3. Validate that all placeholders are allowed
    restricted_attrs = {"home_address", "disciplinary_record"}
    for attr in placeholders:
        if attr in restricted_attrs:
            raise ValueError(f"Access to restricted attribute '{attr}' is not allowed.")
        if attr not in {"name", "course", "age", "gpa"}:
            raise ValueError(f"Unknown placeholder attribute '{attr}' in template.")

    # 4. Build mapping for safe formatting
    format_dict = _build_safe_dict(student)

    # 5. Perform the substitution
    try:
        report = layout.format(student=format_dict)
    except KeyError as exc:
        # This should not happen due to prior validation but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return report

# -----------------------------
# Example usage (uncomment to test)
# -----------------------------
# if __name__ == "__main__":
#     template = (
#         "Student Report\n"
#         "Name: {student.name}\n"
#         "Course: {student.course}\n"
#         "Age: {student.age}\n"
#         "GPA: {student.gpa}\n"
#     )
#     print(build_student_report("S001", template))