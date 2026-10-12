import re
from dataclasses import dataclass, asdict

# --------------------------------------------------------------------
# Mock data store (in a real system this would be a database or
# external service).  The dictionary maps learner codes to Student
# instances.  In a real application the data would be securely stored.
# --------------------------------------------------------------------
_STUDENT_DB = {}

@dataclass
class Student:
    """Simple representation of a student record."""
    learner_code: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str
    disciplinary_record: str  # Sensitive information


# --------------------------------------------------------------------
# Populate the mock database with a few example students.
# In practice, this would be replaced by a call to the data layer.
# --------------------------------------------------------------------
def _initialize_mock_db():
    global _STUDENT_DB
    _STUDENT_DB = {
        "S001": Student(
            learner_code="S001",
            name="Alice Johnson",
            course="Computer Science",
            age=20,
            gpa=3.8,
            home_address="123 Maple St, Springfield",
            disciplinary_record="None"
        ),
        "S002": Student(
            learner_code="S002",
            name="Bob Smith",
            course="Mechanical Engineering",
            age=22,
            gpa=3.4,
            home_address="456 Oak Ave, Shelbyville",
            disciplinary_record="Late submission of project"
        ),
    }

_initialize_mock_db()

# --------------------------------------------------------------------
# Allowed placeholders that are considered non‑sensitive.
# Any placeholder not in this set will cause a ValueError to be raised.
# --------------------------------------------------------------------
_ALLOWED_PLACEHOLDERS = {
    "student.name",
    "student.course",
    "student.age",
    "student.gpa",
    "student.home_address"
}

# --------------------------------------------------------------------
# Helper function to safely format the template.
# --------------------------------------------------------------------
def _safe_format(template: str, student: Student) -> str:
    """
    Replace placeholders in the template with actual student data.
    Raises ValueError if a restricted placeholder is found or if
    the template contains an invalid placeholder syntax.
    """
    # Find all placeholders of the form {student.attribute}
    pattern = re.compile(r"{\s*([^}]+)\s*}")
    matches = pattern.findall(template)

    for placeholder in matches:
        # Normalize placeholder name
        key = f"student.{placeholder}"
        if key not in _ALLOWED_PLACEHOLDERS:
            raise ValueError(f"Access to restricted or unknown attribute '{placeholder}' is not allowed.")

        # Retrieve the value from the student object
        value = getattr(student, placeholder, None)
        if value is None:
            raise ValueError(f"Student attribute '{placeholder}' does not exist.")

        # Replace the placeholder with its value
        template = template.replace(f"{{{placeholder}}}", str(value))

    return template

# --------------------------------------------------------------------
# Main function as requested
# --------------------------------------------------------------------
def compile_student_profile(learner_code: str, profile_template: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    learner_code : str
        Unique identifier for a student.
    profile_template : str
        String containing placeholders to be replaced with actual data.

    Returns
    -------
    str
        The formatted student report.

    Raises
    ------
    ValueError
        If the learner code is invalid, or if the template contains
        restricted or non‑existent placeholders.
    """
    # Validate learner code and fetch the student record
    student = _STUDENT_DB.get(learner_code)
    if not student:
        raise ValueError(f"Invalid learner code: '{learner_code}'")

    # Safely format the template
    return _safe_format(profile_template, student)


# --------------------------------------------------------------------
# Example usage (uncomment to test)
# --------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa}\n"
        "Address: {student.home_address}"
    )
    try:
        report = compile_student_profile("S001", template)
        print(report)
    except ValueError as e:
        print(f"Error: {e}")