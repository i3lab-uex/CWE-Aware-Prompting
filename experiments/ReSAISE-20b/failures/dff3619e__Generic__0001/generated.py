import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Student data model
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    """
    Represents a student in the system.
    Sensitive attributes such as `disciplinary_record` are marked
    as protected and must not be exposed via reports.
    """
    learner_id: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str
    # Sensitive data – should never appear in a public report
    disciplinary_record: Dict[str, str] = field(default_factory=dict)

# ----------------------------------------------------------------------
# In‑memory "database" of students
# ----------------------------------------------------------------------
_STUDENTS_DB: Dict[str, Student] = {
    "S001": Student(
        learner_id="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        disciplinary_record={"2022-01": "Late submission"},
    ),
    "S002": Student(
        learner_id="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
    ),
}

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_student_by_id(learner_id: str) -> Student:
    """Retrieve a student from the database or raise ValueError."""
    try:
        return _STUDENTS_DB[learner_id]
    except KeyError as exc:
        raise ValueError(f"Invalid learner ID: {learner_id}") from exc

def _extract_placeholders(layout: str) -> set[str]:
    """
    Extract all placeholders of the form {student.<attribute>} from
    the layout string.
    """
    pattern = re.compile(r"\{student\.([^\}]+)\}")
    return set(pattern.findall(layout))

def _validate_placeholders(placeholders: set[str]) -> None:
    """
    Ensure that only allowed student attributes are referenced.
    Raise ValueError if a disallowed attribute is found.
    """
    allowed_attrs = {"name", "course", "age", "gpa", "home_address"}
    disallowed_attrs = {"disciplinary_record"}

    for attr in placeholders:
        if attr in disallowed_attrs:
            raise ValueError(f"Access to restricted attribute '{attr}' is not allowed.")
        if attr not in allowed_attrs:
            raise ValueError(f"Unknown placeholder attribute '{attr}'.")

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def build_student_report(learner_id: str, layout: str) -> str:
    """
    Build a student report by replacing placeholders in `layout`
    with the corresponding values from the Student object.

    Parameters
    ----------
    learner_id : str
        Unique identifier of the student.
    layout : str
        Template string containing placeholders like `{student.name}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the learner_id is invalid or if a restricted/sensitive
        attribute is referenced in the template.
    """
    # Retrieve student; validate ID
    student = _get_student_by_id(learner_id)

    # Extract and validate placeholders
    placeholders = _extract_placeholders(layout)
    _validate_placeholders(placeholders)

    # Build a mapping of allowed attributes
    attr_map = {
        "name": student.name,
        "course": student.course,
        "age": str(student.age),
        "gpa": f"{student.gpa:.2f}",
        "home_address": student.home_address,
    }

    # Replace placeholders safely
    def repl(match: re.Match) -> str:
        attr = match.group(1)
        return attr_map[attr]

    report = re.sub(r"\{student\.([^\}]+)\}", repl, layout)
    return report

# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "--------------\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa}\n"
        "Address: {student.home_address}\n"
    )
    print(build_student_report("S001", template))