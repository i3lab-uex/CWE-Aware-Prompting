import re
from typing import Any

# ----------------------------------------------------------------------
# Assume these classes are defined elsewhere in the system.
# They provide a simple interface to retrieve employee and performance data.
# ----------------------------------------------------------------------
class Employee:
    """
    Mock implementation for demonstration purposes.
    In production, this would interface with a database or other data store.
    """
    _employees = {
        "E001": {"name": "Alice Smith", "position": "Senior Engineer",
                 "department": "R&D"},
        "E002": {"name": "Bob Johnson", "position": "Project Manager",
                 "department": "Operations"},
    }

    def __init__(self, employee_id: str, data: dict):
        self.employee_id = employee_id
        for key, value in data.items():
            setattr(self, key, value)

    @classmethod
    def get_by_id(cls, employee_id: str) -> "Employee":
        data = cls._employees.get(employee_id)
        if not data:
            raise ValueError(f"Employee ID '{employee_id}' does not exist.")
        return cls(employee_id, data)


class Performance:
    """
    Mock implementation for demonstration purposes.
    In production, this would interface with a database or other data store.
    """
    _performances = {
        "E001": {"rating": 4.7, "feedback": "Excellent teamwork",
                 "bonus": 1500},
        "E002": {"rating": 3.9, "feedback": "Good leadership",
                 "bonus": 1200},
    }

    def __init__(self, employee_id: str, data: dict):
        self.employee_id = employee_id
        for key, value in data.items():
            setattr(self, key, value)

    @classmethod
    def get_for_employee(cls, employee_id: str) -> "Performance":
        data = cls._performances.get(employee_id)
        if not data:
            raise ValueError(f"No performance record for employee ID '{employee_id}'.")
        return cls(employee_id, data)


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def construct_employee_report(employee_id: str, report_template: str) -> str:
    """
    Construct a performance summary for the given employee using a template.

    Parameters
    ----------
    employee_id : str
        The unique identifier of the employee.
    report_template : str
        A template string containing placeholders such as '{employee.name}' or
        '{performance.rating}'.  The function will replace these with the actual
        values from the employee's data.

    Returns
    -------
    str
        The formatted performance report.

    Raises
    ------
    ValueError
        If the employee ID is invalid or if the template tries to access
        restricted fields (e.g., 'feedback' or 'bonus').
    """
    # Retrieve data objects
    employee = Employee.get_by_id(employee_id)
    performance = Performance.get_for_employee(employee_id)

    # Define restricted fields that must not be exposed
    RESTRICTED = {"feedback", "bonus"}

    # Regular expression to find placeholders like {employee.name}
    placeholder_pattern = re.compile(r"\{([^\}]+)\}")

    def resolve_placeholder(match: re.Match) -> str:
        path = match.group(1).strip()
        parts = path.split(".")
        if not parts:
            raise ValueError(f"Invalid placeholder syntax: '{match.group(0)}'")

        # Resolve the root object
        obj_name = parts[0]
        if obj_name == "employee":
            current_obj: Any = employee
        elif obj_name == "performance":
            current_obj = performance
        else:
            raise ValueError(f"Unknown root object '{obj_name}' in placeholder '{match.group(0)}'")

        # Resolve subsequent attributes
        for attr in parts[1:]:
            if attr in RESTRICTED:
                raise ValueError(f"Access to restricted field '{attr}' is not allowed.")
            if not hasattr(current_obj, attr):
                raise ValueError(f"Attribute '{attr}' not found on object '{obj_name}'.")
            current_obj = getattr(current_obj, attr)

        # Convert the final value to string for formatting
        return str(current_obj)

    try:
        formatted_report = placeholder_pattern.sub(resolve_placeholder, report_template)
    except ValueError as exc:
        # Re‑raise with context
        raise ValueError(f"Failed to construct report: {exc}") from None

    return formatted_report