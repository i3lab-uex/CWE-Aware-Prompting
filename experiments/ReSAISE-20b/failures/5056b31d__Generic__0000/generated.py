import re
from dataclasses import dataclass, asdict
from typing import Dict

# ---------- Student data structures ----------
@dataclass
class Student:
    student_id: str
    name: str
    course: str
    age: int
    GPA: float
    home_address: str  # sensitive
    discipline_record: str  # sensitive

# Example in‑memory database (replace with real DB access as needed)
_STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        student_id="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        student_id="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission"
    ),
}

# ---------- Helper utilities ----------
_ALLOWED_FIELDS = {"name", "course", "age", "GPA"}
_PLACEHOLDER_RE = re.compile(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

def _extract_placeholders(template: str):
    """Return a set of placeholder field names found in the template."""
    return {match.group(1) for match in _PLACEHOLDER_RE.finditer(template)}

def _get_student_by_id(student_id: str) -> Student:
    """Retrieve a student object from the database or raise an error."""
    try:
        return _STUDENT_DB[student_id]
    except KeyError as exc:
        raise ValueError(f"Student with id '{student_id}' not found.") from exc

# ---------- Main function ----------
def generate_student_report(student_id: str, template: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    student_id : str
        Unique identifier for the student.
    template : str
        Template string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student is not found, if the template contains disallowed fields,
        or if an error occurs during formatting.
    """
    # Validate and fetch student
    student = _get_student_by_id(student_id)

    # Extract placeholders and validate them
    placeholders = _extract_placeholders(template)
    for field in placeholders:
        if field not in _ALLOWED_FIELDS:
            raise ValueError(
                f"Access to sensitive or undefined field '{field}' is not permitted."
            )

    # Prepare a safe mapping
    student_dict = {k: getattr(student, k) for k in _ALLOWED_FIELDS}

    try:
        report = template.format(**student_dict)
    except KeyError as exc:
        raise ValueError(f"Missing field in student data: {exc}") from exc
    except Exception as exc:
        raise ValueError(f"Error generating report: {exc}") from exc

    return report

# ---------- Example usage ----------
if __name__ == "__main__":
    tmpl = (
        "Student Report\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.GPA}"
    )
    print(generate_student_report("S001", tmpl))