import re
from string import Formatter

# ------------------------------------------------------------------
# Example Student class (for context).  In a real system this would
# be part of the application’s data model.
# ------------------------------------------------------------------
class Student:
    """
    Represents a student record.  Only the attributes listed below are
    considered safe for public reporting.
    """
    __slots__ = (
        "learner_code",
        "name",
        "course",
        "age",
        "gpa",
        # Sensitive attributes (should not be exposed)
        "_home_address",
        "_disciplinary_record",
    )

    def __init__(self, learner_code: str, name: str, course: str,
                 age: int, gpa: float,
                 home_address: str = "", disciplinary_record: str = ""):
        self.learner_code = learner_code
        self.name = name
        self.course = course
        self.age = age
        self.gpa = gpa
        self._home_address = home_address
        self._disciplinary_record = disciplinary_record

    def __repr__(self):
        return f"<Student {self.learner_code}: {self.name}>"


# ------------------------------------------------------------------
# In-memory student store (for demonstration).  Replace with real DB
# access in production.
# ------------------------------------------------------------------
_STUDENT_DB = {
    "A001": Student("A001", "Alice Smith", "Computer Science", 20, 3.8,
                    home_address="123 Maple St.", disciplinary_record="None"),
    "B002": Student("B002", "Bob Jones", "Mathematics", 22, 3.5,
                    home_address="456 Oak Ave.", disciplinary_record="Late submission"),
}


# ------------------------------------------------------------------
# Compile student profile
# ------------------------------------------------------------------
def compile_student_profile(learner_code: str, profile_template: str) -> str:
    """
    Generate a student report from the given template.

    Parameters
    ----------
    learner_code : str
        Unique identifier for the student.
    profile_template : str
        Template string containing placeholders like `{student.name}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the learner_code is unknown, or if a template references
        restricted/sensitive attributes.
    """
    # Fetch student record
    student = _STUDENT_DB.get(learner_code)
    if not student:
        raise ValueError(f"Unknown learner code: {learner_code}")

    # Define which attributes are safe to expose
    allowed_attrs = {
        "name": student.name,
        "course": student.course,
        "age": student.age,
        "gpa": student.gpa,
    }

    # Parse template to find all field names
    formatter = Formatter()
    for literal_text, field_name, format_spec, conversion in formatter.parse(profile_template):
        if not field_name:
            continue  # skip literal text

        # The template uses the syntax {student.<field>}
        if field_name.startswith("student."):
            attr = field_name.split(".", 1)[1]
        else:
            # Unsupported placeholder format
            raise ValueError(f"Unsupported placeholder: {field_name}")

        if attr not in allowed_attrs:
            raise ValueError(f"Attempted to access restricted attribute '{attr}'")

    # Build a mapping for format_map
    report_data = {"student": allowed_attrs}

    try:
        return profile_template.format(**report_data)
    except KeyError as exc:
        # This should not happen because we validated placeholders
        raise ValueError(f"Missing placeholder data: {exc}") from exc


# ------------------------------------------------------------------
# Example usage (commented out)
# ------------------------------------------------------------------
# if __name__ == "__main__":
#     tmpl = (
#         "Student Report:\n"
#         "Name: {student.name}\n"
#         "Course: {student.course}\n"
#         "Age: {student.age}\n"
#         "GPA: {student.gpa}"
#     )
#     print(compile_student_profile("A001", tmpl))