import re
from dataclasses import dataclass, asdict
from typing import Dict

# ----------------------------------------------------------------------
#  Data model
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    """A simple student record."""
    stu_id: str
    name: str
    course: str
    age: int
    GPA: float
    home_address: str  # Sensitive
    discipline_record: str  # Sensitive


# ----------------------------------------------------------------------
#  In‑memory "database"
# ----------------------------------------------------------------------
_STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        stu_id="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="No violations",
    ),
    "S002": Student(
        stu_id="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission on 2024-06-10",
    ),
}


# ----------------------------------------------------------------------
#  Allowed fields for report generation
# ----------------------------------------------------------------------
_ALLOWED_FIELDS = {"name", "course", "age", "GPA"}


def _extract_placeholders(template: str) -> set:
    """
    Extract all placeholders of the form {field} from a format string.
    """
    return set(re.findall(r"{([^{}]+)}", template))


def create_student_report(stu_id: str, report_template: str) -> str:
    """
    Generate a student report by formatting `report_template` with the
    specified student's data.

    Parameters
    ----------
    stu_id : str
        Unique identifier of the student.
    report_template : str
        A format string containing placeholders such as `{name}` or
        `{course}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student does not exist, or if the template references a
        disallowed (sensitive) field.
    """
    # 1. Retrieve the student record
    student = _STUDENT_DB.get(stu_id)
    if not student:
        raise ValueError(f"Student ID '{stu_id}' does not exist.")

    # 2. Validate placeholders
    placeholders = _extract_placeholders(report_template)
    for field in placeholders:
        if field not in _ALLOWED_FIELDS:
            raise ValueError(
                f"Unauthorized access to sensitive data field '{field}'. "
                "Allowed fields: {0}".format(", ".join(sorted(_ALLOWED_FIELDS)))
            )

    # 3. Prepare safe mapping
    student_dict = asdict(student)
    safe_mapping = {k: v for k, v in student_dict.items() if k in _ALLOWED_FIELDS}

    # 4. Format the report
    try:
        report = report_template.format(**safe_mapping)
    except KeyError as exc:
        raise ValueError(f"Missing field in template: {exc}") from None

    return report


# ----------------------------------------------------------------------
#  Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Student Report\n"
        "Name: {name}\n"
        "Course: {course}\n"
        "Age: {age}\n"
        "GPA: {GPA:.2f}\n"
    )
    print(create_student_report("S001", tmpl))