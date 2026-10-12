import re
from dataclasses import dataclass, fields
from typing import Dict

# --------------------------------------------------------------------------- #
# Dummy student database (replace with your actual data source)
# --------------------------------------------------------------------------- #
@dataclass
class Student:
    id: str
    name: str
    course: str
    age: int
    GPA: float
    home_address: str
    discipline_record: str

# Example data – in a real system this would come from a database
STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        id="S001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        id="S002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission on 2023-09-15"
    ),
}


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def _extract_placeholder_attributes(format_str: str) -> set[str]:
    """
    Extract attribute names used in the format string.
    Supports simple `{student.attribute}` placeholders only.
    """
    pattern = r"\{student\.([a-zA-Z_][a-zA-Z0-9_]*)\}"
    return set(re.findall(pattern, format_str))


def _validate_no_sensitive_access(attrs: set[str]) -> None:
    """
    Raise ValueError if any sensitive attribute is requested.
    Sensitive attributes: GPA, home_address
    """
    sensitive = {"GPA", "home_address"}
    if attrs & sensitive:
        raise ValueError(
            f"Access to sensitive attributes {attrs & sensitive} is prohibited."
        )


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def create_student_summary(id: str, format_string: str) -> str:
    """
    Generate a student report using the provided format string.

    Parameters
    ----------
    id : str
        Unique identifier for the student.
    format_string : str
        Format string containing placeholders such as `{student.name}`.

    Returns
    -------
    str
        The formatted student report.

    Raises
    ------
    ValueError
        If the student ID does not exist or if the format string attempts to
        access sensitive attributes (GPA, home_address).
    """
    # 1. Retrieve student
    student = STUDENT_DB.get(id)
    if not student:
        raise ValueError(f"Student ID '{id}' does not exist.")

    # 2. Validate placeholders
    attrs = _extract_placeholder_attributes(format_string)
    if not attrs:
        raise ValueError("Format string must contain at least one `{student.attribute}` placeholder.")
    _validate_no_sensitive_access(attrs)

    # 3. Ensure requested attributes exist on Student
    student_fields = {f.name for f in fields(student)}
    missing = attrs - student_fields
    if missing:
        raise ValueError(f"Unknown attribute(s) requested: {missing}")

    # 4. Format the string
    try:
        report = format_string.format(student=student)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Formatting error: {exc}") from exc

    return report


# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    tmpl = (
        "Student Report\n"
        "--------------\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "Discipline Record: {student.discipline_record}"
    )
    print(create_student_summary("S001", tmpl))