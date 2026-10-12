import re
from dataclasses import dataclass, asdict
from typing import Dict

# --- Mock student database ---------------------------------------------------
@dataclass(frozen=True)
class Student:
    name: str
    course: str
    age: int
    GPA: float
    home_address: str  # sensitive
    discipline_record: str  # sensitive

# Example in‑memory store keyed by token
_student_db: Dict[str, Student] = {
    "token123": Student(
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Main St, Springfield",
        discipline_record="None"
    ),
    # Add more students as needed
}

# --- Core functionality ------------------------------------------------------
_ALLOWED_FIELDS = {"name", "course", "age", "GPA"}

_PLACEHOLDER_RE = re.compile(r"\{student\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def compile_student_report(student_token: str, report_template: str) -> str:
    """
    Generate a student report by substituting allowed fields into the template.

    Parameters
    ----------
    student_token : str
        Unique identifier for a student.
    report_template : str
        Template string containing placeholders like `{student.name}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the token is unknown, or if a placeholder refers to a disallowed field.
    """
    # 1. Retrieve the student
    try:
        student = _student_db[student_token]
    except KeyError as exc:
        raise ValueError(f"Student token '{student_token}' not found.") from exc

    # 2. Find all placeholders
    matches = _PLACEHOLDER_RE.findall(report_template)

    # 3. Validate and replace placeholders
    def replacement(match: re.Match) -> str:
        field = match.group(1)
        if field not in _ALLOWED_FIELDS:
            raise ValueError(f"Access to sensitive or unknown field '{field}' is not permitted.")
        value = getattr(student, field)
        return str(value)

    try:
        report = _PLACEHOLDER_RE.sub(replacement, report_template)
    except ValueError as exc:
        # Re‑raise with a generic message to avoid leaking internal details
        raise ValueError(str(exc)) from None

    return report


# --- Example usage ------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.GPA:.2f}\n"
    )
    try:
        print(compile_student_report("token123", template))
    except ValueError as e:
        print(f"Error: {e}")