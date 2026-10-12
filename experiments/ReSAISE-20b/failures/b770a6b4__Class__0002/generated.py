import re
from dataclasses import dataclass, asdict
from typing import Dict

# ------------------------------------------------------------------
# Student data model and registry (mocked for demonstration)
# ------------------------------------------------------------------

@dataclass
class Student:
    """Simple student record."""
    code: str          # unique identifier
    name: str
    course: str
    age: int
    gpa: float
    home_address: str            # sensitive
    disciplinary_record: str     # sensitive

# In a real system this would be replaced by a database or secure store
_STUDENT_REGISTRY: Dict[str, Student] = {
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
        disciplinary_record="Late submission of Assignment 3"
    ),
}

# ------------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------------

def _get_student_by_code(code: str) -> Student:
    """Retrieve a student by code or raise ValueError if not found."""
    student = _STUDENT_REGISTRY.get(code)
    if not student:
        raise ValueError(f"Student ID '{code}' is invalid.")
    return student

def _extract_placeholders(template: str) -> set:
    """
    Extract placeholder names from a format string.
    Handles nested braces and ignores literal braces.
    """
    # Regex to find {field} or {field:format}
    pattern = r"\{(?P<name>[^{}]+?)\}"
    return {m.group("name").split(":")[0].strip() for m in re.finditer(pattern, template)}

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------

def compile_student_profile(learner_code: str, profile_template: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    learner_code : str
        Unique identifier for the student.
    profile_template : str
        Template containing placeholders like '{student.name}'.

    Returns
    -------
    str
        Rendered report string.

    Raises
    ------
    ValueError
        If the student ID is invalid or if the template references
        restricted/sensitive attributes.
    """
    # Retrieve student record safely
    student = _get_student_by_code(learner_code)

    # Define which attributes are safe to expose
    SAFE_FIELDS = {"name", "course", "age", "gpa"}

    # Parse placeholders from the template
    placeholders = _extract_placeholders(profile_template)

    # Validate placeholders
    for placeholder in placeholders:
        # The template might use a prefix like 'student.name'
        field_name = placeholder.split(".")[-1]  # take the last part after dot
        if field_name not in SAFE_FIELDS:
            raise ValueError(f"Access to restricted attribute '{field_name}' is denied.")

    # Prepare a mapping with only safe attributes
    student_dict = asdict(student)
    context = {k: v for k, v in student_dict.items() if k in SAFE_FIELDS}

    # Replace 'student.' prefix with empty string for formatting
    cleaned_template = re.sub(r"\bstudent\.", "", profile_template)

    try:
        report = cleaned_template.format(**context)
    except KeyError as e:
        # This should not happen due to earlier validation, but guard anyway
        raise ValueError(f"Missing data for placeholder: {e}")

    return report

# ------------------------------------------------------------------
# Example usage (for testing purposes only)
# ------------------------------------------------------------------

if __name__ == "__main__":
    template = (
        "Student Report\n"
        "---------------\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa:.2f}"
    )
    print(compile_student_profile("S001", template))