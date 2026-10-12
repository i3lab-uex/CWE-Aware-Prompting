import re
from typing import Dict

# Assume these classes are defined elsewhere in the codebase.
# from employee_module import Employee, Performance

# For demonstration purposes we provide minimal stubs.
class Employee:
    def __init__(self, name: str, position: str, department: str):
        self.name = name
        self.position = position
        self.department = department

class Performance:
    def __init__(self, rating: str):
        self.rating = rating


def build_employee_summary(emp_key: str, template_str: str) -> str:
    """
    Build a formatted employee performance summary.

    Parameters
    ----------
    emp_key : str
        Identifier of the employee.  In a real system this would be used to look up
        the Employee and Performance objects from a database.  For the purposes of
        this exercise we simply create dummy objects.
    template_str : str
        A string containing placeholders such as `{employee.name}`, `{performance.rating}`.

    Returns
    -------
    str
        The template string with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If a placeholder refers to an invalid attribute or a restricted field such as
        `feedback` or `bonus`.
    """
    # ------------------------------------------------------------------
    # 1. Retrieve the objects that provide data for formatting.
    # ------------------------------------------------------------------
    # In a real implementation these would be looked up from persistence
    # storage.  Here we create dummy data to illustrate the logic.
    employee = Employee(name="John Doe", position="Software Engineer", department="R&D")
    performance = Performance(rating="Excellent")

    # ------------------------------------------------------------------
    # 2. Build a mapping of allowable attributes.
    # ------------------------------------------------------------------
    allowed_mapping: Dict[str, any] = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating,
    }

    # Restricted fields that should never be exposed via formatting.
    restricted_fields = {"employee.feedback", "performance.bonus"}

    # ------------------------------------------------------------------
    # 3. Find all placeholders in the template.
    # ------------------------------------------------------------------
    placeholder_pattern = re.compile(r"{([^{}]+)}")
    placeholders = placeholder_pattern.findall(template_str)

    # ------------------------------------------------------------------
    # 4. Validate each placeholder and build a replacement dictionary.
    # ------------------------------------------------------------------
    replacements: Dict[str, str] = {}
    for key in placeholders:
        if key in restricted_fields:
            raise ValueError(f"Access to restricted field '{key}' is not allowed.")
        if key not in allowed_mapping:
            raise ValueError(f"Unknown placeholder '{key}'.")
        # Convert value to string for safe formatting
        replacements[key] = str(allowed_mapping[key])

    # ------------------------------------------------------------------
    # 5. Perform the substitution in a safe way.
    # ------------------------------------------------------------------
    def _replacement(match: re.Match) -> str:
        key = match.group(1)
        return replacements[key]

    result = placeholder_pattern.sub(_replacement, template_str)

    # ------------------------------------------------------------------
    # 6. Return the final formatted string.
    # ------------------------------------------------------------------
    return result