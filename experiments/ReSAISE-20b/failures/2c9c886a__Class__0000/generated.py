import re
from dataclasses import dataclass, fields
from typing import Dict

# --- Student data model ---------------------------------------------------------

@dataclass(frozen=True)
class Student:
    """Represents a student with various attributes."""
    name: str
    course: str
    age: int
    GPA: float
    home_address: str  # Sensitive
    discipline_record: str  # Sensitive

# --- In‑memory student registry -----------------------------------------------

# For demonstration purposes, a simple in-memory dictionary is used.
# In a real system this would interface with a database or secure storage.
STUDENT_REGISTRY: Dict[str, Student] = {
    "S001": Student(
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="No violations"
    ),
    "S002": Student(
        name="Bob Smith",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission of assignment"
    ),
}

# --- Allowed attributes --------------------------------------------------------

ALLOWED_FIELDS = {f.name for f in fields(Student) if f.name not in {"home_address", "discipline_record"}}

# --- Main function -------------------------------------------------------------

def draft_student_report(student_number: str, report_template: str) -> str:
    """
    Generates a student report based on the provided template.

    Parameters
    ----------
    student_number : str
        The unique identifier of the student.
    report_template : str
        A format string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student does not exist or if the template attempts to access
        disallowed (sensitive) attributes.
    """
    # Retrieve student; raise if not found
    try:
        student = STUDENT_REGISTRY[student_number]
    except KeyError as exc:
        raise ValueError(f"Student with number '{student_number}' does not exist.") from exc

    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"\{([a-zA-Z_][\w\.]*)\}")
    placeholders = placeholder_pattern.findall(report_template)

    # Validate each placeholder
    for ph in placeholders:
        if not ph.startswith("student."):
            raise ValueError(f"Unauthorized placeholder '{ph}'. Only 'student' attributes are allowed.")
        attr = ph.split(".", 1)[1]
        if attr not in ALLOWED_FIELDS:
            raise ValueError(f"Access to sensitive attribute '{attr}' is forbidden.")

    # Prepare a mapping for formatting
    context = {"student": student}

    try:
        report = report_template.format(**context)
    except Exception as exc:  # pragma: no cover
        raise ValueError("Failed to format the report.") from exc

    return report


# --- Example usage -------------------------------------------------------------

if __name__ == "__main__":
    template = (
        "Student Report\n"
        "---------------\n"
        "Name   : {student.name}\n"
        "Course : {student.course}\n"
        "Age    : {student.age}\n"
        "GPA    : {student.GPA:.2f}\n"
    )
    print(draft_student_report("S001", template))