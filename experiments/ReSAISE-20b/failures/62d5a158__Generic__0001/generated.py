import re
from dataclasses import dataclass
from typing import Dict

# --------------------------------------------------------------------------- #
#  Student data model (simplified for this example)
# --------------------------------------------------------------------------- #

@dataclass
class Student:
    """Simple student data container."""
    name: str
    course: str
    age: int
    gpa: float
    home_address: str
    disciplinary_record: str | None = None


# --------------------------------------------------------------------------- #
#  Example data store (in a real system this would be a database)
# --------------------------------------------------------------------------- #

STUDENTS: Dict[str, Student] = {
    "S001": Student(
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        disciplinary_record=None
    ),
    "S002": Student(
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        disciplinary_record="Late assignment submission"
    ),
}


# --------------------------------------------------------------------------- #
#  Core function
# --------------------------------------------------------------------------- #

def create_student_summary(stu_id: str, summary_template: str) -> str:
    """
    Generate a student report by filling in placeholders in the template.

    Parameters
    ----------
    stu_id : str
        Unique identifier for a student.
    summary_template : str
        Template string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The filled-in report.

    Raises
    ------
    ValueError
        If the student ID is unknown or if a placeholder references a restricted
        attribute.
    """
    # Validate the student ID
    student = STUDENTS.get(stu_id)
    if student is None:
        raise ValueError(f"Invalid student ID: {stu_id}")

    # Define which attributes are allowed in the template
    ALLOWED_ATTRS = {
        "name",
        "course",
        "age",
        "gpa",
        "home_address",
    }

    # Find all placeholders in the form {student.attr}
    placeholder_pattern = re.compile(r"\{student\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    placeholders = placeholder_pattern.findall(summary_template)

    # Validate each placeholder
    for attr in set(placeholders):
        if attr not in ALLOWED_ATTRS:
            raise ValueError(f"Access to restricted or unknown attribute '{attr}' is not allowed.")

    # Build a mapping of placeholder names to values
    context = {attr: getattr(student, attr) for attr in placeholders}

    # Safely substitute the placeholders
    try:
        report = summary_template.format(**context)
    except KeyError as exc:
        # This should not happen because we validated attributes, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return report


# --------------------------------------------------------------------------- #
#  Example usage
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Student Report:\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa:.2f}\n"
        "Address: {student.home_address}"
    )
    print(create_student_summary("S001", template))