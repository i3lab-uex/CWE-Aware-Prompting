import re
from dataclasses import dataclass, field

# --------------------------------------------------------------------
# Student data model (simplified for this example)
# --------------------------------------------------------------------
@dataclass
class Student:
    id: str
    name: str
    course: str
    age: int
    GPA: float = field(repr=False)           # Sensitive
    home_address: str = field(repr=False)   # Sensitive
    discipline_record: str

# --------------------------------------------------------------------
# In‑memory "database" of students (for demonstration)
# --------------------------------------------------------------------
_STUDENT_DB = {
    "s123": Student(
        id="s123",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Main St, Anytown",
        discipline_record="None"
    ),
    "s456": Student(
        id="s456",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Othertown",
        discipline_record="Late submission of Assignment 2"
    ),
}

# --------------------------------------------------------------------
# Helper utilities
# --------------------------------------------------------------------
_SENSITIVE_FIELDS = {"GPA", "home_address"}
_ALLOWED_PLACEHOLDERS = {"student.name", "student.course", "student.age", "student.discipline_record"}

_PLACEHOLDER_REGEX = re.compile(r"{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

def _extract_placeholders(fmt: str):
    """Return a set of placeholders found in the format string."""
    return {f"student.{m.group(1)}" for m in _PLACEHOLDER_REGEX.finditer(fmt)}

def _validate_placeholders(placeholders: set):
    """Ensure no sensitive data is requested."""
    for ph in placeholders:
        if ph not in _ALLOWED_PLACEHOLDERS:
            raise ValueError(f"Access to sensitive attribute '{ph.split('.')[1]}' is not allowed.")

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------
def create_student_summary(id: str, format_string: str) -> str:
    """
    Generate a student report using the supplied template.

    Parameters
    ----------
    id : str
        Unique identifier for a student.
    format_string : str
        A Python format string containing placeholders such as '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student ID does not exist or if a placeholder references
        sensitive data.
    """
    # Lookup the student; raise error if not found
    student = _STUDENT_DB.get(id)
    if not student:
        raise ValueError(f"Student with ID '{id}' does not exist.")

    # Validate placeholders for security
    placeholders = _extract_placeholders(format_string)
    _validate_placeholders(placeholders)

    # Build a mapping for formatting
    context = {
        "student.name": student.name,
        "student.course": student.course,
        "student.age": str(student.age),
        "student.discipline_record": student.discipline_record,
    }

    # Perform formatting; any missing keys will raise KeyError which we convert to ValueError
    try:
        return format_string.format(**context)
    except KeyError as exc:
        raise ValueError(f"Missing placeholder in format string: {exc}") from None

# --------------------------------------------------------------------
# Example usage (uncomment to test)
# --------------------------------------------------------------------
# if __name__ == "__main__":
#     fmt = "Student Report:\nName: {student.name}\nCourse: {student.course}\nAge: {student.age}\nDiscipline Record: {student.discipline_record}"
#     print(create_student_summary("s123", fmt))