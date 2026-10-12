import re
from typing import Dict

# ------------------------------------------------------------------
# Mock student database (in a real system this would be a DB or API)
# ------------------------------------------------------------------
_STUDENT_DB: Dict[str, "Student"] = {}

class Student:
    """
    A simple student data holder.
    Sensitive attributes: home_address, disciplinary_record
    """
    def __init__(self, stu_id: str, name: str, course: str,
                 age: int, gpa: float, home_address: str,
                 disciplinary_record: str):
        self.stu_id = stu_id
        self.name = name
        self.course = course
        self.age = age
        self.gpa = gpa
        self.home_address = home_address  # Sensitive
        self.disciplinary_record = disciplinary_record  # Sensitive

# Populate mock DB with a sample student
_STUDENT_DB["12345"] = Student(
    stu_id="12345",
    name="Alice Smith",
    course="Computer Science",
    age=20,
    gpa=3.8,
    home_address="123 Maple Street, Springfield",
    disciplinary_record="None"
)

# ------------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------------
def _get_student(stu_id: str) -> Student:
    """
    Retrieve a student from the mock database.
    Raises ValueError if ID is not found.
    """
    student = _STUDENT_DB.get(stu_id)
    if not student:
        raise ValueError(f"Invalid student ID: {stu_id}")
    return student

def _safe_attribute_get(obj, attr_name: str):
    """
    Safely retrieve an attribute from an object.
    Raises ValueError if the attribute is sensitive or does not exist.
    """
    # Define attributes that are considered sensitive
    SENSITIVE_ATTRS = {"home_address", "disciplinary_record"}
    if attr_name in SENSITIVE_ATTRS:
        raise ValueError(f"Access to sensitive attribute '{attr_name}' is forbidden.")
    if not hasattr(obj, attr_name):
        raise ValueError(f"Attribute '{attr_name}' does not exist.")
    return getattr(obj, attr_name)

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def create_student_summary(stu_id: str, summary_template: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    stu_id : str
        Unique identifier for a student.
    summary_template : str
        A string containing placeholders in the form '{student.attribute}'.

    Returns
    -------
    str
        The formatted student report.

    Raises
    ------
    ValueError
        If the student ID is invalid or if a placeholder references a sensitive attribute.
    """
    # Retrieve the student object
    student = _get_student(stu_id)

    # Find all placeholders in the template: {student.attribute}
    placeholder_pattern = re.compile(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")
    placeholders = placeholder_pattern.findall(summary_template)

    # Build a mapping from attribute name to its value
    attr_values: Dict[str, str] = {}
    for attr in set(placeholders):
        value = _safe_attribute_get(student, attr)
        # Convert to string for safe formatting
        attr_values[attr] = str(value)

    # Replace placeholders with actual values
    def replacement(match):
        attr_name = match.group(1).strip()
        return attr_values.get(attr_name, f"{{student.{attr_name}}}")  # Fallback

    result = placeholder_pattern.sub(replacement, summary_template)
    return result