import re
from dataclasses import dataclass, asdict
from typing import Dict

# --------------------------------------------------------------------
# Mock student data store (in a real system this would be replaced by
# database queries or an external service).
# --------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    stu_id: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str          # Sensitive
    discipline_record: str     # Sensitive

# Example in-memory store (for demonstration purposes)
STUDENT_STORE: Dict[str, Student] = {
    "S001": Student(
        stu_id="S001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        stu_id="S002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission"
    ),
}

# --------------------------------------------------------------------
# Allowed attributes for inclusion in reports
# --------------------------------------------------------------------
ALLOWED_ATTRIBUTES = {"name", "course", "age", "gpa"}

# --------------------------------------------------------------------
def _extract_placeholders(template: str) -> set:
    """
    Extract placeholder names from a format string.
    Supports nested fields (e.g., {student.name}) by taking the part
    before any dot.
    """
    placeholders = set()
    # Regex to find { ... } patterns
    for match in re.finditer(r"{([^{}]+)}", template):
        field = match.group(1).strip()
        # Take only the first part before a dot if present
        field_name = field.split(".")[0]
        placeholders.add(field_name)
    return placeholders

def create_student_report(stu_id: str, report_template: str) -> str:
    """
    Generate a student report by formatting the provided template with
    allowed attributes from the specified student's record.

    Args:
        stu_id (str): Unique identifier of the student.
        report_template (str): Format string containing placeholders.

    Returns:
        str: The formatted report.

    Raises:
        ValueError: If the student does not exist, or if the template
                    attempts to access sensitive data.
    """
    # 1. Retrieve student record
    student = STUDENT_STORE.get(stu_id)
    if not student:
        raise ValueError(f"Student ID '{stu_id}' does not exist.")

    # 2. Validate template placeholders
    placeholders = _extract_placeholders(report_template)
    disallowed = placeholders - ALLOWED_ATTRIBUTES
    if disallowed:
        raise ValueError(
            f"Unauthorized access to sensitive data: {', '.join(sorted(disallowed))}"
        )

    # 3. Prepare context dictionary
    student_dict = {k: getattr(student, k) for k in ALLOWED_ATTRIBUTES}

    # 4. Format the report
    try:
        formatted_report = report_template.format(**student_dict)
    except KeyError as e:
        # This should not happen because we validated placeholders
        raise ValueError(f"Missing placeholder in template: {e}") from e

    return formatted_report


# --------------------------------------------------------------------
# Example usage (for testing purposes)
# --------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "Name: {name}\n"
        "Course: {course}\n"
        "Age: {age}\n"
        "GPA: {gpa}"
    )
    try:
        print(create_student_report("S001", template))
    except ValueError as exc:
        print(f"Error: {exc}")