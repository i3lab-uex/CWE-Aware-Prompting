import re
from dataclasses import dataclass, fields
from typing import Dict

# ----------------------------------------------------------------------
# Data model and in‑memory storage (mock database)
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    name: str
    course: str
    age: int
    GPA: float          # Sensitive – must never be exposed
    home_address: str   # Sensitive – must never be exposed
    discipline_record: str

# Mock database of students keyed by their unique ID
STUDENTS_DB: Dict[str, Student] = {
    "S001": Student(
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        name="Bob Smith",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission"
    ),
    # Add more students as needed
}

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
_SENSITIVE_FIELDS = {"GPA", "home_address"}

def _extract_placeholders(template: str):
    """
    Return a set of placeholder names found in the template.
    Placeholders are expected to be in Python format syntax:
        {object.attribute}
    """
    # Regex finds all substrings like {something}
    pattern = r"\{([^{}]+)\}"
    return set(re.findall(pattern, template))

def _validate_placeholders(placeholders: set):
    """
    Raise ValueError if any placeholder refers to a sensitive attribute.
    Only 'student' objects are allowed in this context.
    """
    for placeholder in placeholders:
        parts = placeholder.split(".")
        # We expect exactly two parts: object and attribute
        if len(parts) != 2:
            raise ValueError(f"Invalid placeholder syntax: '{placeholder}'")
        obj_name, attr_name = parts
        if obj_name != "student":
            raise ValueError(f"Unsupported object '{obj_name}' in placeholder")
        if attr_name in _SENSITIVE_FIELDS:
            raise ValueError(f"Access to sensitive field '{attr_name}' is forbidden")

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def produce_student_report(stu_id: str, custom_template: str) -> str:
    """
    Generate a formatted student report based on the provided template.

    Parameters
    ----------
    stu_id : str
        Unique identifier of the student.
    custom_template : str
        A format string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student ID does not exist, or if the template tries to access
        sensitive attributes (GPA, home_address), or contains malformed placeholders.
    """
    # 1. Retrieve student
    try:
        student = STUDENTS_DB[stu_id]
    except KeyError as exc:
        raise ValueError(f"Student ID '{stu_id}' not found") from exc

    # 2. Validate placeholders
    placeholders = _extract_placeholders(custom_template)
    _validate_placeholders(placeholders)

    # 3. Format the string
    try:
        report = custom_template.format(student=student)
    except AttributeError as exc:
        # This should not happen due to prior validation, but guard anyway
        raise ValueError(f"Formatting error: {exc}") from exc

    return report

# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "---------------\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "Discipline Record: {student.discipline_record}\n"
    )
    print(produce_student_report("S001", template))