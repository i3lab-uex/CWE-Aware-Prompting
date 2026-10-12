import re
from dataclasses import dataclass, field
from typing import Dict

# ---------- Domain model ----------
@dataclass(frozen=True)
class Student:
    name: str
    course: str
    age: int
    gpa: float = field(repr=False)          # Sensitive, should not be exposed
    home_address: str = field(repr=False)   # Sensitive, should not be exposed
    discipline_record: list[str] = field(default_factory=list)

# ---------- In‑memory student store ----------
_STUDENTS: Dict[str, Student] = {
    "S001": Student(
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record=["Late submission", "Library violation"],
    ),
    # Add more students as needed
}

# ---------- Utility ----------
_SENSITIVE_FIELDS = {"gpa", "home_address"}

def _extract_placeholders(template: str) -> set[str]:
    """
    Extract all placeholders in the form {field} or {object.field}
    from a format string.
    """
    pattern = re.compile(r"\{([^{}]+)\}")
    return {m.group(1) for m in pattern.finditer(template)}

def _is_sensitive(field: str) -> bool:
    """
    Determine if a field is considered sensitive.
    The placeholder may be in the form 'student.field'.
    """
    # Normalise to just the field name
    if "." in field:
        _, attr = field.split(".", 1)
    else:
        attr = field
    return attr in _SENSITIVE_FIELDS

# ---------- Main function ----------
def produce_student_report(stu_id: str, custom_template: str) -> str:
    """
    Generate a student report using the provided template.

    Parameters
    ----------
    stu_id : str
        Unique identifier for a student.
    custom_template : str
        A format string containing placeholders such as `{student.name}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student ID does not exist or if the template tries to access
        sensitive attributes (GPA, home address).
    """
    # 1. Validate student existence
    if stu_id not in _STUDENTS:
        raise ValueError(f"Student ID '{stu_id}' does not exist.")

    student = _STUDENTS[stu_id]

    # 2. Inspect placeholders for sensitive data
    placeholders = _extract_placeholders(custom_template)
    for ph in placeholders:
        if _is_sensitive(ph):
            raise ValueError(f"Template contains sensitive placeholder '{ph}'.")

    # 3. Prepare safe namespace for formatting
    safe_namespace = {
        "student": {
            "name": student.name,
            "course": student.course,
            "age": student.age,
            # Expose discipline_record if needed; it's non‑sensitive
            "discipline_record": student.discipline_record,
        }
    }

    # 4. Render the template
    try:
        report = custom_template.format(**safe_namespace)
    except KeyError as e:
        raise ValueError(f"Missing placeholder in template: {e}") from e
    except Exception as exc:
        raise ValueError(f"Error rendering template: {exc}") from exc

    return report