import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------
# Mock Student class (normally provided by the system)
# ----------------------------------------------------
@dataclass
class Student:
    stu_id: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str
    # Sensitive data that must not appear in public reports
    disciplinary_record: str = field(repr=False, default="")

# ----------------------------------------------------
# In‑memory student repository
# ----------------------------------------------------
STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        stu_id="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        disciplinary_record="None"
    ),
    "S002": Student(
        stu_id="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        disciplinary_record="Late submission of assignment #3"
    ),
}

# ----------------------------------------------------
# Utility: Extract placeholder names from a format string
# ----------------------------------------------------
def _extract_placeholders(template: str):
    """
    Return a set of placeholder names used in the template.
    Only supports simple attribute access like {student.name}.
    """
    # Regex matches {object.attribute} or {attribute}
    pattern = r"{\s*(?P<full>[^{}]+)\s*}"
    placeholders = set()
    for match in re.finditer(pattern, template):
        full = match.group("full")
        # split on dot to get the first part
        parts = full.split(".", 1)
        if len(parts) == 2:
            obj, attr = parts
            placeholders.add(attr)
        else:
            placeholders.add(full)
    return placeholders

# ----------------------------------------------------
# Main function
# ----------------------------------------------------
def create_student_summary(stu_id: str, summary_template: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    stu_id : str
        Unique identifier of the student.
    summary_template : str
        A format string containing placeholders such as '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student ID is not found, or if a placeholder refers to
        restricted/sensitive data.
    """
    # Validate student ID
    student = STUDENT_DB.get(stu_id)
    if not student:
        raise ValueError(f"Invalid student ID: {stu_id}")

    # Define allowed attributes
    allowed_attrs = {
        "name",
        "course",
        "age",
        "gpa",
        "home_address",
    }

    # Inspect placeholders
    placeholders = _extract_placeholders(summary_template)
    for attr in placeholders:
        if attr not in allowed_attrs:
            raise ValueError(
                f"Attempt to access restricted or unknown attribute '{attr}'. "
                "Only the following attributes are allowed: "
                f"{', '.join(sorted(allowed_attrs))}."
            )

    # Perform formatting safely
    try:
        report = summary_template.format(student=student)
    except Exception as e:  # pragma: no cover
        raise ValueError(f"Failed to format template: {e}") from e

    return report


# ----------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Student Report\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa:.2f}\n"
        "Address: {student.home_address}"
    )
    print(create_student_summary("S001", tmpl))