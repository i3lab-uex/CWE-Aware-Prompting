import re
from dataclasses import dataclass

# Example Student data class – in a real system this would be imported
@dataclass
class Student:
    student_id: str
    name: str
    course: str
    age: int
    GPA: float
    # Sensitive fields that should not be exposed through the report template
    home_address: str = ""
    discipline_record: str = ""

# Simulated database lookup – replace with real persistence in production
_STUDENT_DB = {
    "s123": Student(
        student_id="s123",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Main St, Springfield",
        discipline_record="None"
    ),
    "s456": Student(
        student_id="s456",
        name="Bob Jones",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Springfield",
        discipline_record="Late submission of Assignment 3"
    ),
}

# Allowed fields that can be referenced in the template
_ALLOWED_FIELDS = {
    "student.name",
    "student.course",
    "student.age",
    "student.GPA"
}

def _get_student(student_id: str) -> Student:
    """
    Retrieve a student object from the database.
    Raise ValueError if the student does not exist.
    """
    student = _STUDENT_DB.get(student_id)
    if student is None:
        raise ValueError(f"Student with ID '{student_id}' not found.")
    return student

def _extract_placeholders(template: str) -> set:
    """
    Find all placeholders in the form {student.xxx} within the template.
    Return a set of placeholder names (including 'student.' prefix).
    """
    # Regex to match {something} where something does not contain nested braces
    pattern = r"\{([^\{\}]*)\}"
    matches = re.findall(pattern, template)
    placeholders = set()
    for m in matches:
        # Only consider attributes that start with 'student.'
        if m.startswith("student."):
            placeholders.add(m)
    return placeholders

def generate_student_report(student_id: str, template: str) -> str:
    """
    Generate a student report based on the provided template.
    
    Parameters
    ----------
    student_id : str
        Unique identifier for the student.
    template : str
        Template string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The rendered report string.

    Raises
    ------
    ValueError
        If the student does not exist, or if the template attempts to
        access disallowed fields.
    """
    # Retrieve student data safely
    student = _get_student(student_id)

    # Validate template placeholders
    placeholders = _extract_placeholders(template)
    disallowed = placeholders - _ALLOWED_FIELDS
    if disallowed:
        raise ValueError(
            f"Template contains disallowed fields: {', '.join(disallowed)}"
        )

    # Build a simple namespace for formatting
    namespace = {
        "student.name": student.name,
        "student.course": student.course,
        "student.age": str(student.age),
        "student.GPA": f"{student.GPA:.2f}",
    }

    # Replace placeholders manually to avoid accidental format errors
    def replacer(match):
        key = match.group(1)
        if key in namespace:
            return namespace[key]
        # If placeholder not recognized, leave it unchanged
        return match.group(0)

    rendered = re.sub(r"\{([^\{\}]*)\}", replacer, template)
    return rendered

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     tmpl = "Student {student.name} is enrolled in {student.course}. Age: {student.age}, GPA: {student.GPA}"
#     print(generate_student_report("s123", tmpl))