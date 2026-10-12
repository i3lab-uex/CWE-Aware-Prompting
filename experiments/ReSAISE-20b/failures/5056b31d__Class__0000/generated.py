import re
from typing import Any, Dict

# ----------------------------------------------------------------------
# Domain model (simplified for this example)
# ----------------------------------------------------------------------
class Student:
    """
    A minimal representation of a student. In a real system this would
    likely be an ORM model with database access.
    """
    def __init__(
        self,
        student_id: str,
        name: str,
        course: str,
        age: int,
        gpa: float,
        home_address: str,
        discipline_record: str,
    ) -> None:
        self.student_id = student_id
        self.name = name
        self.course = course
        self.age = age
        self.gpa = gpa
        self.home_address = home_address          # Sensitive
        self.discipline_record = discipline_record  # Sensitive


# ----------------------------------------------------------------------
# Mock data store and retrieval function
# ----------------------------------------------------------------------
_STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        student_id="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Main St, Springfield",
        discipline_record="None",
    ),
    "S002": Student(
        student_id="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Springfield",
        discipline_record="Late submission of assignments",
    ),
}

def get_student_by_id(student_id: str) -> Student:
    """
    Retrieve a student from the mock database.
    Raises KeyError if the student does not exist.
    """
    return _STUDENT_DB[student_id]


# ----------------------------------------------------------------------
# Report generation
# ----------------------------------------------------------------------
_ALLOWED_FIELDS = {"name", "course", "age", "gpa"}
_SENSITIVE_FIELDS = {"home_address", "discipline_record"}

def _extract_safe_attrs(student: Student) -> Dict[str, Any]:
    """
    Return a dictionary containing only allowed attributes of the student.
    Raise ValueError if an attempt is made to expose a sensitive attribute.
    """
    attrs = {}
    for key in vars(student).keys():
        if key in _SENSITIVE_FIELDS:
            continue  # never expose sensitive fields
        if key in _ALLOWED_FIELDS or key == "student_id":
            attrs[key] = getattr(student, key)
    return attrs

def generate_student_report(student_id: str, template: str) -> str:
    """
    Generate a report string for the given student using the supplied template.

    Parameters
    ----------
    student_id : str
        Unique identifier of the student.
    template : str
        A format string that may contain placeholders like '{name}' or
        '{course}'. Only the fields defined in _ALLOWED_FIELDS are allowed.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student does not exist, if the template references a disallowed
        field, or if an attempt is made to expose sensitive information.
    """
    try:
        student = get_student_by_id(student_id)
    except KeyError as exc:
        raise ValueError(f"Student with id '{student_id}' not found.") from exc

    # Check template for disallowed placeholders
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")
    placeholders = placeholder_pattern.findall(template)
    for field in placeholders:
        if field not in _ALLOWED_FIELDS and field != "student_id":
            raise ValueError(f"Disallowed placeholder '{field}' in template.")

    # Build the context dictionary
    context = _extract_safe_attrs(student)
    try:
        report = template.format(**context)
    except KeyError as exc:
        # This should not happen due to earlier checks, but guard anyway
        raise ValueError(f"Missing field in context: {exc}") from exc

    return report


# ----------------------------------------------------------------------
# Example usage (would normally be in a separate test module)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Student Report\n"
        "---------------\n"
        "Name: {name}\n"
        "Course: {course}\n"
        "Age: {age}\n"
        "GPA: {gpa:.2f}"
    )
    print(generate_student_report("S001", tmpl))