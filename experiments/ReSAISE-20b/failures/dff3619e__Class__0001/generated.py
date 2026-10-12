import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Student model
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    """Represents a student with personal and academic data."""
    id: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str = field(repr=False)          # Sensitive data
    disciplinary_record: str = field(repr=False)   # Sensitive data


# ----------------------------------------------------------------------
# In‑memory student repository
# ----------------------------------------------------------------------
_students: Dict[str, Student] = {
    "S001": Student(
        id="S001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple Street, Springfield",
        disciplinary_record="None"
    ),
    "S002": Student(
        id="S002",
        name="Bob Johnson",
        course="Mechanical Engineering",
        age=22,
        gpa=3.4,
        home_address="456 Oak Avenue, Shelbyville",
        disciplinary_record="Late assignment on 2023-04-12"
    ),
}


# ----------------------------------------------------------------------
# Report generation
# ----------------------------------------------------------------------
ALLOWED_FIELDS = {"name", "course", "age", "gpa"}
RESTRICTED_FIELDS = {"home_address", "disciplinary_record"}

PLACEHOLDER_PATTERN = re.compile(r"\{student\.([a-zA-Z_][a-zA-Z0-9_]*)\}")


def build_student_report(learner_id: str, layout: str) -> str:
    """
    Build a student report by substituting placeholders in the given layout.

    Parameters
    ----------
    learner_id : str
        Unique identifier for the student.
    layout : str
        Report template containing placeholders such as `{student.name}`.

    Returns
    -------
    str
        The populated report string.

    Raises
    ------
    ValueError
        If the student ID is not found, or if the template attempts to
        access restricted fields.
    """
    # 1. Retrieve student data
    student = _students.get(learner_id)
    if student is None:
        raise ValueError(f"Invalid learner ID: {learner_id}")

    # 2. Find all placeholders
    matches = PLACEHOLDER_PATTERN.findall(layout)

    # 3. Validate placeholders and build substitution mapping
    substitutions = {}
    for field_name in matches:
        if field_name in RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted field '{field_name}' is not allowed.")
        if field_name not in ALLOWED_FIELDS:
            raise ValueError(f"Unknown placeholder '{field_name}'.")
        # Use getattr on the frozen dataclass
        substitutions[field_name] = str(getattr(student, field_name))

    # 4. Perform safe substitution
    def _replacer(match: re.Match) -> str:
        field = match.group(1)
        return substitutions.get(field, match.group(0))

    report = PLACEHOLDER_PATTERN.sub(_replacer, layout)
    return report


# ----------------------------------------------------------------------
# Example usage (commented out – remove to test the function)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     template = (
#         "Student Report\n"
#         "Name: {student.name}\n"
#         "Course: {student.course}\n"
#         "Age: {student.age}\n"
#         "GPA: {student.gpa}\n"
#     )
#     print(build_student_report("S001", template))