import re
from typing import Dict

# --------------------------------------------------------------------
# Student data model – in a real system this would be replaced by the
# actual ORM or persistence layer.  Only the attributes that are meant
# to be public are listed here.
# --------------------------------------------------------------------
class Student:
    def __init__(
        self,
        stu_id: str,
        name: str,
        course: str,
        age: int,
        gpa: float,
        home_address: str,
        disciplinary_record: str,  # sensitive
    ):
        self.stu_id = stu_id
        self.name = name
        self.course = course
        self.age = age
        self.gpa = gpa
        self.home_address = home_address
        # The disciplinary record is considered sensitive and must not
        # be exposed by the summary function.
        self._disciplinary_record = disciplinary_record

    @property
    def disciplinary_record(self):
        # Accessing this property is considered a security risk.
        raise PermissionError("Access to disciplinary record is forbidden")

# --------------------------------------------------------------------
# A simple in‑memory registry of students.  In a real application this
# would be replaced by database look‑ups.
# --------------------------------------------------------------------
_STUDENT_REGISTRY: Dict[str, Student] = {}

def register_student(student: Student) -> None:
    """Register a student in the global registry."""
    _STUDENT_REGISTRY[student.stu_id] = student

# --------------------------------------------------------------------
# Helper – safe formatting
# --------------------------------------------------------------------
_REPLACE_PATTERN = re.compile(r"\{student\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

# Attributes that are considered sensitive and must not be exposed
_SENSITIVE_ATTRS = {"disciplinary_record"}

def _extract_placeholders(template: str) -> set:
    """Return a set of attribute names referenced in the template."""
    return set(_REPLACE_PATTERN.findall(template))

def _get_student_attr(student: Student, attr_name: str):
    """Retrieve an attribute value from a student instance."""
    if attr_name in _SENSITIVE_ATTRS:
        raise ValueError(f"Attempted to expose sensitive attribute '{attr_name}'")
    if not hasattr(student, attr_name):
        raise ValueError(f"Attribute '{attr_name}' does not exist on Student")
    return getattr(student, attr_name)

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------
def create_student_summary(stu_id: str, summary_template: str) -> str:
    """
    Generate a student report based on the supplied template.

    Parameters
    ----------
    stu_id : str
        The unique identifier for the student.
    summary_template : str
        A string containing placeholders in the form {student.<attr>}.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student ID is unknown, or if the template references a
        restricted attribute.
    """
    # Retrieve student – raise ValueError for unknown ID
    student = _STUDENT_REGISTRY.get(stu_id)
    if student is None:
        raise ValueError(f"Student ID '{stu_id}' not found")

    # Scan for placeholders and validate
    placeholders = _extract_placeholders(summary_template)
    for attr in placeholders:
        if attr in _SENSITIVE_ATTRS:
            raise ValueError(f"Template references restricted attribute '{attr}'")
        if not hasattr(student, attr):
            raise ValueError(f"Template references unknown attribute '{attr}'")

    # Perform the substitution safely
    def replacer(match):
        attr_name = match.group(1)
        value = _get_student_attr(student, attr_name)
        return str(value)

    report = _REPLACE_PATTERN.sub(replacer, summary_template)
    return report

# --------------------------------------------------------------------
# Example usage (this part would normally be omitted from a library)
# --------------------------------------------------------------------
if __name__ == "__main__":
    # Create and register a sample student
    s = Student(
        stu_id="S12345",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Townsville",
        disciplinary_record="None",
    )
    register_student(s)

    template = (
        "Student Report\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa}\n"
        "Address: {student.home_address}"
    )

    print(create_student_summary("S12345", template))