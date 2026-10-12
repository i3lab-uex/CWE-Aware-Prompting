import re
from contextlib import contextmanager
from typing import Dict

# --------------------------------------------------------------------------- #
# 1. Student model – only a minimal in‑memory representation for demo
# --------------------------------------------------------------------------- #
class Student:
    """
    Represents a student with a limited set of public attributes.
    Sensitive fields are omitted or marked as restricted.
    """
    def __init__(self, learner_id: str, name: str, course: str,
                 age: int, gpa: float, address: str):
        self.learner_id = learner_id
        self.name = name
        self.course = course
        self.age = age
        self.gpa = gpa
        self.address = address

    # Restricted fields (should never be exposed via the report)
    _sensitive_fields = {"address", "gpa"}


# --------------------------------------------------------------------------- #
# 2. In‑memory data store – mimics a database connection
# --------------------------------------------------------------------------- #
STUDENTS_DB: Dict[str, Student] = {
    "S001": Student("S001", "Alice Smith", "Computer Science", 20, 3.8,
                    "123 Maple St"),
    "S002": Student("S002", "Bob Johnson", "Mathematics", 22, 3.5,
                    "456 Oak Ave"),
    # Add more students as needed
}


@contextmanager
def db_session():
    """
    Context manager that simulates a database session.
    It ensures the session is closed after use, preventing resource leaks
    (CWE‑664).
    """
    try:
        # In a real implementation, open DB connection here
        yield STUDENTS_DB
    finally:
        # In a real implementation, close DB connection here
        pass


# --------------------------------------------------------------------------- #
# 3. Helper – validate and fetch student
# --------------------------------------------------------------------------- #
def _get_student(learner_id: str) -> Student:
    """
    Retrieves a student from the database or raises ValueError if not found.
    """
    with db_session() as db:
        student = db.get(learner_id)
        if not student:
            raise ValueError(f"Invalid learner ID: {learner_id}")
        return student


# --------------------------------------------------------------------------- #
# 4. Main function – build_student_report
# --------------------------------------------------------------------------- #
PLACEHOLDER_PATTERN = re.compile(r"\{(?P<path>[^}]+)\}")

def build_student_report(learner_id: str, layout: str) -> str:
    """
    Generates a student report based on the provided template.

    Parameters
    ----------
    learner_id : str
        Unique identifier of the student.
    layout : str
        Template string containing placeholders like `{student.name}`.

    Returns
    -------
    str
        The rendered report with placeholders substituted by actual values.

    Raises
    ------
    ValueError
        If the learner ID is invalid or if a placeholder references a
        restricted/sensitive attribute.
    """
    # Fetch the student once – this is our resource acquisition
    student = _get_student(learner_id)

    # Helper to resolve a single placeholder path
    def _resolve_path(path: str):
        """
        Resolves attributes of the form 'student.attr' or nested attributes.
        Only whitelisted attributes are allowed; others raise ValueError.
        """
        parts = path.split(".")
        if not parts or parts[0] != "student":
            raise ValueError(f"Invalid placeholder path: {path}")

        obj = student
        for attr in parts[1:]:
            # Disallow access to restricted fields
            if attr in Student._sensitive_fields:
                raise ValueError(f"Access to restricted attribute '{attr}' is denied")
            if not hasattr(obj, attr):
                raise ValueError(f"Attribute '{attr}' does not exist on Student")
            obj = getattr(obj, attr)
        return str(obj)

    # Replace all placeholders safely
    def _replace(match: re.Match):
        path = match.group("path").strip()
        return _resolve_path(path)

    report = PLACEHOLDER_PATTERN.sub(_replace, layout)
    return report


# --------------------------------------------------------------------------- #
# 5. Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "==============\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
    )
    print(build_student_report("S001", template))