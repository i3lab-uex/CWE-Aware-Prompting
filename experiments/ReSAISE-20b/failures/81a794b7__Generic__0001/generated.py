import re
from typing import Dict

# Assume these classes are defined elsewhere in the codebase.
# They provide the necessary attributes and methods for employee lookup.

class Employee:
    """
    Represents an employee with basic personal details.
    """
    _registry: Dict[str, "Employee"] = {}

    def __init__(self, emp_id: str, name: str, position: str):
        self.id = emp_id
        self.name = name
        self.position = position
        Employee._registry[emp_id] = self

    @classmethod
    def get_by_id(cls, emp_id: str) -> "Employee":
        return cls._registry.get(emp_id)

class Performance:
    """
    Represents a performance review for an employee.
    """
    _registry: Dict[str, "Performance"] = {}

    def __init__(self, emp_id: str, rating: float):
        self.emp_id = emp_id
        self.rating = rating
        Performance._registry[emp_id] = self

    @classmethod
    def get_by_employee(cls, employee: Employee) -> "Performance":
        return cls._registry.get(employee.id)


# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def compile_employee_evaluation(employee_id: str, template: str) -> str:
    """
    Generate a formatted employee evaluation string based on the provided template.

    Parameters
    ----------
    employee_id : str
        The unique identifier for the employee.
    template : str
        A string containing placeholders to be replaced with actual data.

    Returns
    -------
    str
        The formatted evaluation string.

    Raises
    ------
    ValueError
        If the employee ID is invalid, or if the template attempts to access
        unauthorized data such as 'feedback' or 'bonus'.
    """
    # --- Retrieve employee and performance objects ---------------------------------
    employee = Employee.get_by_id(employee_id)
    if not employee:
        raise ValueError(f"Employee ID '{employee_id}' is invalid.")

    performance = Performance.get_by_employee(employee)
    if not performance:
        raise ValueError(f"No performance record found for employee ID '{employee_id}'.")

    # --- Define allowed placeholder mapping ----------------------------------------
    placeholder_map = {
        "personnel.name": employee.name,
        "personnel.position": employee.position,
        "review.rating": f"{performance.rating:.1f}",
    }

    # --- Identify placeholders in the template ------------------------------------
    placeholder_pattern = re.compile(r"\{([^\}]+)\}")
    placeholders_in_template = set(placeholder_pattern.findall(template))

    # --- Check for unauthorized placeholders ---------------------------------------
    unauthorized_fields = {"feedback", "bonus"}
    if any(field in placeholder for field in unauthorized_fields
           for placeholder in placeholders_in_template):
        raise ValueError("Template contains unauthorized fields (e.g., 'feedback', 'bonus').")

    # --- Replace placeholders safely ---------------------------------------------
    def replacement(match: re.Match) -> str:
        key = match.group(1)
        if key not in placeholder_map:
            # If an unknown placeholder is encountered, leave it unchanged
            return match.group(0)
        return placeholder_map[key]

    formatted = placeholder_pattern.sub(replacement, template)

    return formatted


# --------------------------------------------------------------------------- #
# Example usage (for illustration; remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Sample data
    emp = Employee("E001", "Alice Smith", "Software Engineer")
    perf = Performance("E001", 4.2)

    tmpl = ("Employee Report:\n"
            "Name: {personnel.name}\n"
            "Position: {personnel.position}\n"
            "Rating: {review.rating}")

    print(compile_employee_evaluation("E001", tmpl))