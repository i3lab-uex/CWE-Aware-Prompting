import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------------
# 1. Student data model
# ------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    """Immutable representation of a student."""
    name: str
    course: str
    age: int
    gpa: float
    home_address: str
    disciplinary_record: str = field(repr=False)  # Sensitive data


# ------------------------------------------------------------------
# 2. In‑memory “database” of students
# ------------------------------------------------------------------
# In a real system this would be replaced by a persistent datastore.
_STUDENT_DB: Dict[str, Student] = {
    "ABC123": Student(
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        disciplinary_record="No violations"
    ),
    "XYZ789": Student(
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        disciplinary_record="Late assignment: 2/2024"
    ),
}


# ------------------------------------------------------------------
# 3. Allowed attributes for formatting
# ------------------------------------------------------------------
_ALLOWED_ATTRS = {
    "name",
    "course",
    "age",
    "gpa",
    "home_address"
}  # disciplinary_record is intentionally omitted


# ------------------------------------------------------------------
# 4. Core function
# ------------------------------------------------------------------
def compile_student_profile(learner_code: str, profile_template: str) -> str:
    """
    Generate a student report by filling placeholders in ``profile_template``.
    
    Parameters
    ----------
    learner_code : str
        Unique identifier for the student.
    profile_template : str
        A string containing placeholders such as ``{student.name}``.
    
    Returns
    -------
    str
        The report with placeholders replaced by the student's data.
    
    Raises
    ------
    ValueError
        If ``learner_code`` is not found, or if the template tries to access a
        restricted attribute.
    """
    # ------------------------------------------------------------------
    # 4.1 Validate student ID and fetch data
    # ------------------------------------------------------------------
    try:
        student = _STUDENT_DB[learner_code]
    except KeyError as exc:
        raise ValueError(f"Invalid learner code: {learner_code}") from exc

    # ------------------------------------------------------------------
    # 4.2 Find all placeholders of the form {student.<attr>}
    # ------------------------------------------------------------------
    placeholder_pattern = re.compile(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")
    placeholders = placeholder_pattern.findall(profile_template)

    # ------------------------------------------------------------------
    # 4.3 Ensure each placeholder references an allowed attribute
    # ------------------------------------------------------------------
    for attr in set(placeholders):
        if attr not in _ALLOWED_ATTRS:
            raise ValueError(
                f"Access to restricted or unknown attribute '{attr}' is not permitted."
            )

    # ------------------------------------------------------------------
    # 4.4 Replace placeholders safely
    # ------------------------------------------------------------------
    def replacer(match: re.Match) -> str:
        attr_name = match.group(1)
        value = getattr(student, attr_name)
        return str(value)

    report = placeholder_pattern.sub(replacer, profile_template)

    return report


# ------------------------------------------------------------------
# 5. Example usage (uncomment to test)
# ------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa:.2f}\n"
        "Address: {student.home_address}\n"
    )
    print(compile_student_profile("ABC123", template))