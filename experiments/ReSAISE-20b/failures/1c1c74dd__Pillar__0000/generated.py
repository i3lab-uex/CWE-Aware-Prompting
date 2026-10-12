import string
from dataclasses import dataclass
from typing import Dict

# ----------------------------------------------------------------------
# Student entity definition
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    """Immutable representation of a student."""
    name: str
    course: str
    age: int
    gpa: float          # Sensitive data
    home_address: str   # Sensitive data
    discipline_record: str

# ----------------------------------------------------------------------
# In‑memory student repository (for demonstration purposes)
# ----------------------------------------------------------------------
_STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission of assignment"
    ),
}

# ----------------------------------------------------------------------
# Helper: Safe formatter that blocks sensitive attributes
# ----------------------------------------------------------------------
class _SafeFormatter(string.Formatter):
    """Custom string formatter that forbids access to sensitive fields."""
    _sensitive_keys = {"student.gpa", "student.home_address"}

    def get_field(self, field_name: str, args, kwargs):
        # Detect if the template tries to access a forbidden attribute
        full_name = f"student.{field_name}"
        if full_name in self._sensitive_keys:
            raise ValueError(f"Access to sensitive attribute '{full_name}' is not allowed.")
        return super().get_field(field_name, args, kwargs)

# ----------------------------------------------------------------------
# Main API
# ----------------------------------------------------------------------
def produce_student_report(stu_id: str, custom_template: str) -> str:
    """
    Generate a student report using the supplied template.

    Parameters
    ----------
    stu_id : str
        Unique identifier of the student.
    custom_template : str
        Format string containing placeholders such as '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student ID does not exist or if the template references a sensitive attribute.
    """
    # Validate existence of student
    student = _STUDENT_DB.get(stu_id)
    if not student:
        raise ValueError(f"Student ID '{stu_id}' does not exist.")

    # Prepare a namespace for formatting
    context = {"student": student}

    # Use the safe formatter to process the template
    formatter = _SafeFormatter()
    try:
        report = formatter.format(custom_template, **context)
    except KeyError as exc:
        raise ValueError(f"Missing placeholder in template: {exc}") from exc
    except ValueError as exc:
        # Re‑raise to preserve message about sensitive data
        raise

    return report


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = "Student Report\nName: {student.name}\nCourse: {student.course}\nAge: {student.age}"
    print(produce_student_report("S001", tmpl))