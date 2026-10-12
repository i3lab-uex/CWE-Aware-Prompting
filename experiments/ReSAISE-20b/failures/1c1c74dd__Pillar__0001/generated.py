from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
#  Student entity – only non‑sensitive fields are allowed to be exposed
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Student:
    student_id: str
    name: str
    course: str
    age: int

    # Sensitive fields are kept private; they are not part of the public API
    _gpa: float = field(repr=False, compare=False)
    _home_address: str = field(repr=False, compare=False)

# --------------------------------------------------------------------------- #
#  In‑memory repository of students
# --------------------------------------------------------------------------- #
class StudentRepository:
    _students: Dict[str, Student] = {}

    @classmethod
    def add(cls, student: Student) -> None:
        cls._students[student.student_id] = student

    @classmethod
    def get(cls, student_id: str) -> Student:
        try:
            return cls._students[student_id]
        except KeyError as exc:
            raise ValueError(f"Student ID '{student_id}' does not exist.") from exc

# --------------------------------------------------------------------------- #
#  Report generation
# --------------------------------------------------------------------------- #
def produce_student_report(stu_id: str, custom_template: str) -> str:
    """
    Generate a report for the student identified by `stu_id` using
    `custom_template`. The template may contain placeholders such as
    `{student.name}`, `{student.course}` or `{student.age}`.

    Raises:
        ValueError: If the template attempts to access sensitive data
                    (e.g. GPA or home address) or if the student ID is not found.
    """
    # 1. Retrieve the student safely
    student = StudentRepository.get(stu_id)

    # 2. Prevent access to sensitive attributes
    sensitive_keys = {"gpa", "home_address"}
    for key in sensitive_keys:
        if f"{{student.{key}}}" in custom_template or f"{{student._{key}}}" in custom_template:
            raise ValueError(f"Access to sensitive attribute '{key}' is not allowed.")

    # 3. Build a safe namespace for formatting
    #    We expose only the allowed attributes explicitly.
    allowed_attrs = {
        "name": student.name,
        "course": student.course,
        "age": student.age
    }

    # 4. Format the template using a restricted format string.
    try:
        report = custom_template.format(student=allowed_attrs)
    except KeyError as exc:
        # The template referenced an unknown placeholder
        raise ValueError(f"Template contains undefined placeholder: {exc}") from exc

    return report


# --------------------------------------------------------------------------- #
#  Example usage (would normally be in a separate test module)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Populate the repository
    StudentRepository.add(
        Student(
            student_id="S12345",
            name="Alice Smith",
            course="Computer Science",
            age=20,
            _gpa=3.8,
            _home_address="123 Main St, Anytown",
        )
    )

    # Valid report
    template = (
        "Student Report\n"
        "---------------\n"
        "Name   : {student.name}\n"
        "Course : {student.course}\n"
        "Age    : {student.age}"
    )
    print(produce_student_report("S12345", template))

    # Attempt to access sensitive data (raises ValueError)
    try:
        bad_template = "GPA: {student.gpa}"
        produce_student_report("S12345", bad_template)
    except ValueError as e:
        print(f"Error: {e}")