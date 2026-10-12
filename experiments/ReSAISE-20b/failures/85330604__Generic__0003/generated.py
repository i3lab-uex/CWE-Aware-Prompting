import re
from dataclasses import dataclass, fields
from typing import Dict

# ------------------------------------------------------------------
# Mock student data store (in a real system this would be a database)
# ------------------------------------------------------------------
@dataclass
class Student:
    id: str          # unique identifier
    name: str
    course: str
    age: int
    GPA: float
    home_address: str   # sensitive
    discipline_record: str  # sensitive


# Example in-memory "database"
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
        discipline_record="Late assignment"
    ),
}


# ------------------------------------------------------------------
# Report generation function
# ------------------------------------------------------------------
ALLOWED_FIELDS = {"name", "course", "age", "GPA"}

PLACEHOLDER_PATTERN = re.compile(r"\{([^{}]+)\}")

def create_student_report(stu_id: str, report_template: str) -> str:
    """
    Generates a student report from the provided template.

    Parameters
    ----------
    stu_id : str
        Unique identifier of the student.
    report_template : str
        Format string containing placeholders like `{student.name}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student does not exist or if a placeholder references
        disallowed sensitive data.
    """
    # 1. Retrieve student record
    student = STUDENT_DB.get(stu_id)
    if not student:
        raise ValueError(f"Student with ID '{stu_id}' does not exist.")

    # 2. Validate placeholders
    for placeholder in PLACEHOLDER_PATTERN.findall(report_template):
        # Expected format: student.attribute
        parts = placeholder.split(".")
        if len(parts) != 2 or parts[0] != "student":
            raise ValueError(f"Invalid placeholder format: '{{{placeholder}}}'")

        attr = parts[1]
        if attr not in ALLOWED_FIELDS:
            raise ValueError(
                f"Access to sensitive attribute '{attr}' is not permitted."
            )

    # 3. Build a mapping of allowed attributes
    student_dict = {field: getattr(student, field) for field in ALLOWED_FIELDS}

    # 4. Perform formatting
    try:
        report = report_template.format(**{"student": student_dict})
    except KeyError as e:
        raise ValueError(f"Missing attribute in template: {e}") from e
    except Exception as exc:
        raise ValueError(f"Error formatting report: {exc}") from exc

    return report


# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.GPA:.2f}"
    )
    print(create_student_report("S001", template))