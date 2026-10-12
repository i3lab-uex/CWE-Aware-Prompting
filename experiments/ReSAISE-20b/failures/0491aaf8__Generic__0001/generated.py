import re
from dataclasses import dataclass

# --------------------------------------------------------------------
# Example Student class (the real system would provide this)
# --------------------------------------------------------------------
@dataclass
class Student:
    id: str
    name: str
    course: str
    age: int
    GPA: float  # Sensitive
    home_address: str  # Sensitive
    discipline_record: list


# --------------------------------------------------------------------
# In‑memory "database" of students (replace with real persistence)
# --------------------------------------------------------------------
_STUDENT_DB = {
    "S001": Student(
        id="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record=[],
    ),
    "S002": Student(
        id="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record=["Late submission"],
    ),
}


# --------------------------------------------------------------------
# Helper: Detect placeholders in the format string
# --------------------------------------------------------------------
_PLACEHOLDER_RE = re.compile(r"\{([^{}]+)\}")

def _extract_placeholders(fmt: str) -> set[str]:
    """Return a set of unique placeholder names used in the format string."""
    return {m.group(1).strip() for m in _PLACEHOLDER_RE.finditer(fmt)}


# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------
def create_student_summary(id: str, format_string: str) -> str:
    """
    Generate a student report using the supplied template.

    Args:
        id: Unique identifier of the student.
        format_string: A Python format string containing placeholders such
                       as '{student.name}' or '{student.course}'.

    Returns:
        A formatted string representing the student's report.

    Raises:
        ValueError: If the student ID does not exist, or if a sensitive
                    attribute (GPA or home_address) is requested in the template.
    """
    # 1. Validate student existence
    student = _STUDENT_DB.get(id)
    if not student:
        raise ValueError(f"Student with id '{id}' does not exist.")

    # 2. Inspect placeholders for forbidden fields
    placeholders = _extract_placeholders(format_string)
    for placeholder in placeholders:
        # Only consider placeholders that refer to the student object
        if not placeholder.startswith("student."):
            continue

        # Extract attribute name (supports nested attributes, e.g., student.discipline_record[0])
        attr_path = placeholder.split(".", 1)[1]
        # Handle simple attribute names; ignore complex expressions for safety
        attr_name = attr_path.split("[")[0].split("(")[0]
        if attr_name in {"GPA", "home_address"}:
            raise ValueError(
                f"Access to sensitive attribute '{attr_name}' is not allowed."
            )

    # 3. Format the string
    try:
        report = format_string.format(student=student)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to format report: {exc}") from exc

    return report


# --------------------------------------------------------------------
# Example usage (uncomment to test)
# --------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Report:\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}"
    )
    print(create_student_summary("S001", template))