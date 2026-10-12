import re
from dataclasses import dataclass

# ----------------------------------------------------------------------
# Minimal data model (for demonstration; replace with real implementations)
# ----------------------------------------------------------------------
@dataclass
class Employee:
    code: str
    name: str
    position: str
    department: str

@dataclass
class Performance:
    employee_code: str
    rating: float
    # Sensitive fields that must never be exposed via the template
    feedback: str
    bonus: float

# ----------------------------------------------------------------------
# In‑memory "database" (replace with real persistence in production)
# ----------------------------------------------------------------------
EMPLOYEES = {
    "E001": Employee(code="E001", name="Alice Smith", position="Engineer", department="R&D"),
    "E002": Employee(code="E002", name="Bob Johnson", position="Manager", department="Sales"),
}

PERFORMANCES = {
    "E001": Performance(employee_code="E001", rating=4.2, feedback="Excellent teamwork.", bonus=1200.00),
    "E002": Performance(employee_code="E002", rating=3.8, feedback="Needs improvement in forecasting.", bonus=800.00),
}

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
PLACEHOLDER_RE = re.compile(r"\{([^\}]+)\}")

ALLOWED_FIELDS = {
    "employee.name",
    "employee.position",
    "employee.department",
    "performance.rating",
}

RESTRICTED_FIELDS = {
    "performance.feedback",
    "performance.bonus",
}


def _lookup_value(path: str, employee: Employee, performance: Performance) -> str:
    """
    Resolve a dotted path like 'employee.name' to its value.
    Raises ValueError if the field is restricted or not found.
    """
    if path in RESTRICTED_FIELDS:
        raise ValueError(f"Access to restricted field '{path}' is not allowed.")

    if path == "employee.name":
        return employee.name
    elif path == "employee.position":
        return employee.position
    elif path == "employee.department":
        return employee.department
    elif path == "performance.rating":
        return str(performance.rating)
    else:
        raise ValueError(f"Unknown placeholder '{path}'.")


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_performance_report(emp_code: str, summary_template: str) -> str:
    """
    Generate a performance report for the given employee code using the provided
    template string. The template may contain placeholders such as:
        {employee.name}, {employee.position},
        {performance.rating}

    Restricted fields (feedback, bonus) cannot be accessed and will raise a
    ValueError if attempted.

    Parameters:
        emp_code (str): Identifier of the employee.
        summary_template (str): Template string with placeholders.

    Returns:
        str: The formatted performance report.

    Raises:
        ValueError: If the employee code is unknown, a placeholder refers to
                    restricted or non‑existent data.
    """
    # Retrieve employee and performance records
    employee = EMPLOYEES.get(emp_code)
    if not employee:
        raise ValueError(f"Employee code '{emp_code}' does not exist.")

    performance = PERFORMANCES.get(emp_code)
    if not performance:
        raise ValueError(f"No performance data for employee code '{emp_code}'.")

    # Find all placeholders in the template
    placeholders = PLACEHOLDER_RE.findall(summary_template)

    # Build a mapping for str.format()
    format_kwargs = {}
    for placeholder in placeholders:
        if placeholder not in ALLOWED_FIELDS:
            raise ValueError(f"Placeholder '{placeholder}' is not allowed or does not exist.")
        format_kwargs[placeholder] = _lookup_value(placeholder, employee, performance)

    try:
        report = summary_template.format(**format_kwargs)
    except KeyError as exc:
        # Should not happen because we validated placeholders
        raise ValueError(f"Missing data for placeholder {exc}") from exc

    return report


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     template = (
#         "Employee Report\n"
#         "Name: {employee.name}\n"
#         "Position: {employee.position}\n"
#         "Department: {employee.department}\n"
#         "Performance Rating: {performance.rating}"
#     )
#     print(create_performance_report("E001", template))