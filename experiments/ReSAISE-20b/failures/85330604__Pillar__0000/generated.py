import re
from dataclasses import dataclass, asdict
from typing import Dict

# --------------------------------------------------------------------------- #
#   Data model & in‑memory storage (mock of the system database)
# --------------------------------------------------------------------------- #

@dataclass
class Student:
    """Represents a student record in the system."""
    stu_id: str
    name: str
    course: str
    age: int
    GPA: float
    home_address: str          # Sensitive – must not be exposed
    discipline_record: str     # Sensitive – must not be exposed


# Mock database: mapping from stu_id to Student instance
_STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        stu_id="S001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple Street, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        stu_id="S002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Avenue, Shelbyville",
        discipline_record="Late submission of Assignment 3"
    ),
}


# --------------------------------------------------------------------------- #
#   Utility functions
# --------------------------------------------------------------------------- #

def _get_student(stu_id: str) -> Student:
    """
    Retrieve a student from the mock database.
    Raises ValueError if the student does not exist.
    """
    student = _STUDENT_DB.get(stu_id)
    if student is None:
        raise ValueError(f"Student with ID '{stu_id}' does not exist.")
    return student


def _extract_placeholders(template: str) -> set:
    """
    Extract placeholder names from the template.
    Supports simple `{field}` syntax; ignores nested expressions.
    """
    pattern = r"\{([^{}]+)\}"
    return set(re.findall(pattern, template))


def _sanitize_context(context: dict) -> dict:
    """
    Return a copy of the context dictionary with only non‑sensitive keys.
    Raises ValueError if a sensitive key is present.
    """
    allowed_keys = {"name", "course", "age", "GPA"}
    for key in context:
        if key not in allowed_keys:
            raise ValueError(f"Attempt to expose sensitive data via placeholder '{{{key}}}'.")
    return {k: context[k] for k in allowed_keys if k in context}


# --------------------------------------------------------------------------- #
#   Main function
# --------------------------------------------------------------------------- #

def create_student_report(stu_id: str, report_template: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    stu_id : str
        Unique identifier for the student.
    report_template : str
        Template string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student does not exist, or if the template attempts to access
        sensitive data such as home_address or discipline_record.
    """
    # 1. Retrieve the student record
    student = _get_student(stu_id)

    # 2. Build a context dictionary with only allowed attributes
    student_dict = asdict(student)
    # Remove the stu_id key – it should not appear in the template
    student_dict.pop("stu_id", None)
    context = _sanitize_context(student_dict)

    # 3. Validate the template for disallowed placeholders
    placeholders = _extract_placeholders(report_template)
    # Normalize placeholders by stripping potential prefixes like 'student.'
    normalized = {p.split(".")[-1] for p in placeholders}
    disallowed = normalized - {"name", "course", "age", "GPA"}
    if disallowed:
        raise ValueError(
            f"Template contains unauthorized placeholders: {', '.join(sorted(disallowed))}"
        )

    # 4. Perform safe formatting
    try:
        report = report_template.format(**context)
    except KeyError as exc:
        raise ValueError(f"Missing placeholder value for '{exc.args[0]}'") from exc

    return report


# --------------------------------------------------------------------------- #
#   Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Student Report\n"
        "Name: {name}\n"
        "Course: {course}\n"
        "Age: {age}\n"
        "GPA: {GPA:.2f}"
    )
    print(create_student_report("S001", template))