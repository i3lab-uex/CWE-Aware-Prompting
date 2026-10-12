import re
from typing import Dict

# ------------------------------------------------------------------
# Mock Student class (in real system this would be imported)
# ------------------------------------------------------------------
class Student:
    def __init__(self, name: str, course: str, age: int,
                 gpa: float, address: str, disciplinary_record: str):
        self.name = name
        self.course = course
        self.age = age
        self.gpa = gpa
        self.address = address
        self.disciplinary_record = disciplinary_record

# ------------------------------------------------------------------
# In‑memory registry of students
# ------------------------------------------------------------------
_STUDENT_REGISTRY: Dict[str, Student] = {
    "S12345": Student(
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        address="123 Maple Ave, Springfield",
        disciplinary_record="None"
    ),
    "S67890": Student(
        name="Bob Johnson",
        course="Mechanical Engineering",
        age=22,
        gpa=3.2,
        address="456 Oak St, Springfield",
        disciplinary_record="Late submission of project"
    ),
}

# ------------------------------------------------------------------
# Restricted attributes (sensitive data)
# ------------------------------------------------------------------
_RESTRICTED_ATTRS = {"gpa", "disciplinary_record"}

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def compile_student_profile(learner_code: str, profile_template: str) -> str:
    """
    Generates a student report by substituting placeholders in the template
    with actual data from the Student object identified by learner_code.

    Parameters:
        learner_code (str): Unique identifier for a student.
        profile_template (str): Template containing placeholders of the form
                                {student.attribute}.

    Returns:
        str: The formatted report string.

    Raises:
        ValueError: If the learner_code is invalid, or if the template
                    attempts to access restricted attributes.
    """
    # Validate learner_code and retrieve student
    student = _STUDENT_REGISTRY.get(learner_code)
    if not student:
        raise ValueError(f"Invalid learner code: {learner_code}")

    # Find all placeholders of the form {student.attr}
    placeholder_pattern = re.compile(r"\{student\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    placeholders = placeholder_pattern.findall(profile_template)

    # Check for restricted attributes
    for attr in set(placeholders):
        if attr.lower() in _RESTRICTED_ATTRS:
            raise ValueError(
                f"Access to restricted attribute '{attr}' is not allowed."
            )

    # Prepare a mapping for safe formatting
    student_attrs = {
        attr: getattr(student, attr)
        for attr in placeholders
    }

    # Perform substitution using str.format_map with a safe dictionary
    try:
        report = profile_template.format_map(student_attrs)
    except KeyError as e:
        # This should not happen due to earlier validation
        raise ValueError(f"Missing attribute in student data: {e}") from e

    return report


# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "Address: {student.address}"
    )
    print(compile_student_profile("S12345", template))