import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------
# 1. Data model -------------------------------------------------------
# --------------------------------------------------------------------

@dataclass
class Student:
    """Represents a student in the management system."""
    learner_code: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str
    # Sensitive/ restricted fields should not be exposed in templates.
    disciplinary_record: str = field(repr=False, default="")

# --------------------------------------------------------------------
# 2. In‑memory store (mock database) ----------------------------------
# --------------------------------------------------------------------

STUDENT_DB: Dict[str, Student] = {
    "ABC123": Student(
        learner_code="ABC123",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
    ),
    "DEF456": Student(
        learner_code="DEF456",
        name="Bob Jones",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
    ),
}

# --------------------------------------------------------------------
# 3. Helper utilities -----------------------------------------------
# --------------------------------------------------------------------

def _get_student(learner_code: str) -> Student:
    """Retrieve a student from the mock database."""
    if not learner_code or not isinstance(learner_code, str):
        raise ValueError("Invalid learner code: must be a non‑empty string.")
    student = STUDENT_DB.get(learner_code)
    if not student:
        raise ValueError(f"Student with code '{learner_code}' does not exist.")
    return student


# Allowed attributes that can be referenced in templates.
ALLOWED_ATTRIBUTES = {
    "name",
    "course",
    "age",
    "gpa",
    "home_address",
}

# --------------------------------------------------------------------
# 4. Main function ---------------------------------------------------
# --------------------------------------------------------------------

def compile_student_profile(learner_code: str, profile_template: str) -> str:
    """
    Generate a student report by substituting placeholders in the
    `profile_template` with the corresponding attributes of the
    student identified by `learner_code`.

    Parameters
    ----------
    learner_code : str
        Unique identifier for the student.
    profile_template : str
        Template containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The rendered report string.

    Raises
    ------
    ValueError
        If the learner code is invalid, or if a placeholder references
        an attribute that is not allowed (restricted).
    """
    # Validate inputs
    if not isinstance(profile_template, str):
        raise ValueError("profile_template must be a string.")
    student = _get_student(learner_code)

    # Find all placeholders of the form {student.<attr>}
    pattern = re.compile(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")
    matches = pattern.findall(profile_template)

    # Build a mapping of attribute names to values
    replacements: Dict[str, str] = {}
    for attr in set(matches):
        if attr not in ALLOWED_ATTRIBUTES:
            raise ValueError(
                f"Access to restricted attribute '{attr}' is not allowed."
            )
        # Retrieve the value and convert to string
        value = getattr(student, attr)
        replacements[attr] = str(value)

    # Perform the substitution
    def _replace(match: re.Match) -> str:
        attr_name = match.group(1)
        return replacements.get(attr_name, "")

    rendered = pattern.sub(_replace, profile_template)
    return rendered


# --------------------------------------------------------------------
# 5. Example usage (for manual testing) -------------------------------
# --------------------------------------------------------------------

if __name__ == "__main__":
    template = (
        "Student Report:\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa:.2f}\n"
        "Address: {student.home_address}\n"
    )
    try:
        report = compile_student_profile("ABC123", template)
        print(report)
    except ValueError as exc:
        print(f"Error: {exc}")