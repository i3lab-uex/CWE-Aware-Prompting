import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
#  Student data model and a simple in‑memory registry
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    """Represents a student with basic personal and academic details."""
    learner_code: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str
    disciplinary_record: str = field(repr=False)  # Sensitive information


# Example in‑memory registry (replace with real DB access in production)
_STUDENT_REGISTRY: Dict[str, Student] = {
    "A001": Student(
        learner_code="A001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        disciplinary_record="No violations"
    ),
    "B002": Student(
        learner_code="B002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        disciplinary_record="Late submission in 2023"
    ),
}


# --------------------------------------------------------------------------- #
#  Utility classes
# --------------------------------------------------------------------------- #

class _SafeMapping(dict):
    """
    A mapping that safely resolves attributes from the Student instance.
    Raises KeyError if an attribute is missing.
    """
    def __missing__(self, key):
        raise KeyError(f"Missing placeholder: {key}")


# --------------------------------------------------------------------------- #
#  Main function
# --------------------------------------------------------------------------- #

def compile_student_profile(learner_code: str, profile_template: str) -> str:
    """
    Generate a student report by filling in the provided template with data
    from the Student identified by `learner_code`.

    Parameters:
        learner_code (str): Unique identifier for the student.
        profile_template (str): Template containing placeholders like
                                '{student.name}' or '{student.course}'.

    Returns:
        str: The formatted report string.

    Raises:
        ValueError: If the student ID is invalid or if the template attempts
                    to access restricted attributes.
    """
    # ------------------------------------------------------- #
    # 1. Validate learner_code
    # ------------------------------------------------------- #
    student = _STUDENT_REGISTRY.get(learner_code)
    if student is None:
        raise ValueError(f"Invalid learner code: {learner_code}")

    # ------------------------------------------------------- #
    # 2. Detect restricted placeholders
    # ------------------------------------------------------- #
    RESTRICTED = {"disciplinary_record"}  # attributes that are not allowed in templates

    placeholders = re.findall(r'{student\.([a-zA-Z_][a-zA-Z0-9_]*)}', profile_template)
    if any(name in RESTRICTED for name in placeholders):
        raise ValueError("Template contains restricted or sensitive information")

    # ------------------------------------------------------- #
    # 3. Prepare a mapping for format_map
    # ------------------------------------------------------- #
    data = _SafeMapping()
    data["student"] = student

    # Since format_map will call __getitem__ on the mapping,
    # we provide a custom __getitem__ that resolves nested attributes.
    def _getattr(item):
        parts = item.split(".")
        obj = data
        for part in parts:
            if isinstance(obj, dict):
                # top-level key
                obj = obj[part]
            else:
                try:
                    obj = getattr(obj, part)
                except AttributeError as exc:
                    raise KeyError(f"Attribute '{part}' not found") from exc
        return obj

    # Monkey‑patch format_map to use the custom getter
    original_getitem = data.__getitem__

    def _getitem(key):
        try:
            return _getattr(key)
        except KeyError as exc:
            raise KeyError(f"Missing placeholder: {key}") from exc

    data.__getitem__ = _getitem  # type: ignore[assignment]

    try:
        report = profile_template.format_map(data)
    finally:
        # Restore original __getitem__ to avoid side effects
        data.__getitem__ = original_getitem

    return report


# --------------------------------------------------------------------------- #
#  Example usage (commented out – remove comments to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Student Report:\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa:.2f}\n"
        "Address: {student.home_address}"
    )
    print(compile_student_profile("A001", template))