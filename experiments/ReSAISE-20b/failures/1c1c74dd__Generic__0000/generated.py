import dataclasses
from typing import Dict

# --- Student data model ----------------------------------------------------
@dataclasses.dataclass(frozen=True)
class Student:
    """Represents a student with non‑sensitive and sensitive attributes."""
    name: str
    course: str
    age: int
    GPA: float          # Sensitive
    home_address: str   # Sensitive
    discipline_record: str


# --- In‑memory "database" of students ------------------------------------
_STUDENTS_DB: Dict[str, Student] = {
    # Example entries – in a real system this would come from a database
    "S001": Student(
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        GPA=3.9,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        name="Bob Smith",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission in MATH101"
    ),
}


# --- Helper utilities ------------------------------------------------------
def _extract_placeholders(template: str) -> set:
    """
    Parse a format string and return the set of field names used.
    Only fields that start with 'student.' are considered relevant.
    """
    import string
    formatter = string.Formatter()
    placeholders = set()

    for literal_text, field_name, format_spec, conversion in formatter.parse(template):
        if field_name and field_name.startswith("student."):
            # Remove any nested attributes after the first dot (e.g., student.name.first)
            attr = field_name.split(".", 1)[1]
            placeholders.add(attr)

    return placeholders


# --- Main function ---------------------------------------------------------
def produce_student_report(stu_id: str, custom_template: str) -> str:
    """
    Generate a student report using the supplied template.

    Parameters
    ----------
    stu_id : str
        Unique identifier for a student.
    custom_template : str
        Format string containing placeholders such as '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student ID does not exist, if a sensitive attribute is requested,
        or if placeholder names are invalid.
    """
    # 1. Retrieve student record
    try:
        student = _STUDENTS_DB[stu_id]
    except KeyError as exc:
        raise ValueError(f"Student ID '{stu_id}' does not exist.") from exc

    # 2. Inspect template for sensitive placeholders
    placeholders = _extract_placeholders(custom_template)
    SENSITIVE_ATTRS = {"GPA", "home_address"}
    if placeholders & SENSITIVE_ATTRS:
        raise ValueError(
            f"Access to sensitive attributes {placeholders & SENSITIVE_ATTRS} is not allowed."
        )

    # 3. Prepare a mapping for formatting
    student_dict = dataclasses.asdict(student)

    # 4. Perform the actual formatting, catching any missing keys
    try:
        report = custom_template.format(student=student_dict)
    except KeyError as exc:
        # Convert formatting errors into a clear ValueError
        missing_field = exc.args[0]
        raise ValueError(f"Invalid placeholder '{missing_field}' in template.") from exc

    return report


# --- Example usage ---------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "---------------\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}"
    )
    print(produce_student_report("S001", template))