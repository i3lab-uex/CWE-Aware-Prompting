import re
from dataclasses import dataclass, field
from typing import Dict

# -------------------------------------------------------------
# Domain model – a minimal Student definition
# -------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    unique_id: str
    name: str
    course: str
    age: int
    gpa: float = field(repr=False)          # Sensitive
    home_address: str = field(repr=False)   # Sensitive
    discipline_record: str = ""


# -------------------------------------------------------------
# In‑memory "database" of students for demonstration purposes
# -------------------------------------------------------------
STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        unique_id="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
    ),
    "S002": Student(
        unique_id="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Springfield",
    ),
}


# -------------------------------------------------------------
# Helper class that prevents access to sensitive attributes
# -------------------------------------------------------------
class SafeStudentMap(dict):
    """
    A mapping that exposes only non‑sensitive student attributes.
    Attempting to access a sensitive attribute raises ValueError.
    """

    _sensitive = {"gpa", "home_address"}

    def __init__(self, student: Student):
        super().__init__()
        for field_name in vars(student).keys():
            if field_name not in self._sensitive:
                self[field_name] = getattr(student, field_name)

    def __missing__(self, key):
        if key in self._sensitive:
            raise ValueError(f"Access to sensitive attribute '{key}' is forbidden.")
        raise KeyError(key)


# -------------------------------------------------------------
# Main function
# -------------------------------------------------------------
def build_student_profile(unique_id: str, report_template: str) -> str:
    """
    Build a formatted student profile from a template.

    Args:
        unique_id: The student's unique identifier.
        report_template: A format string containing placeholders like
                         '{student.name}', '{student.course}'.

    Returns:
        A formatted string with the student's data inserted.

    Raises:
        ValueError: If a sensitive attribute is accessed or if
                    the unique_id does not exist.
    """
    # Validate existence of student
    student = STUDENT_DB.get(unique_id)
    if not student:
        raise ValueError(f"Student with ID '{unique_id}' does not exist.")

    # Detect placeholders that reference student attributes
    placeholder_pattern = re.compile(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")
    placeholders = placeholder_pattern.findall(report_template)

    # Prepare a safe mapping for formatting
    student_map = SafeStudentMap(student)

    # Ensure that no placeholder references a sensitive field
    for attr in placeholders:
        if attr in SafeStudentMap._sensitive:
            raise ValueError(f"Template contains forbidden sensitive attribute '{attr}'.")

    # Replace placeholders with actual values
    formatted = report_template.format(student=student_map)
    return formatted


# -------------------------------------------------------------
# Example usage (uncomment to test)
# -------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "--------------\n"
        "Name   : {student.name}\n"
        "Course : {student.course}\n"
        "Age    : {student.age}\n"
    )
    print(build_student_profile("S001", template))