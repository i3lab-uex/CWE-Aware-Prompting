import re
from dataclasses import dataclass, asdict
from typing import Dict

# --------------------------------------------------------------------------- #
#   Domain model and in‑memory repository                                   #
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    """Represents a student in the system."""
    learner_id: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str
    disciplinary_record: str  # Sensitive field

# Simple in‑memory repository for demo purposes.
class StudentRepository:
    _students: Dict[str, Student] = {}

    @classmethod
    def add(cls, student: Student) -> None:
        cls._students[student.learner_id] = student

    @classmethod
    def get(cls, learner_id: str) -> Student:
        try:
            return cls._students[learner_id]
        except KeyError as exc:
            raise ValueError(f"Invalid learner ID: {learner_id}") from exc

# --------------------------------------------------------------------------- #
#   Helper for safe placeholder resolution                                 #
# --------------------------------------------------------------------------- #

_RE_PLACEHOLDER = re.compile(r"\{(?P<path>[^}]+)\}")

# Fields that are considered sensitive and must not be exposed.
_RESTRICTED_FIELDS = {"disciplinary_record"}

def _extract_placeholder_values(student: Student) -> Dict[str, str]:
    """
    Convert a Student instance into a dict that can be safely used for string
    formatting. Restricted fields are omitted to avoid accidental leakage.
    """
    values = {}
    for key, value in asdict(student).items():
        if key in _RESTRICTED_FIELDS:
            continue  # skip sensitive data
        values[key] = str(value)
    return values

def _validate_placeholders(template: str) -> None:
    """
    Ensure that all placeholders refer to allowed student attributes.
    Raises ValueError if a restricted or unknown attribute is used.
    """
    for match in _RE_PLACEHOLDER.finditer(template):
        path = match.group("path")
        if not path.startswith("student."):
            raise ValueError(f"Unsupported placeholder: {match.group(0)}")
        attr = path.split(".", 1)[1]
        if attr in _RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted field '{attr}' is not allowed.")
        # Unknown attributes will be caught later when formatting.

# --------------------------------------------------------------------------- #
#   Main API function                                                      #
# --------------------------------------------------------------------------- #

def build_student_report(learner_id: str, layout: str) -> str:
    """
    Generate a student report by replacing placeholders in *layout* with
    corresponding values from the Student identified by *learner_id*.

    Parameters:
        learner_id (str): Unique identifier of the student.
        layout (str): Template containing placeholders like `{student.name}`.

    Returns:
        str: The rendered report.

    Raises:
        ValueError: If the learner_id is invalid, or if a placeholder
                    references a restricted field.
    """
    # 1. Retrieve the student, raising ValueError if not found
    student = StudentRepository.get(learner_id)

    # 2. Validate placeholders to guard against restricted data
    _validate_placeholders(layout)

    # 3. Prepare a mapping of allowed attributes for formatting
    values = _extract_placeholder_values(student)

    # 4. Perform the actual substitution; unknown keys will raise KeyError
    try:
        report = layout.format(**values)
    except KeyError as exc:
        raise ValueError(f"Unknown placeholder: {exc}") from exc

    return report


# --------------------------------------------------------------------------- #
#   Example usage (commented out – remove if running as a module)           #
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Populate repository with a sample student
    StudentRepository.add(
        Student(
            learner_id="S12345",
            name="Alice Johnson",
            course="Computer Science",
            age=20,
            gpa=3.8,
            home_address="123 Maple St, Townsville",
            disciplinary_record="None"
        )
    )

    template = (
        "Student Report\n"
        "---------------\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa}\n"
    )

    print(build_student_report("S12345", template))