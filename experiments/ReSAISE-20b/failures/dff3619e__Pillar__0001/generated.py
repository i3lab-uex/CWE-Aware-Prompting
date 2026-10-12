import re
from typing import Dict

# ----------------------------------------------------------------------
# Student data model
# ----------------------------------------------------------------------
class Student:
    """
    Represents a student with personal and academic information.
    Only non-sensitive attributes are exposed for reporting purposes.
    """
    __slots__ = ("id", "name", "course", "age", "gpa",
                 "_home_address", "_disciplinary_record")

    def __init__(self, id: str, name: str, course: str,
                 age: int, gpa: float,
                 home_address: str, disciplinary_record: str):
        self.id = id
        self.name = name
        self.course = course
        self.age = age
        self.gpa = gpa
        # Sensitive data stored in private slots
        self._home_address = home_address
        self._disciplinary_record = disciplinary_record

    # Property getters for non-sensitive data only
    @property
    def age(self) -> int:
        return self.__dict__["age"]

    @property
    def gpa(self) -> float:
        return self.__dict__["gpa"]

# ----------------------------------------------------------------------
# In‑memory student registry
# ----------------------------------------------------------------------
STUDENT_REGISTRY: Dict[str, Student] = {
    "A123": Student(
        id="A123",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        disciplinary_record="None"
    ),
    "B456": Student(
        id="B456",
        name="Bob Jones",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Rivertown",
        disciplinary_record="Late submission"
    ),
}

# ----------------------------------------------------------------------
# Report generation
# ----------------------------------------------------------------------
_ALLOWED_ATTRIBUTES = {"name", "course", "age", "gpa"}

_PLACEHOLDER_RE = re.compile(r"\{student\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def _validate_template(template: str) -> None:
    """
    Ensure the template does not reference restricted attributes.
    Raises ValueError if a forbidden attribute is detected.
    """
    for match in _PLACEHOLDER_RE.finditer(template):
        attr = match.group(1)
        if attr not in _ALLOWED_ATTRIBUTES:
            raise ValueError(
                f"Template references restricted attribute '{attr}'. "
                "Access to sensitive data is prohibited."
            )

def _render_template(template: str, student: Student) -> str:
    """
    Safely replace placeholders in the template with actual student data.
    Only attributes from _ALLOWED_ATTRIBUTES are accessible.
    """
    def replacer(match: re.Match) -> str:
        attr = match.group(1)
        value = getattr(student, attr)
        return str(value)

    return _PLACEHOLDER_RE.sub(replacer, template)

def build_student_report(learner_id: str, layout: str) -> str:
    """
    Generate a report for the student identified by `learner_id`
    using the provided `layout` template.

    Parameters
    ----------
    learner_id : str
        Unique identifier of the student.
    layout : str
        Template containing placeholders such as '{student.name}'.

    Returns
    -------
    str
        The fully rendered report string.

    Raises
    ------
    ValueError
        If the student ID is unknown, or if the template attempts to
        access restricted/sensitive data.
    """
    # 1. Validate student ID existence
    student = STUDENT_REGISTRY.get(learner_id)
    if student is None:
        raise ValueError(f"Invalid learner ID: {learner_id}")

    # 2. Validate the template against restricted attributes
    _validate_template(layout)

    # 3. Render the template with safe attribute access
    return _render_template(layout, student)

# ----------------------------------------------------------------------
# Example usage (commented out to keep module import safe)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     template = (
#         "Student Report\n"
#         "Name: {student.name}\n"
#         "Course: {student.course}\n"
#         "Age: {student.age}\n"
#         "GPA: {student.gpa}"
#     )
#     print(build_student_report("A123", template))