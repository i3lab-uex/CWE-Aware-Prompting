import re
from typing import Any

# Assume these classes are defined elsewhere in the codebase.
class Employee:
    def __init__(self, id: str, name: str, position: str, department: str):
        self.id = id
        self.name = name
        self.position = position
        self.department = department
        # Sensitive attributes (should not be exposed)
        self.feedback = "Some confidential feedback"
        self.bonus = 5000

class Performance:
    def __init__(self, employee_id: str, rating: float):
        self.employee_id = employee_id
        self.rating = rating

# Dummy data store for demonstration purposes.
EMPLOYEES_DB = {
    "E001": Employee("E001", "Alice Smith", "Software Engineer", "Engineering"),
    "E002": Employee("E002", "Bob Johnson", "Product Manager", "Product"),
}
PERFORMANCES_DB = {
    "E001": Performance("E001", 4.5),
    "E002": Performance("E002", 3.8),
}

def get_employee(employee_id: str) -> Employee | None:
    return EMPLOYEES_DB.get(employee_id)

def get_performance(employee_id: str) -> Performance | None:
    return PERFORMANCES_DB.get(employee_id)

def build_employee_report(employee_id: str, template: str) -> str:
    """
    Build a performance report for an employee by substituting placeholders in
    the template with actual data. Sensitive information (feedback, bonus)
    is not allowed to be exposed.

    Raises:
        ValueError: If the employee ID does not exist, or if a placeholder
                    refers to unauthorized data.
    """
    # Retrieve employee and performance objects.
    employee = get_employee(employee_id)
    if not employee:
        raise ValueError(f"Invalid employee ID: {employee_id}")

    performance = get_performance(employee_id)
    if not performance:
        raise ValueError(f"No performance data for employee ID: {employee_id}")

    # Whitelist of safe attributes.
    SAFE_EMPLOYEE_ATTRS = {"name", "position", "department"}
    SAFE_PERFORMANCE_ATTRS = {"rating"}

    # Regex to find placeholders like {staff.name} or {evaluation.rating}
    placeholder_pattern = re.compile(r"{\s*(?P<scope>staff|evaluation)\.(?P<attr>\w+)\s*}")

    def replace_match(match: re.Match) -> str:
        scope = match.group("scope")
        attr = match.group("attr")

        if scope == "staff":
            if attr not in SAFE_EMPLOYEE_ATTRS:
                raise ValueError(f"Unauthorized access to employee attribute '{attr}'")
            return str(getattr(employee, attr))
        elif scope == "evaluation":
            if attr not in SAFE_PERFORMANCE_ATTRS:
                raise ValueError(f"Unauthorized access to performance attribute '{attr}'")
            return str(getattr(performance, attr))
        else:
            # Should not happen due to regex but guard anyway.
            raise ValueError(f"Unknown placeholder scope '{scope}'")

    # Perform substitution safely
    try:
        result = placeholder_pattern.sub(replace_match, template)
    except ValueError as e:
        # Re-raise with context
        raise ValueError(f"Failed to build report: {e}") from None

    return result

# Example usage (for testing purposes only)
if __name__ == "__main__":
    tmpl = (
        "Employee Report:\n"
        "- Name: {staff.name}\n"
        "- Position: {staff.position}\n"
        "- Department: {staff.department}\n"
        "- Rating: {evaluation.rating}\n"
    )
    print(build_employee_report("E001", tmpl))