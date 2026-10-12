import re
from typing import Any

# Assume these classes are defined elsewhere in the codebase.
class Employee:
    def __init__(self, emp_id: str, name: str, position: str,
                 department: str, performance):
        self.id = emp_id
        self.name = name
        self.position = position
        self.department = department
        self.performance = performance

class Performance:
    def __init__(self, rating: str, feedback: str, bonus: float):
        self.rating = rating
        self.feedback = feedback
        self.bonus = bonus

# Dummy repository lookup function – replace with actual data access logic.
def get_employee(emp_id: str) -> Employee | None:
    """
    Retrieve an Employee instance by ID.
    In a real system this would query the database or other storage.
    """
    # Example stub data for demonstration purposes.
    if emp_id == "E123":
        perf = Performance(rating="Excellent", feedback="Great work!", bonus=5000.0)
        return Employee(emp_id, "Alice Smith", "Senior Engineer",
                        "R&D", perf)
    return None

def compile_performance_report(emp_id: str, report_template: str) -> str:
    """
    Compile a performance report for the specified employee using the given template.

    Parameters
    ----------
    emp_id : str
        The unique identifier of the employee.
    report_template : str
        A string containing placeholders like '{employee.name}' or
        '{performance.rating}'. Placeholders referencing restricted fields
        (e.g., feedback, bonus) or any other unknown field will raise a
        ValueError.

    Returns
    -------
    str
        The formatted performance report.

    Raises
    ------
    ValueError
        If the employee ID does not exist or if the template attempts to
        access restricted/unknown fields.
    """
    employee = get_employee(emp_id)
    if not employee:
        raise ValueError(f"Invalid employee ID: {emp_id}")

    # Define the set of allowed placeholders and their corresponding values.
    allowed_placeholders = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": getattr(employee.performance, "rating", None),
    }

    # Regular expression to find all placeholders of the form {some.key}
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")

    def replace_placeholder(match: re.Match) -> str:
        key = match.group(1).strip()
        if key not in allowed_placeholders:
            # Disallow any placeholder that is not explicitly permitted.
            raise ValueError(f"Restricted or unknown field in template: '{key}'")
        value = allowed_placeholders[key]
        if value is None:
            raise ValueError(f"Field '{key}' has no accessible value.")
        return str(value)

    try:
        formatted_report = placeholder_pattern.sub(replace_placeholder, report_template)
    except ValueError as ve:
        # Re-raise with a clear message.
        raise ValueError(f"Template processing error: {ve}") from None

    return formatted_report