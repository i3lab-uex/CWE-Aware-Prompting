import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------
# Data model ----------------------------------------------------------
# --------------------------------------------------------------------

@dataclass
class Student:
    """Represents a student in the system."""
    code: str
    name: str
    course: str
    age: int
    gpa: float
    address: str
    # Sensitive data that must never be exposed via the template
    disciplinary_record: Dict[str, str] = field(default_factory=dict)


# --------------------------------------------------------------------
# In‑memory data store -----------------------------------------------
# --------------------------------------------------------------------

# A simple in‑memory registry of students.
_STUDENT_REGISTRY: Dict[str, Student] = {
    "S001": Student(
        code="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        address="123 Maple St, Springfield",
    ),
    "S002": Student(
        code="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        address="456 Oak Ave, Springfield",
    ),
}


# --------------------------------------------------------------------
# Helper utilities ---------------------------------------------------
# --------------------------------------------------------------------

def _get_student(code: str) -> Student:
    """Retrieve a student by code or raise ValueError."""
    student = _STUDENT_REGISTRY.get(code)
    if not student:
        raise ValueError(f"Student with code '{code}' does not exist.")
    return student


def _sanitize_template(template: str) -> str:
    """
    Ensure the template only contains allowed placeholders.
    Allowed placeholders are of the form {student.<attribute>} where
    <attribute> is one of the non‑sensitive Student fields.
    """
    # Regex to capture placeholders like {student.name}
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")

    allowed_attrs = {"name", "course", "age", "gpa", "address"}
    for match in placeholder_pattern.finditer(template):
        key = match.group(1).strip()
        if not key.startswith("student."):
            raise ValueError(f"Disallowed placeholder '{match.group(0)}' in template.")
        attr = key.split(".", 1)[1]
        if attr not in allowed_attrs:
            raise ValueError(f"Access to restricted attribute '{attr}' is prohibited.")
    return template


# --------------------------------------------------------------------
# Main function ------------------------------------------------------
# --------------------------------------------------------------------

def compile_student_profile(learner_code: str, profile_template: str) -> str:
    """
    Generate a student report by rendering the provided template.

    Parameters
    ----------
    learner_code : str
        Unique identifier for the student.
    profile_template : str
        Template string containing placeholders such as '{student.name}'.

    Returns
    -------
    str
        The rendered report with placeholders substituted by actual data.

    Raises
    ------
    ValueError
        If the student code is invalid or if the template attempts to access
        restricted attributes.
    """
    # Retrieve student data safely
    student = _get_student(learner_code)

    # Validate the template for allowed placeholders
    sanitized_template = _sanitize_template(profile_template)

    # Build a simple mapping for format_map
    safe_dict = {
        "student.name": student.name,
        "student.course": student.course,
        "student.age": student.age,
        "student.gpa": student.gpa,
        "student.address": student.address,
    }

    # Replace placeholders
    try:
        report = sanitized_template.format(**safe_dict)
    except KeyError as exc:
        # This should never happen due to prior validation
        raise ValueError(f"Missing placeholder value for {exc}") from exc

    return report


# --------------------------------------------------------------------
# Example usage -------------------------------------------------------
# --------------------------------------------------------------------

if __name__ == "__main__":
    template = (
        "Student Report\n"
        "==============\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa}\n"
        "Address: {student.address}\n"
    )
    print(compile_student_profile("S001", template))