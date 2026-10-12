import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Domain model – Student
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    """Represents a student with personal and academic information."""
    code: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str | None = field(default=None, repr=False)
    disciplinary_record: str | None = field(default=None, repr=False)


# ----------------------------------------------------------------------
# In‑memory repository of students
# ----------------------------------------------------------------------
STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        code="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        disciplinary_record="None"
    ),
    "S002": Student(
        code="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        disciplinary_record="Late submission of assignment #3"
    ),
}


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_student(learner_code: str) -> Student:
    """Retrieve a student from the repository, raising ValueError if not found."""
    try:
        return STUDENT_DB[learner_code]
    except KeyError as exc:
        raise ValueError(f"Invalid learner code: {learner_code}") from exc


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def compile_student_profile(learner_code: str, profile_template: str) -> str:
    """
    Generate a student report by substituting placeholders in the provided template.

    Parameters
    ----------
    learner_code : str
        Unique identifier for a student.
    profile_template : str
        Template containing placeholders like `{student.name}`.

    Returns
    -------
    str
        The rendered report with placeholder values replaced.

    Raises
    ------
    ValueError
        If the learner code is invalid or if a placeholder refers to a restricted field.
    """
    # Allowed attributes that can appear in the template
    ALLOWED_FIELDS = {"name", "course", "age", "gpa"}

    # Retrieve the student object
    student = _get_student(learner_code)

    # Find all placeholders of the form `{student.<field>}`
    placeholder_pattern = re.compile(r"\{student\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    placeholders = placeholder_pattern.findall(profile_template)

    # Verify that each referenced field is permitted
    for field_name in placeholders:
        if field_name not in ALLOWED_FIELDS:
            raise ValueError(f"Access to restricted field '{field_name}' is not allowed")

    # Build a mapping from placeholder names to their values
    context = {f"student.{field}": getattr(student, field) for field in ALLOWED_FIELDS}

    # Perform safe substitution
    try:
        rendered = profile_template.format(**context)
    except KeyError as exc:
        # This should not happen due to the previous check, but we guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return rendered


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     template = (
#         "Student Report\n"
#         "Name: {student.name}\n"
#         "Course: {student.course}\n"
#         "Age: {student.age}\n"
#         "GPA: {student.gpa}"
#     )
#     print(compile_student_profile("S001", template))