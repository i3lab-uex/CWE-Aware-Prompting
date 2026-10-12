import re
from dataclasses import dataclass, fields

# ----------------------------------------------------------------------
#  Student data model (simplified for this example)
# ----------------------------------------------------------------------
@dataclass
class Student:
    """Represents a student with personal and academic data."""
    name: str
    course: str
    age: int
    gpa: float
    home_address: str  # sensitive
    disciplinary_record: str  # sensitive


# ----------------------------------------------------------------------
#  In‑memory "database" of students
# ----------------------------------------------------------------------
STUDENT_DB = {
    "S001": Student(
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        disciplinary_record="None"
    ),
    "S002": Student(
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        disciplinary_record="Late submission"
    ),
}


# ----------------------------------------------------------------------
#  Build student report
# ----------------------------------------------------------------------
def build_student_report(learner_id: str, layout: str) -> str:
    """
    Generate a student report by substituting placeholders in *layout* with
    attributes from the Student instance identified by *learner_id*.

    Parameters
    ----------
    learner_id : str
        Unique identifier of the student.
    layout : str
        Template string containing placeholders in the form `{student.<attr>}`.

    Returns
    -------
    str
        The fully rendered report.

    Raises
    ------
    ValueError
        If the learner_id is not found, or if a placeholder references a
        restricted or non‑existent attribute.
    """
    # ------------------------------------------------------------------
    #  Validate learner_id and fetch student
    # ------------------------------------------------------------------
    if learner_id not in STUDENT_DB:
        raise ValueError(f"Invalid student ID: {learner_id}")

    student = STUDENT_DB[learner_id]

    # ------------------------------------------------------------------
    #  Determine allowed attributes (public data only)
    # ------------------------------------------------------------------
    # All dataclass fields except those flagged as sensitive
    _sensitive_fields = {"home_address", "disciplinary_record"}
    allowed_attrs = {
        f.name for f in fields(student) if f.name not in _sensitive_fields
    }

    # ------------------------------------------------------------------
    #  Replace placeholders
    # ------------------------------------------------------------------
    placeholder_pattern = re.compile(r"\{student\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    def _replace(match: re.Match) -> str:
        attr_name = match.group(1)
        if attr_name not in allowed_attrs:
            raise ValueError(
                f"Access to restricted or unknown attribute '{attr_name}' is not allowed."
            )
        value = getattr(student, attr_name)
        return str(value)

    try:
        rendered = placeholder_pattern.sub(_replace, layout)
    except ValueError as exc:
        # Re‑raise with a clear message
        raise ValueError(f"Failed to build report: {exc}") from exc

    return rendered


# ----------------------------------------------------------------------
#  Example usage (for manual testing)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "---------------\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa:.2f}\n"
    )
    print(build_student_report("S001", template))