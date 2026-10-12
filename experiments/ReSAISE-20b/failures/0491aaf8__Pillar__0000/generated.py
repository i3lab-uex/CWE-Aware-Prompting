import re
from types import SimpleNamespace

# --- Mock Student class (would normally come from the system) ---
class Student:
    def __init__(self, student_id: str, name: str, course: str,
                 age: int, GPA: float, home_address: str, discipline_record: list):
        self.id = student_id
        self.name = name
        self.course = course
        self.age = age
        self.GPA = GPA
        self.home_address = home_address
        self.discipline_record = discipline_record


# --- In‑memory registry of students for the example ---
class StudentRegistry:
    def __init__(self):
        self._students = {}

    def add(self, student: Student) -> None:
        self._students[student.id] = student

    def get(self, student_id: str) -> Student:
        try:
            return self._students[student_id]
        except KeyError as exc:
            raise ValueError(f"Student ID '{student_id}' not found") from exc


# --- Global registry instance ---
_registry = StudentRegistry()


def create_student_summary(id: str, format_string: str) -> str:
    """
    Generate a student report using the provided template.

    Args:
        id: Unique identifier of the student.
        format_string: A string containing placeholders such as
                       '{student.name}', '{student.course}', etc.

    Returns:
        A formatted string containing the student's information.

    Raises:
        ValueError: If the student ID does not exist or if a sensitive
                    attribute is requested in the template.
    """
    # 1. Retrieve student from registry (raises ValueError if missing)
    student = _registry.get(id)

    # 2. Detect any attempt to access sensitive data
    sensitive_patterns = [r'\bGPA\b', r'\bhome_address\b']
    for pattern in sensitive_patterns:
        if re.search(pattern, format_string):
            raise ValueError("Attempt to access sensitive attribute(s)")

    # 3. Build a safe namespace containing only non‑sensitive attributes
    allowed_attrs = {
        'name': student.name,
        'course': student.course,
        'age': student.age
    }
    safe_student = SimpleNamespace(**allowed_attrs)

    # 4. Format the string using a protected namespace
    try:
        result = format_string.format(student=safe_student)
    except AttributeError as exc:
        # In case the template references a missing attribute
        raise ValueError(f"Invalid placeholder in format string: {exc}") from exc

    return result


# ----------------- Example usage (for testing) -----------------
if __name__ == "__main__":
    # Populate the registry with a sample student
    _registry.add(
        Student(
            student_id="S123",
            name="Alice Johnson",
            course="Computer Science",
            age=20,
            GPA=3.8,
            home_address="123 Maple St.",
            discipline_record=[]
        )
    )

    # Valid template
    template = "Student Report:\nName: {student.name}\nCourse: {student.course}\nAge: {student.age}"
    print(create_student_summary("S123", template))

    # Attempt to access sensitive data (will raise ValueError)
    bad_template = "GPA: {student.GPA}"
    try:
        print(create_student_summary("S123", bad_template))
    except ValueError as e:
        print(f"Error: {e}")