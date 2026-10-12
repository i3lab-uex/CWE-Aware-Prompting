import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------
# Domain model: Student
# ------------------------------------------------------------

@dataclass(frozen=True)
class Student:
    """Immutable representation of a student."""
    learner_code: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str
    disciplinary_record: str = field(repr=False)  # sensitive, not exposed

# ------------------------------------------------------------
# In‑memory “database” of students
# ------------------------------------------------------------

_STUDENT_DB: Dict[str, Student] = {
    "A123": Student(
        learner_code="A123",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        disciplinary_record="None"
    ),
    "B456": Student(
        learner_code="B456",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        disciplinary_record="Late assignment on 2024-02-15"
    ),
}

# ------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------

_ALLOWED_FIELDS = {
    "name",
    "course",
    "age",
    "gpa",
    "home_address",
}

_PLACEHOLDER_RE = re.compile(r"\{student\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def _replace_placeholders(template: str, student: Student) -> str:
    """
    Replace placeholders of the form {student.<field>} with
    corresponding student attributes.

    Raises ValueError if a placeholder refers to a disallowed field.
    """
    def repl(match: re.Match) -> str:
        attr = match.group(1)
        if attr not in _ALLOWED_FIELDS:
            raise ValueError(f"Access to restricted attribute '{attr}' is not allowed.")
        value = getattr(student, attr)
        return str(value)

    # Perform substitution
    result = _PLACEHOLDER_RE.sub(repl, template)
    return result

# ------------------------------------------------------------
# Main function
# ------------------------------------------------------------

def compile_student_profile(learner_code: str, profile_template: str) -> str:
    """
    Generate a student report by replacing placeholders in the provided template.

    Parameters
    ----------
    learner_code : str
        Unique identifier of the student.
    profile_template : str
        Template string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The populated report string.

    Raises
    ------
    ValueError
        If the learner_code is not found or a restricted attribute is referenced.
    """
    # Retrieve student record
    try:
        student = _STUDENT_DB[learner_code]
    except KeyError as exc:
        raise ValueError(f"Student with code '{learner_code}' does not exist.") from exc

    # Replace placeholders safely
    return _replace_placeholders(profile_template, student)

# ------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------

# if __name__ == "__main__":
#     template = (
#         "Student Report:\n"
#         "Name: {student.name}\n"
#         "Course: {student.course}\n"
#         "Age: {student.age}\n"
#         "GPA: {student.gpa}\n"
#         "Address: {student.home_address}"
#     )
#     print(compile_student_profile("A123", template))