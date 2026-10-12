import datetime
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
# 1. Student data model (simulated database)
# --------------------------------------------------------------------------- #

@dataclass
class Student:
    id: str
    name: str
    course: str
    age: int
    GPA: float
    home_address: str
    discipline_record: Dict[str, datetime.date] = field(default_factory=dict)


# Simulated in‑memory "database" of students
_STUDENT_DB: Dict[str, Student] = {
    "s001": Student(
        id="s001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
    ),
    "s002": Student(
        id="s002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
    ),
}


# --------------------------------------------------------------------------- #
# 2. Safe proxy that blocks access to sensitive attributes
# --------------------------------------------------------------------------- #

class _SafeStudentProxy:
    """
    A lightweight wrapper around a Student instance that only exposes
    non‑sensitive attributes. Attempting to access any forbidden attribute
    raises a ValueError.
    """
    _ALLOWED_ATTRS = {"name", "course", "age"}

    def __init__(self, student: Student) -> None:
        self._student = student

    def __getattr__(self, name: str):
        if name in self._ALLOWED_ATTRS:
            return getattr(self._student, name)
        raise ValueError(
            f"Access to sensitive attribute '{name}' is forbidden in student reports."
        )

    def __repr__(self) -> str:
        attrs = ", ".join(f"{a}={getattr(self, a)!r}" for a in self._ALLOWED_ATTRS)
        return f"<SafeStudentProxy {attrs}>"


# --------------------------------------------------------------------------- #
# 3. Main function
# --------------------------------------------------------------------------- #

def create_student_summary(id: str, format_string: str) -> str:
    """
    Generate a student report from the provided format string.

    Parameters
    ----------
    id : str
        Unique identifier of the student.
    format_string : str
        A format string that may contain placeholders such as
        '{student.name}', '{student.course}', or '{student.age}'.

    Returns
    -------
    str
        The formatted student report.

    Raises
    ------
    ValueError
        If the id does not exist or if the format string attempts to
        access a forbidden attribute (e.g., GPA, home_address).
    """
    # Validate ID
    student = _STUDENT_DB.get(id)
    if not student:
        raise ValueError(f"Student with id '{id}' does not exist.")

    # Wrap the student in a safe proxy
    safe_student = _SafeStudentProxy(student)

    try:
        report = format_string.format(student=safe_student)
    except AttributeError as exc:
        # Occurs when the format string references an attribute that
        # doesn't exist on the proxy. We re‑raise as ValueError for consistency.
        raise ValueError(
            f"Invalid placeholder in format string: {exc}"
        ) from exc

    return report


# --------------------------------------------------------------------------- #
# 4. Example usage (for manual testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = "Student: {student.name}\nCourse: {student.course}\nAge: {student.age}"
    print(create_student_summary("s001", template))

    # Uncommenting the following line will raise ValueError due to sensitive data access
    # print(create_student_summary("s001", "GPA: {student.GPA}"))