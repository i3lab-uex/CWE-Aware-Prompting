import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
# Mock data structures – in a real system these would come from the database
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    student_number: str
    name: str
    course: str
    age: int
    GPA: float
    # Sensitive fields that must never be exposed in reports
    home_address: str = field(repr=False, compare=False)
    discipline_record: str = field(repr=False, compare=False)


# Example registry of students
_STUDENT_REGISTRY: Dict[str, Student] = {
    "S001": Student(
        student_number="S001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None",
    ),
    "S002": Student(
        student_number="S002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Springfield",
        discipline_record="Late assignment submission",
    ),
}


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _get_student(student_number: str) -> Student:
    """Retrieve a student from the registry, raising an error if not found."""
    try:
        return _STUDENT_REGISTRY[student_number]
    except KeyError as exc:
        raise ValueError(f"Student with number '{student_number}' not found.") from exc


def _extract_placeholders(template: str) -> set:
    """
    Find all placeholders of the form {student.<attribute>} in the template.
    Returns a set of attribute names.
    """
    pattern = r"{student\.([a-zA-Z_][a-zA-Z0-9_]*)}"
    return set(re.findall(pattern, template))


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def draft_student_report(student_number: str, report_template: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    student_number : str
        Unique identifier of the student.
    report_template : str
        A format string containing placeholders like `{student.name}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student does not exist or if the template references a
        disallowed (sensitive) attribute.
    """
    # 1. Retrieve the student data
    student = _get_student(student_number)

    # 2. Identify placeholders in the template
    placeholders = _extract_placeholders(report_template)

    # 3. Define allowed attributes – only non-sensitive fields
    ALLOWED_ATTRIBUTES = {"name", "course", "age", "GPA"}

    # 4. Validate placeholders
    for attr in placeholders:
        if attr not in ALLOWED_ATTRIBUTES:
            raise ValueError(
                f"Unauthorized access to sensitive data: '{attr}'. "
                "Only name, course, age, and GPA are allowed in reports."
            )

    # 5. Build a mapping for formatting
    context = {attr: getattr(student, attr) for attr in placeholders}

    # 6. Produce the final report
    try:
        return report_template.format(student=context)
    except KeyError as exc:
        # This should not happen because we validated placeholders,
        # but catch it just in case.
        raise ValueError(f"Missing placeholder data: {exc}") from exc


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Student Report\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.GPA:.2f}"
    )
    print(draft_student_report("S001", template))