import string
from dataclasses import dataclass, asdict
from typing import Dict

# ----------------------------------------------------------------------
# Mock student storage (in a real system this would be replaced with
# database access logic).  The keys are the unique student identifiers.
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    name: str
    course: str
    age: int
    GPA: float
    home_address: str
    discipline_record: str


# Example data – in practice this would be fetched from a secure source
_STUDENTS: Dict[str, Student] = {
    "S001": Student(
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None",
    ),
    "S002": Student(
        name="Bob Smith",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission in 2023",
    ),
}


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_allowed_attributes(student: Student) -> Dict[str, object]:
    """
    Return a dictionary of attributes that are allowed to be exposed in
    the report.  Sensitive fields (home_address, discipline_record)
    are omitted.
    """
    allowed = {
        "name": student.name,
        "course": student.course,
        "age": student.age,
        "GPA": student.GPA,  # GPA is considered non‑sensitive here
    }
    return allowed


def _validate_template(template: str, allowed_keys: set) -> None:
    """
    Ensure that the template does not reference any disallowed keys.
    Raises ValueError if a forbidden key is found.
    """
    formatter = string.Formatter()
    for literal_text, field_name, format_spec, conversion in formatter.parse(template):
        if field_name:
            # The field_name can contain nested attributes like "student.name".
            # We split on '.' and only check the first part.
            key = field_name.split(".", 1)[0]
            if key not in allowed_keys:
                raise ValueError(
                    f"Unauthorized placeholder '{field_name}' used in report template."
                )


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_student_report(stu_id: str, report_template: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    stu_id : str
        Unique identifier for the student.
    report_template : str
        Template string containing placeholders such as '{name}', '{course}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student ID does not exist or if the template attempts to
        access disallowed (sensitive) attributes.
    """
    # Retrieve student record – raise if not found
    try:
        student = _STUDENTS[stu_id]
    except KeyError as exc:
        raise ValueError(f"Student ID '{stu_id}' not found.") from exc

    # Prepare allowed attributes
    allowed_attrs = _get_allowed_attributes(student)

    # Validate template against allowed keys
    _validate_template(report_template, set(allowed_attrs.keys()))

    # Perform formatting safely
    try:
        report = report_template.format(**allowed_attrs)
    except KeyError as exc:
        # This should not happen because of the validation step
        raise ValueError(f"Missing placeholder in template: {exc}") from exc

    return report


# ----------------------------------------------------------------------
# Example usage (for testing purposes)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "---------------\n"
        "Name: {name}\n"
        "Course: {course}\n"
        "Age: {age}\n"
        "GPA: {GPA:.2f}\n"
    )
    print(create_student_report("S001", template))