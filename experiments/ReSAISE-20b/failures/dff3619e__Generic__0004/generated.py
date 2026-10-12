import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
# 1. Student data model
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    """Represents a student with basic profile and academic info."""
    name: str
    course: str
    age: int
    gpa: float
    home_address: str
    disciplinary_record: str = field(repr=False)  # Sensitive


# --------------------------------------------------------------------------- #
# 2. In‑memory student store (for demonstration purposes)
# --------------------------------------------------------------------------- #

_STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        disciplinary_record="None"
    ),
    "S002": Student(
        name="Bob Smith",
        course="Mechanical Engineering",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Springfield",
        disciplinary_record="Late submission of Project X"
    ),
    # Add more students as needed...
}


# --------------------------------------------------------------------------- #
# 3. Helper proxy to expose only non‑sensitive attributes
# --------------------------------------------------------------------------- #

class _StudentProxy:
    """A read‑only proxy that exposes only permitted Student attributes."""
    __slots__ = ("_student",)

    _allowed_attrs = {"name", "course", "age", "gpa", "home_address"}

    def __init__(self, student: Student):
        self._student = student

    def __getattr__(self, item):
        if item not in self._allowed_attrs:
            raise AttributeError(f"Access to attribute '{item}' is forbidden.")
        return getattr(self._student, item)


# --------------------------------------------------------------------------- #
# 4. Main function
# --------------------------------------------------------------------------- #

def build_student_report(learner_id: str, layout: str) -> str:
    """
    Generates a student report based on the provided template.

    Parameters
    ----------
    learner_id : str
        Unique identifier of the student.
    layout : str
        A template string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student ID is invalid, or if the template attempts to access a
        restricted/sensitive attribute.
    """
    # Validate student ID and fetch record
    if learner_id not in _STUDENT_DB:
        raise ValueError(f"Invalid student ID: {learner_id}")

    student = _STUDENT_DB[learner_id]
    proxy = _StudentProxy(student)

    # Basic validation: ensure placeholders reference permitted attributes
    placeholder_pattern = re.compile(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")
    for match in placeholder_pattern.finditer(layout):
        attr = match.group(1)
        if attr not in _StudentProxy._allowed_attrs:
            raise ValueError(
                f"Template references restricted attribute '{attr}'. "
                "Access denied for security reasons."
            )

    # Perform formatting
    try:
        report = layout.format(student=proxy)
    except AttributeError as exc:
        # This should not happen due to prior checks, but guard anyway
        raise ValueError(f"Invalid placeholder in template: {exc}") from exc

    return report


# --------------------------------------------------------------------------- #
# 5. Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     template = (
#         "Student Report\n"
#         "---------------\n"
#         "Name: {student.name}\n"
#         "Course: {student.course}\n"
#         "Age: {student.age}\n"
#         "GPA: {student.gpa:.2f}\n"
#         "Address: {student.home_address}"
#     )
#
#     print(build_student_report("S001", template))