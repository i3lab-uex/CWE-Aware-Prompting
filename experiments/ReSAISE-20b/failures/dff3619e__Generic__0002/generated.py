import re
from dataclasses import dataclass, fields
from typing import Dict

# ----------------------------------------------------
# Basic in‑memory student store (for demo purposes)
# ----------------------------------------------------

@dataclass
class Student:
    """Represents a student profile."""
    id: str
    name: str
    course: str
    age: int
    gpa: float
    address: str
    disciplinary_record: str  # considered sensitive


# Example data – in a real system this would come from a database
STUDENT_DB: Dict[str, Student] = {
    "s001": Student(
        id="s001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        address="123 Maple Ave, Townsville",
        disciplinary_record="None"
    ),
    "s002": Student(
        id="s002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        gpa=3.5,
        address="456 Oak St, Villageton",
        disciplinary_record="Late submission of assignment 3"
    ),
}


# ----------------------------------------------------
# Helper utilities
# ----------------------------------------------------

def _extract_placeholders(template: str) -> set[str]:
    """
    Return a set of placeholder names found in the template.
    Placeholders are expected to be of the form {student.attr}.
    """
    return set(re.findall(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}", template))


def _validate_placeholders(placeholders: set[str]) -> None:
    """
    Ensure that placeholders reference only allowed attributes.
    Raise ValueError if a restricted attribute is requested or
    an unknown attribute is used.
    """
    # Allowed attributes – everything except 'disciplinary_record'
    allowed_attrs = {f.name for f in fields(Student) if f.name != "disciplinary_record"}

    for attr in placeholders:
        if attr not in allowed_attrs:
            raise ValueError(
                f"Access to restricted or unknown attribute '{attr}' is not allowed."
            )


# ----------------------------------------------------
# Main function
# ----------------------------------------------------

def build_student_report(learner_id: str, layout: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    learner_id : str
        Unique identifier for a student.
    layout : str
        A string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the learner_id is invalid or if the template tries to access
        restricted/sensitive information.
    """
    # 1. Validate learner ID
    student = STUDENT_DB.get(learner_id)
    if not student:
        raise ValueError(f"Invalid learner ID: {learner_id}")

    # 2. Parse and validate placeholders
    placeholders = _extract_placeholders(layout)
    _validate_placeholders(placeholders)

    # 3. Prepare a mapping for formatting
    student_dict = {field.name: getattr(student, field.name) for field in fields(Student)}

    # 4. Replace placeholders with actual values
    def replace(match: re.Match) -> str:
        attr_name = match.group(1)
        return str(student_dict[attr_name])

    report = re.sub(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}", replace, layout)

    return report


# ----------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------

# if __name__ == "__main__":
#     tmpl = (
#         "Student Report\n"
#         "Name: {student.name}\n"
#         "Course: {student.course}\n"
#         "Age: {student.age}\n"
#         "GPA: {student.gpa}\n"
#         "Address: {student.address}"
#     )
#     print(build_student_report("s001", tmpl))