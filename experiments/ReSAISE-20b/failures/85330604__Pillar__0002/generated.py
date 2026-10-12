import re
from typing import Dict

# -------------------- Mock system data ---------------------------------
class Student:
    """
    Simple student representation. In a real system this would be an ORM model.
    """
    def __init__(self, stu_id: str, name: str, course: str,
                 age: int, gpa: float, home_address: str, discipline_record: str):
        self.id = stu_id
        self.name = name
        self.course = course
        self.age = age
        self.gpa = gpa
        self.home_address = home_address          # Sensitive
        self.discipline_record = discipline_record  # Sensitive

# A simple in‑memory "database" of students
_STUDENT_DB: Dict[str, Student] = {
    "S001": Student("S001", "Alice Smith", "Computer Science",
                    20, 3.8, "123 Main St", "None"),
    "S002": Student("S002", "Bob Jones", "Mathematics",
                    22, 3.5, "456 Elm St", "Late submission"),
    # Add more students as needed
}

# -------------------- Helper functions ---------------------------------
def _get_student(stu_id: str) -> Student:
    """
    Retrieve a student from the mock database.
    Raises ValueError if the ID does not exist.
    """
    try:
        return _STUDENT_DB[stu_id]
    except KeyError as exc:
        raise ValueError(f"Student ID '{stu_id}' does not exist.") from exc

def _extract_placeholders(template: str) -> set:
    """
    Find all placeholders in the form {student.<attribute>} within the template.
    Returns a set of attribute names.
    """
    pattern = r"\{student\.([a-zA-Z_][a-zA-Z0-9_]*)\}"
    return set(re.findall(pattern, template))

def _validate_placeholders(placeholders: set):
    """
    Ensure that no sensitive attributes are requested.
    Sensitive fields: home_address, discipline_record
    """
    sensitive = {"home_address", "discipline_record"}
    unauthorized = placeholders & sensitive
    if unauthorized:
        raise ValueError(f"Unauthorized access to sensitive data: {', '.join(unauthorized)}")

def _render_template(template: str, student: Student) -> str:
    """
    Render the template using only allowed attributes.
    """
    # Build a dict of permitted attributes
    data = {
        "name": student.name,
        "course": student.course,
        "age": student.age,
        "gpa": student.gpa
    }
    # Use a simple replacement strategy
    def replacer(match):
        key = match.group(1)
        return str(data[key])

    rendered = re.sub(r"\{student\.([a-zA-Z_][a-zA-Z0-9_]*)\}", replacer, template)
    return rendered

# -------------------- Main function ------------------------------------
def create_student_report(stu_id: str, report_template: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    stu_id : str
        Unique identifier for the student.
    report_template : str
        A format string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The rendered report string.

    Raises
    ------
    ValueError
        If the student ID does not exist or if the template requests
        sensitive data.
    """
    # 1. Retrieve student (raises ValueError if not found)
    student = _get_student(stu_id)

    # 2. Extract and validate placeholders
    placeholders = _extract_placeholders(report_template)
    _validate_placeholders(placeholders)

    # 3. Render the template
    report = _render_template(report_template, student)
    return report

# -------------------- Example usage ------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Student Report\n"
        "---------------\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa:.2f}\n"
    )
    try:
        print(create_student_report("S001", tmpl))
    except ValueError as e:
        print(f"Error: {e}")