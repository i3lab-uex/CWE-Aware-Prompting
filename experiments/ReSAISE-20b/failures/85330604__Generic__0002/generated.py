import re
from dataclasses import dataclass, field
from typing import Dict

# --- Mock Student data storage -------------------------------------------------
@dataclass
class Student:
    name: str
    course: str
    age: int
    GPA: float
    home_address: str = field(repr=False)
    discipline_record: str = field(repr=False)

# Example in‑memory database (in a real system this would be replaced by DB access)
_STUDENTS_DB: Dict[str, Student] = {
    "S001": Student(
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Main St, Townsville",
        discipline_record="None"
    ),
    "S002": Student(
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Cityville",
        discipline_record="Late assignment"
    ),
}

# --- Allowed attributes -------------------------------------------------------
_ALLOWED_ATTRS = {"name", "course", "age", "GPA"}

# --- Main function -------------------------------------------------------------
def create_student_report(stu_id: str, report_template: str) -> str:
    """
    Generate a student report from the given template.

    Parameters
    ----------
    stu_id : str
        Unique identifier of the student.
    report_template : str
        Template string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        Formatted report string.

    Raises
    ------
    ValueError
        If the student ID is unknown or if the template references
        disallowed (sensitive) attributes.
    """
    # 1. Retrieve student record
    student = _STUDENTS_DB.get(stu_id)
    if not student:
        raise ValueError(f"Student ID '{stu_id}' does not exist.")

    # 2. Find all placeholders of the form {student.attribute}
    placeholder_pattern = re.compile(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")
    placeholders = placeholder_pattern.findall(report_template)

    # 3. Validate each attribute
    for attr in placeholders:
        if attr not in _ALLOWED_ATTRS:
            raise ValueError(
                f"Access to sensitive attribute '{attr}' is not permitted."
            )

    # 4. Prepare a mapping for formatting
    context = {attr: getattr(student, attr) for attr in placeholders}

    # 5. Perform safe formatting
    try:
        report = report_template.format(student=context)
    except KeyError as exc:
        # Should not happen because we validated attributes
        raise ValueError(f"Missing attribute in template: {exc}") from exc

    return report


# --- Example usage -------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.GPA:.2f}"
    )
    print(create_student_report("S001", template))