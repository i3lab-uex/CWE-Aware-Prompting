import re
from typing import Dict

# --------------------------------------------------------------------------- #
#   Dummy data and Student class (in a real system this would come from a DB)
# --------------------------------------------------------------------------- #
class Student:
    """Represents a student with non‑sensitive and sensitive attributes."""
    def __init__(self, name: str, course: str, age: int,
                 gpa: float, home_address: str, discipline_record: str):
        self.name = name
        self.course = course
        self.age = age
        self.gpa = gpa                    # Sensitive
        self.home_address = home_address  # Sensitive
        self.discipline_record = discipline_record

# A simple in‑memory "database" of students.
STUDENT_DB: Dict[str, Student] = {
    "S001": Student("Alice Smith", "Computer Science", 20, 3.8,
                    "123 Maple St.", "None"),
    "S002": Student("Bob Johnson", "Mathematics", 22, 3.5,
                    "456 Oak Ave.", "Late to class"),
}

# --------------------------------------------------------------------------- #
#   Helper functions
# --------------------------------------------------------------------------- #

def _validate_template(template: str) -> None:
    """
    Ensure that the template does not reference any sensitive attributes.
    Raises ValueError if a forbidden placeholder is found.
    """
    # Find all placeholders like {student.attr}
    placeholders = re.findall(r"{([^{}]+)}", template)
    forbidden_attrs = {"student.gpa", "student.home_address"}
    for ph in placeholders:
        # Normalize: strip spaces, lowercase
        key = ph.strip().lower()
        if key in forbidden_attrs:
            raise ValueError(f"Template attempts to access sensitive data: {{{ph}}}")

def _get_student(stu_id: str) -> Student:
    """Retrieve a student from the database, raising if not found."""
    try:
        return STUDENT_DB[stu_id]
    except KeyError as exc:
        raise ValueError(f"Student ID '{stu_id}' does not exist.") from exc

# --------------------------------------------------------------------------- #
#   Main function
# --------------------------------------------------------------------------- #

def produce_student_report(stu_id: str, custom_template: str) -> str:
    """
    Generate a formatted report for the student identified by `stu_id`.

    Parameters
    ----------
    stu_id : str
        Unique identifier of the student.
    custom_template : str
        A format string containing placeholders like `{student.name}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the template references sensitive attributes or if `stu_id`
        does not exist in the database.
    """
    # Validate template for sensitive data
    _validate_template(custom_template)

    # Retrieve student record
    student = _get_student(stu_id)

    # Prepare a namespace for formatting
    context = {"student": student}

    try:
        report = custom_template.format(**context)
    except KeyError as exc:
        # The template referenced a non‑existent attribute
        raise ValueError(f"Template references unknown placeholder: {exc}") from exc

    return report

# --------------------------------------------------------------------------- #
#   Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "---------------\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
    )
    print(produce_student_report("S001", template))