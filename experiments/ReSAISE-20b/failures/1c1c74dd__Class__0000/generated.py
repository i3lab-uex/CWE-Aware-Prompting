import re
from dataclasses import dataclass, fields

# ----------------------------------------------------------------------
# Data model (simplified for this example)
# ----------------------------------------------------------------------
@dataclass
class Student:
    name: str
    course: str
    age: int
    GPA: float          # sensitive
    home_address: str   # sensitive
    discipline_record: str


# ----------------------------------------------------------------------
# Mock database of students
# ----------------------------------------------------------------------
_STUDENT_DB = {
    "S001": Student(
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission"
    ),
    # Add more students as needed
}


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _parse_format_fields(template: str):
    """
    Parse a format string and return a set of all field names used.
    Supports nested fields like {student.name}.
    """
    pattern = r"\{([^\{\}]+)\}"
    return set(re.findall(pattern, template))


def _validate_template(template: str):
    """
    Raise ValueError if the template attempts to access sensitive attributes.
    Sensitive attributes are 'GPA' and 'home_address'.
    """
    fields_in_template = _parse_format_fields(template)
    sensitive_attrs = {"GPA", "home_address"}
    for field in fields_in_template:
        # Only check if the field refers to a student attribute directly
        # e.g., {student.GPA}
        if field.startswith("student."):
            attr = field.split(".", 1)[1]
            if attr in sensitive_attrs:
                raise ValueError(f"Access to sensitive attribute '{attr}' is prohibited.")
    # If the template uses a different placeholder structure, it will be ignored
    return True


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def produce_student_report(stu_id: str, custom_template: str) -> str:
    """
    Generate a formatted student report based on the provided template.

    Parameters
    ----------
    stu_id : str
        Unique identifier of the student.
    custom_template : str
        Format string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student ID does not exist or if the template attempts to access
        sensitive attributes such as GPA or home address.
    """
    # Validate existence of the student
    if stu_id not in _STUDENT_DB:
        raise ValueError(f"Student ID '{stu_id}' does not exist.")

    # Validate template for sensitive data exposure
    _validate_template(custom_template)

    student = _STUDENT_DB[stu_id]

    # Prepare a safe namespace for formatting
    report = custom_template.format(student=student)
    return report


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = "Student Report:\nName: {student.name}\nCourse: {student.course}\nAge: {student.age}"
    print(produce_student_report("S001", tmpl))