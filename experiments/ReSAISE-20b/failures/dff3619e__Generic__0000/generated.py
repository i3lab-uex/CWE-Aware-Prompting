import re
from dataclasses import dataclass
from typing import Dict

# ---------- Student model ----------
@dataclass(frozen=True)
class Student:
    student_id: str
    name: str
    course: str
    age: int
    gpa: float
    address: str  # sensitive field
    disciplinary_record: str

# ---------- In‑memory data store ----------
STUDENTS_DB: Dict[str, Student] = {
    "S001": Student(
        student_id="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        address="123 Maple St, Springfield",
        disciplinary_record="None",
    ),
    "S002": Student(
        student_id="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        address="456 Oak Ave, Shelbyville",
        disciplinary_record="Late submission in CS101",
    ),
}

# ---------- Restricted attributes ----------
RESTRICTED_FIELDS = {"address", "disciplinary_record"}


def build_student_report(learner_id: str, layout: str) -> str:
    """
    Generate a student report by filling in placeholders from the provided layout.

    Parameters
    ----------
    learner_id : str
        Unique identifier for a student.
    layout : str
        Template string containing placeholders such as `{student.name}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the learner_id is unknown, if a restricted field is requested,
        or if placeholder syntax is invalid.
    """

    # Validate student existence
    student = STUDENTS_DB.get(learner_id)
    if not student:
        raise ValueError(f"Unknown learner ID: {learner_id}")

    # Find all placeholders in the layout
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")
    placeholders = placeholder_pattern.findall(layout)

    # Validate each placeholder
    for ph in placeholders:
        # Expecting syntax like 'student.attribute'
        parts = ph.split(".")
        if len(parts) != 2 or parts[0] != "student":
            raise ValueError(f"Invalid placeholder syntax: {{{ph}}}")

        attr = parts[1]
        if attr in RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted field '{attr}' is not allowed.")
        if not hasattr(student, attr):
            raise ValueError(f"Student has no attribute '{attr}'.")

    # Perform the substitution
    try:
        report = layout.format(student=student)
    except Exception as exc:  # Catch any formatting error
        raise ValueError(f"Failed to format report: {exc}") from exc

    return report


# ---------- Example usage ----------
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa:.2f}"
    )
    print(build_student_report("S001", template))