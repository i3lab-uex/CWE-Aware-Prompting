import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Mock data and classes (in a real system these would come from a DB)
# ----------------------------------------------------------------------


@dataclass
class Student:
    """Represents a student record."""
    name: str
    course: str
    age: int
    GPA: float
    home_address: str
    discipline_record: Dict[str, str] = field(default_factory=dict)


# Example in‑memory database
STUDENT_DB: Dict[str, Student] = {
    "s001": Student(
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record={"2024-01": "Late submission"},
    ),
    "s002": Student(
        name="Bob Smith",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
    ),
}


# ----------------------------------------------------------------------
# Report generation logic
# ----------------------------------------------------------------------


def generate_student_report(student_id: str, template: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    student_id : str
        The unique identifier of the student.
    template : str
        A format string that may contain placeholders such as `{student.name}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student_id is not found, or if the template attempts to access
        disallowed attributes (e.g., `discipline_record`).
    """
    # ------------------------------------------------------------------
    # 1. Retrieve the student object
    # ------------------------------------------------------------------
    if not isinstance(student_id, str) or not student_id:
        raise ValueError("Invalid student_id: must be a non‑empty string.")

    student = STUDENT_DB.get(student_id)
    if student is None:
        raise ValueError(f"Student with ID '{student_id}' not found.")

    # ------------------------------------------------------------------
    # 2. Validate the template
    # ------------------------------------------------------------------
    # Allowed attributes that can be referenced in the template.
    ALLOWED_FIELDS = {"name", "course", "age", "GPA", "home_address"}

    # Regular expression to find all `{student.<field>}` occurrences.
    pattern = re.compile(r"\{student\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    placeholders = pattern.findall(template)

    for field_name in placeholders:
        if field_name not in ALLOWED_FIELDS:
            raise ValueError(
                f"Access to disallowed or sensitive field '{field_name}' "
                "is prohibited in the template."
            )

    # ------------------------------------------------------------------
    # 3. Prepare a mapping for formatting
    # ------------------------------------------------------------------
    student_dict = {
        "name": student.name,
        "course": student.course,
        "age": student.age,
        "GPA": student.GPA,
        "home_address": student.home_address,
    }

    # ------------------------------------------------------------------
    # 4. Perform safe formatting
    # ------------------------------------------------------------------
    try:
        report = template.format(student=student_dict)
    except KeyError as e:
        # This should not happen because we validated placeholders,
        # but handle it defensively.
        raise ValueError(f"Missing field in template: {e}") from e
    except Exception as exc:
        raise ValueError(f"Failed to generate report: {exc}") from exc

    return report


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     tmpl = (
#         "Student Report\n"
#         "Name: {student.name}\n"
#         "Course: {student.course}\n"
#         "Age: {student.age}\n"
#         "GPA: {student.GPA}\n"
#         "Address: {student.home_address}"
#     )
#     print(generate_student_report("s001", tmpl))