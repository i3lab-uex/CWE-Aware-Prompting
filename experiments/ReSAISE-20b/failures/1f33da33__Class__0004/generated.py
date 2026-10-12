import re
from typing import Any

# ----------------------------------------------------------------------
# Mocked data structures – in a real system these would be imported
# from the company's ORM or database layer.
# ----------------------------------------------------------------------
class Employee:
    _employees = {
        "E001": {"name": "Alice Smith", "position": "Senior Engineer",
                 "department": "R&D"},
        "E002": {"name": "Bob Jones", "position": "Project Manager",
                 "department": "Operations"},
    }

    def __init__(self, emp_id: str, data: dict):
        self.emp_id = emp_id
        for k, v in data.items():
            setattr(self, k, v)

    @classmethod
    def get_by_id(cls, emp_id: str) -> "Employee":
        data = cls._employees.get(emp_id)
        if not data:
            raise ValueError(f"Employee ID '{emp_id}' does not exist.")
        return cls(emp_id, data)


class Performance:
    _performances = {
        "E001": {"rating": 4.5, "feedback": "Excellent teamwork.",
                 "bonus": 1200},
        "E002": {"rating": 3.8, "feedback": "Good leadership.",
                 "bonus": 800},
    }

    def __init__(self, emp_id: str, data: dict):
        self.emp_id = emp_id
        for k, v in data.items():
            setattr(self, k, v)

    @classmethod
    def get_by_employee(cls, emp_id: str) -> "Performance":
        data = cls._performances.get(emp_id)
        if not data:
            raise ValueError(f"Performance record for employee ID '{emp_id}' missing.")
        return cls(emp_id, data)


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_performance_summary(emp_id: str, summary_template: str) -> str:
    """
    Generate a performance summary for the given employee.

    Parameters
    ----------
    emp_id : str
        The unique identifier of the employee.
    summary_template : str
        Template string containing placeholders such as
        '{employee.name}', '{performance.rating}'.

    Returns
    -------
    str
        The formatted summary string.

    Raises
    ------
    ValueError
        If the employee ID is invalid or if the template attempts to
        access restricted fields (feedback, bonus).
    """
    # Retrieve data objects
    employee = Employee.get_by_id(emp_id)
    performance = Performance.get_by_employee(emp_id)

    # Prepare a mapping from placeholder to value
    def resolve_placeholder(match: re.Match) -> str:
        key = match.group(1).strip()
        # Security check: disallow sensitive fields
        if key.startswith("performance.") and key.split(".", 1)[1] in ("feedback", "bonus"):
            raise ValueError(f"Access to restricted field '{key}' is not allowed.")
        # Resolve namespace
        if key.startswith("employee."):
            attr = key.split(".", 1)[1]
            try:
                return str(getattr(employee, attr))
            except AttributeError:
                raise ValueError(f"Employee has no attribute '{attr}'.")
        elif key.startswith("performance."):
            attr = key.split(".", 1)[1]
            try:
                return str(getattr(performance, attr))
            except AttributeError:
                raise ValueError(f"Performance has no attribute '{attr}'.")
        else:
            raise ValueError(f"Unknown placeholder namespace in '{key}'.")

    # Replace placeholders safely
    pattern = re.compile(r"\{([^}]+)\}")
    try:
        result = pattern.sub(resolve_placeholder, summary_template)
    except ValueError as e:
        # Re-raise to propagate error
        raise

    return result


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     tmpl = ("Employee {employee.name} ({employee.position}) in "
#             "{employee.department} received a rating of "
#             "{performance.rating}.")
#     print(create_performance_summary("E001", tmpl))