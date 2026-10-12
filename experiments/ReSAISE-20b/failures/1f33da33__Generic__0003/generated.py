import re
from typing import Any

# Assume these classes are defined elsewhere in the codebase.
# For demonstration purposes, minimal stubs are provided below.
class Employee:
    def __init__(self, emp_id: str, name: str, position: str, department: str):
        self.id = emp_id
        self.name = name
        self.position = position
        self.department = department

class Performance:
    def __init__(self, employee: Employee, rating: str, feedback: str, bonus: float):
        self.employee = employee
        self.rating = rating
        self.feedback = feedback
        self.bonus = bonus

# Mock data store (replace with actual database or service in production)
_EMPLOYEE_DB = {
    "E001": Employee("E001", "Alice Smith", "Senior Engineer", "R&D"),
    "E002": Employee("E002", "Bob Johnson", "Project Manager", "Operations"),
}

_PERFORMANCE_DB = {
    "E001": Performance(_EMPLOYEE_DB["E001"], "Exceeds Expectations", "Great leadership!", 12000.0),
    "E002": Performance(_EMPLOYEE_DB["E002"], "Meets Expectations", "Consistent performance.", 8000.0),
}

# Restricted fields that must not appear in the template
_RESTRICTED_FIELDS = {"feedback", "bonus"}

# Regex pattern to find placeholders like {employee.name} or {performance.rating}
_PLACEHOLDER_PATTERN = re.compile(r"\{(?P<object>\w+)\.(?P<attribute>\w+)\}")

def _get_employee_by_id(emp_id: str) -> Employee:
    """Retrieve an employee by ID from the data store."""
    employee = _EMPLOYEE_DB.get(emp_id)
    if not employee:
        raise ValueError(f"Employee ID '{emp_id}' does not exist.")
    return employee

def _get_performance_by_employee(emp: Employee) -> Performance:
    """Retrieve performance data for a given employee."""
    performance = _PERFORMANCE_DB.get(emp.id)
    if not performance:
        raise ValueError(f"Performance data for employee ID '{emp.id}' is missing.")
    return performance

def create_performance_summary(emp_id: str, summary_template: str) -> str:
    """
    Generate a performance summary string for the specified employee using the provided template.

    Parameters
    ----------
    emp_id : str
        The unique identifier of the employee.
    summary_template : str
        A string containing placeholders like `{employee.name}`, `{performance.rating}`.

    Returns
    -------
    str
        The formatted performance summary string.

    Raises
    ------
    ValueError
        If the employee ID is invalid or if restricted fields are referenced in the template.
    """
    # Validate employee existence
    employee = _get_employee_by_id(emp_id)
    performance = _get_performance_by_employee(employee)

    # Find all placeholders in the template
    matches = list(_PLACEHOLDER_PATTERN.finditer(summary_template))
    if not matches:
        # No placeholders, return the template as-is
        return summary_template

    # Prepare a mapping of placeholder to actual value
    replacement_map: dict[str, Any] = {}

    for match in matches:
        obj_name = match.group("object")
        attr_name = match.group("attribute")

        # Check for restricted fields
        if obj_name == "performance" and attr_name in _RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted field '{attr_name}' is not allowed in the template.")

        # Resolve attribute value
        if obj_name == "employee":
            value = getattr(employee, attr_name, None)
        elif obj_name == "performance":
            value = getattr(performance, attr_name, None)
        else:
            raise ValueError(f"Unknown placeholder object '{obj_name}' in template.")

        if value is None:
            raise ValueError(f"Attribute '{attr_name}' not found on object '{obj_name}'.")
        replacement_map[match.group(0)] = str(value)

    # Perform replacements
    result = summary_template
    for placeholder, value in replacement_map.items():
        result = result.replace(placeholder, value)

    return result

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    template = (
        "Employee: {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
        "Rating: {performance.rating}\n"
    )
    print(create_performance_summary("E001", template))