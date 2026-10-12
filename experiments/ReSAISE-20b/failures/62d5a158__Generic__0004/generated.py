import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Student model (for illustration purposes)
# ----------------------------------------------------------------------
@dataclass
class Student:
    """A simple student data model."""
    name: str
    course: str
    age: int
    gpa: float
    address: str
    # Sensitive attribute that should not be exposed via templates
    disciplinary_record: str = field(repr=False, default="")

# ----------------------------------------------------------------------
# In‑memory "database" of students
# ----------------------------------------------------------------------
STUDENTS: Dict[str, Student] = {
    "S001": Student(
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        address="123 Maple St, Springfield",
    ),
    "S002": Student(
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        gpa=3.5,
        address="456 Oak Ave, Shelbyville",
    ),
}

# ----------------------------------------------------------------------
# Allowed attributes that may appear in a template
# ----------------------------------------------------------------------
ALLOWED_ATTRS = {
    "name",
    "course",
    "age",
    "gpa",
    "address",
}

# ----------------------------------------------------------------------
# Template processing
# ----------------------------------------------------------------------
PLACEHOLDER_RE = re.compile(r"\{([^}]+)\}")

def _extract_placeholders(template: str) -> set[str]:
    """Return a set of placeholder names found in the template."""
    return {match.group(1) for match in PLACEHOLDER_RE.finditer(template)}

def _validate_placeholders(placeholders: set[str]) -> None:
    """Ensure that only allowed placeholders are used."""
    for ph in placeholders:
        # We expect the format 'student.<attr>'
        if not ph.startswith("student."):
            raise ValueError(f"Unsupported placeholder format: '{{{ph}}}'")
        attr = ph.split(".", 1)[1]
        if attr not in ALLOWED_ATTRS:
            raise ValueError(
                f"Access to restricted or unknown attribute '{attr}' is not allowed."
            )

def _replace_placeholders(template: str, student: Student) -> str:
    """Replace placeholders with the corresponding student attributes."""
    def repl(match):
        full = match.group(1)  # e.g. 'student.name'
        _, attr = full.split(".", 1)
        value = getattr(student, attr)
        return str(value)

    return PLACEHOLDER_RE.sub(repl, template)


# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def create_student_summary(stu_id: str, summary_template: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    stu_id : str
        Unique identifier for a student.
    summary_template : str
        A string containing placeholders such as '{student.name}'.

    Returns
    -------
    str
        The report with all placeholders replaced by student data.

    Raises
    ------
    ValueError
        If the student ID is invalid or if the template contains disallowed placeholders.
    """
    # 1. Validate student ID
    student = STUDENTS.get(stu_id)
    if not student:
        raise ValueError(f"Student ID '{stu_id}' does not exist.")

    # 2. Extract and validate placeholders
    placeholders = _extract_placeholders(summary_template)
    _validate_placeholders(placeholders)

    # 3. Replace placeholders
    report = _replace_placeholders(summary_template, student)
    return report


# ----------------------------------------------------------------------
# Example usage (commented out – remove comments to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Student Report\n"
        "---------------\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa:.2f}\n"
        "Address: {student.address}"
    )
    print(create_student_summary("S001", tmpl))