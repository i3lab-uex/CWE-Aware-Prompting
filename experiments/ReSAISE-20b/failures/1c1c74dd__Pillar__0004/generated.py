import dataclasses
from typing import Dict

# --------------------------------------------------------------------
# Data model
# --------------------------------------------------------------------

@dataclasses.dataclass(frozen=True)
class Student:
    """Represents a student record."""
    name: str
    course: str
    age: int
    GPA: float
    home_address: str
    discipline_record: str


# --------------------------------------------------------------------
# In‑memory student repository (for demonstration purposes)
# --------------------------------------------------------------------

STUDENTS: Dict[str, Student] = {
    "S001": Student(
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None",
    ),
    "S002": Student(
        name="Bob Smith",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Rivertown",
        discipline_record="Late submission in 2024-01",
    ),
}


# --------------------------------------------------------------------
# Helper mapping that blocks sensitive attributes
# --------------------------------------------------------------------

class SafeStudentMapping(dict):
    """A mapping wrapper that disallows access to sensitive attributes."""

    _sensitive_attrs = {"GPA", "home_address"}

    def __init__(self, student: Student):
        super().__init__()
        self._student = student

    def __getitem__(self, key):
        # The format string may request nested attributes like student.name
        if isinstance(key, str) and key.startswith("student."):
            attr = key.split(".", 1)[1]
        else:
            # Unsupported key format; raise KeyError to mimic normal dict behaviour
            raise KeyError(key)

        if attr in self._sensitive_attrs:
            raise ValueError(f"Access to sensitive attribute '{attr}' is prohibited.")
        # Delegate to the actual Student dataclass
        return getattr(self._student, attr)


# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------

def produce_student_report(stu_id: str, custom_template: str) -> str:
    """
    Generate a formatted student report.

    Parameters
    ----------
    stu_id : str
        Unique identifier of the student.
    custom_template : str
        A format string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student ID does not exist or if the template attempts to access a sensitive attribute.
    """
    # Validate student existence
    try:
        student = STUDENTS[stu_id]
    except KeyError as exc:
        raise ValueError(f"Student ID '{stu_id}' not found.") from exc

    # Prepare a safe mapping for formatting
    mapping = SafeStudentMapping(student)

    try:
        report = custom_template.format_map(mapping)
    except KeyError as exc:
        # Occurs if the template references an undefined attribute
        raise ValueError(f"Template contains unknown placeholder: {exc}") from exc
    except ValueError as exc:
        # Propagate our custom sensitive‑attribute error
        raise

    return report


# --------------------------------------------------------------------
# Example usage (uncomment to test)
# --------------------------------------------------------------------

if __name__ == "__main__":
    template = (
        "Student Report\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
    )
    print(produce_student_report("S001", template))