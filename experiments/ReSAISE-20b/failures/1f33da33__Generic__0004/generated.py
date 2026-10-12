import re
from typing import Any

# Assume these classes are defined elsewhere in the system.
# The following stubs are provided only for type checking and to make this module runnable in isolation.
class Employee:
    def __init__(self, emp_id: str, name: str, position: str, department: str,
                 performance_rating: float, feedback: str, bonus: float):
        self.emp_id = emp_id
        self.name = name
        self.position = position
        self.department = department
        # Performance attributes are exposed via a nested object for clarity.
        self.performance = Performance(performance_rating, feedback, bonus)

class Performance:
    def __init__(self, rating: float, feedback: str, bonus: float):
        self.rating = rating
        self.feedback = feedback
        self.bonus = bonus

# In a real system this would query a database or other persistence layer.
EMPLOYEE_DB = {
    "E001": Employee("E001", "Alice Smith", "Software Engineer",
                     "Engineering", 4.5, "Excellent work on the project.", 1200.0),
    "E002": Employee("E002", "Bob Johnson", "Product Manager",
                     "Product", 4.0, "Good leadership.", 800.0),
}

# ---------------------------------------------------------------------------

def create_performance_summary(emp_id: str, summary_template: str) -> str:
    """
    Generate a performance summary for the specified employee using the supplied template.

    Parameters
    ----------
    emp_id : str
        The unique identifier of the employee.
    summary_template : str
        A string containing placeholders like `{employee.name}` or `{performance.rating}`.

    Returns
    -------
    str
        The formatted performance summary with placeholders replaced by actual values.

    Raises
    ------
    ValueError
        If the employee ID does not exist or if the template tries to access restricted fields
        such as `feedback` or `bonus`.
    """
    # -----------------------------------------------------------------------
    # 1. Validate employee ID and fetch the employee object.
    # -----------------------------------------------------------------------
    employee = EMPLOYEE_DB.get(emp_id)
    if not employee:
        raise ValueError(f"Employee ID '{emp_id}' does not exist.")

    # -----------------------------------------------------------------------
    # 2. Find all placeholders in the template.
    # -----------------------------------------------------------------------
    placeholder_pattern = re.compile(r"\{([^\}]+)\}")
    placeholders = placeholder_pattern.findall(summary_template)

    # -----------------------------------------------------------------------
    # 3. Resolve each placeholder to its value.
    # -----------------------------------------------------------------------
    resolved_values: dict[str, Any] = {}
    for placeholder in placeholders:
        # Split on the first dot to determine the root object (employee or performance).
        try:
            root, attr_path = placeholder.split(".", 1)
        except ValueError:
            raise ValueError(f"Invalid placeholder format: '{{{placeholder}}}'")

        # Reject any attempt to access restricted fields.
        if root == "performance" and attr_path.split(".")[0] in {"feedback", "bonus"}:
            raise ValueError(f"Access to restricted field '{attr_path}' is not allowed.")

        # Resolve the value from the appropriate object.
        if root == "employee":
            obj = employee
        elif root == "performance":
            obj = employee.performance
        else:
            raise ValueError(f"Unknown placeholder root '{root}' in '{{{placeholder}}}'")

        # Traverse nested attributes if any.
        try:
            value = obj
            for part in attr_path.split("."):
                value = getattr(value, part)
        except AttributeError as exc:
            raise ValueError(f"Attribute '{attr_path}' not found for employee '{emp_id}'.") from exc

        resolved_values[placeholder] = str(value)

    # -----------------------------------------------------------------------
    # 4. Perform the substitution.
    # -----------------------------------------------------------------------
    def replacement(match: re.Match) -> str:
        key = match.group(1)
        return resolved_values.get(key, match.group(0))

    summary = placeholder_pattern.sub(replacement, summary_template)
    return summary

# ---------------------------------------------------------------------------
# Example usage (uncomment to test):
#
# print(create_performance_summary(
#     "E001",
#     "Employee {employee.name} ({employee.position}) in {employee.department} scored "
#     "{performance.rating}/5.0 in the recent review."
# ))
#