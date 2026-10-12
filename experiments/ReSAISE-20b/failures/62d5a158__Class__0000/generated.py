import re
from dataclasses import dataclass, field
from typing import Dict

# --- Domain model -------------------------------------------------------------

@dataclass
class Student:
    """Represents a student in the system."""
    stu_id: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str
    # Sensitive / restricted data
    disciplinary_record: Dict[str, str] = field(default_factory=dict)

# In‑memory store of students (for demonstration purposes)
STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        stu_id="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        disciplinary_record={"2021": "Late submission"},
    ),
    "S002": Student(
        stu_id="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        disciplinary_record={},
    ),
}

# --- Helper utilities --------------------------------------------------------

_ALLOWED_PLACEHOLDERS = {
    "student.name",
    "student.course",
    "student.age",
    "student.gpa",
    "student.home_address",
}

_RESTRICTED_PLACEHOLDERS = {
    "student.disciplinary_record",
}

# Regular expression to find all {placeholder} occurrences
_PLACEHOLDER_RE = re.compile(r"\{([^{}]+)\}")

def _extract_placeholders(template: str) -> set[str]:
    """Return a set of placeholder names found in the template."""
    return {match.group(1).strip() for match in _PLACEHOLDER_RE.finditer(template)}

def _replace_placeholders(template: str, values: Dict[str, str]) -> str:
    """Replace placeholders in the template with actual values."""
    def repl(match):
        key = match.group(1).strip()
        return str(values.get(key, f"{{{key}}}"))
    return _PLACEHOLDER_RE.sub(repl, template)

# --- Core function -----------------------------------------------------------

def create_student_summary(stu_id: str, summary_template: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    stu_id : str
        Unique identifier of the student.
    summary_template : str
        Template string containing placeholders such as '{student.name}'.

    Returns
    -------
    str
        The formatted student report.

    Raises
    ------
    ValueError
        If the student ID is invalid or if the template attempts to access
        restricted/sensitive information.
    """
    # Validate student ID
    student = STUDENT_DB.get(stu_id)
    if not student:
        raise ValueError(f"Invalid student ID: {stu_id}")

    # Extract placeholders from the template
    placeholders = _extract_placeholders(summary_template)

    # Check for restricted placeholder usage
    if placeholders & _RESTRICTED_PLACEHOLDERS:
        raise ValueError("Template attempts to access restricted student data")

    # Ensure all placeholders are allowed
    invalid_placeholders = placeholders - _ALLOWED_PLACEHOLDERS
    if invalid_placeholders:
        raise ValueError(f"Template contains unknown placeholders: {', '.join(invalid_placeholders)}")

    # Prepare mapping for placeholder substitution
    value_map = {
        "student.name": student.name,
        "student.course": student.course,
        "student.age": student.age,
        "student.gpa": student.gpa,
        "student.home_address": student.home_address,
    }

    # Perform substitution
    report = _replace_placeholders(summary_template, value_map)
    return report

# --- Example usage -----------------------------------------------------------

if __name__ == "__main__":
    tmpl = (
        "Student Report\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa}\n"
        "Address: {student.home_address}"
    )
    try:
        print(create_student_summary("S001", tmpl))
    except ValueError as e:
        print(f"Error: {e}")