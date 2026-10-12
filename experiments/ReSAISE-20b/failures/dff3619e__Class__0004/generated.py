import re
from dataclasses import dataclass
from typing import Dict, Any

# ------------------------------------------------------------------
# Mocked student database and retrieval logic (replace with real DB)
# ------------------------------------------------------------------
@dataclass
class Student:
    """Represents a student record."""
    learner_id: str
    name: str
    course: str
    age: int
    gpa: float
    # Sensitive fields that must never be exposed via the report:
    _home_address: str = None
    _disciplinary_record: str = None


# In‑memory "database" of students for demonstration purposes
_STUDENT_DB: Dict[str, Student] = {
    "12345": Student(
        learner_id="12345",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        _home_address="123 Maple St, Springfield",
        _disciplinary_record="None",
    ),
    "67890": Student(
        learner_id="67890",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.4,
        _home_address="456 Oak Ave, Shelbyville",
        _disciplinary_record="Late submission of assignment 3",
    ),
}


def get_student_by_id(learner_id: str) -> Student:
    """Retrieve a student from the database or raise ValueError if not found."""
    student = _STUDENT_DB.get(learner_id)
    if not student:
        raise ValueError(f"Invalid learner ID: {learner_id!r}")
    return student


# ------------------------------------------------------------------
# Core report generation logic
# ------------------------------------------------------------------
_ALLOWED_PLACEHOLDERS = {"student.name", "student.course", "student.age", "student.gpa"}


def _extract_placeholders(template: str) -> set[str]:
    """Return a set of placeholders found in the template."""
    # Matches {something} or {{escaped}}
    pattern = re.compile(r"{([^{}]+)}")
    return set(match.group(1).strip() for match in pattern.finditer(template))


def build_student_report(learner_id: str, layout: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    learner_id : str
        Unique identifier of the student.
    layout : str
        Template string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The formatted report with placeholders replaced by actual values.

    Raises
    ------
    ValueError
        If the learner_id is invalid, or if the template contains disallowed placeholders.
    """
    # Basic validation of learner_id (e.g., only digits)
    if not re.fullmatch(r"\d{5}", learner_id):
        raise ValueError(f"Invalid learner ID format: {learner_id!r}")

    student = get_student_by_id(learner_id)

    # Find placeholders in the template
    placeholders = _extract_placeholders(layout)
    if not placeholders.issubset(_ALLOWED_PLACEHOLDERS):
        disallowed = placeholders - _ALLOWED_PLACEHOLDERS
        raise ValueError(
            f"Template contains disallowed placeholders: {', '.join(sorted(disallowed))}"
        )

    # Map placeholder names to actual values
    context: Dict[str, Any] = {
        "student.name": student.name,
        "student.course": student.course,
        "student.age": str(student.age),
        "student.gpa": f"{student.gpa:.2f}",
    }

    # Perform safe substitution
    def replace(match: re.Match) -> str:
        key = match.group(1).strip()
        return context.get(key, f"{{{key}}}")  # should never happen due to earlier check

    report = re.sub(r"{([^{}]+)}", replace, layout)
    return report