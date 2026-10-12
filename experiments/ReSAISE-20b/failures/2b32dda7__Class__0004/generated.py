# compile_performance_report.py

import re
from typing import Dict, Any


class Employee:
    """Mockup of the existing Employee class."""
    def __init__(self, emp_id: str, name: str, position: str, department: str):
        self.id = emp_id
        self.name = name
        self.position = position
        self.department = department


class Performance:
    """Mockup of the existing Performance class."""
    def __init__(self, rating: float, feedback: str, bonus: float):
        self.rating = rating
        self.feedback = feedback
        self.bonus = bonus


# --------------------------------------------------------------------------- #
# In‑memory data store (for illustration purposes only). In a real system
# this would be replaced with database look‑ups or API calls.
EMPLOYEE_DB: Dict[str, Employee] = {
    "E001": Employee("E001", "Alice Smith", "Software Engineer", "Engineering"),
    "E002": Employee("E002", "Bob Johnson", "Product Manager", "Product"),
}

PERFORMANCE_DB: Dict[str, Performance] = {
    "E001": Performance(4.5, "Excellent teamwork and delivery.", 1200.00),
    "E002": Performance(4.0, "Strong leadership in product road‑mapping.", 950.00),
}


# --------------------------------------------------------------------------- #
def _extract_placeholders(template: str) -> set:
    """
    Extract all field names from a format string.
    Uses the same logic as str.format_map but without actual formatting.
    """
    placeholder_pattern = r"\{([^\{\}]+)\}"
    matches = re.findall(placeholder_pattern, template)
    return set(matches)


def compile_performance_report(emp_id: str, report_template: str) -> str:
    """
    Compile a performance report for the given employee ID using the provided
    template string. The template may contain placeholders such as
    '{employee.name}', '{performance.rating}', etc.

    Args:
        emp_id: The unique identifier of the employee.
        report_template: A format string containing placeholders.

    Returns:
        The fully formatted performance report string.

    Raises:
        ValueError: If the employee ID does not exist, or if the template
                    attempts to access restricted fields like 'feedback' or
                    'bonus'.
    """
    # ----------------------------------------------------------------------- #
    # 1. Retrieve employee and performance data
    employee = EMPLOYEE_DB.get(emp_id)
    if not employee:
        raise ValueError(f"Employee ID '{emp_id}' does not exist.")

    performance = PERFORMANCE_DB.get(emp_id)
    if not performance:
        raise ValueError(f"No performance data found for employee ID '{emp_id}'.")

    # ----------------------------------------------------------------------- #
    # 2. Detect restricted fields in the template
    placeholders = _extract_placeholders(report_template)

    # The allowed namespaces are 'employee' and 'performance'.
    # Within each namespace, only specific attributes may be accessed.
    restricted_attrs = {"feedback", "bonus"}
    for placeholder in placeholders:
        # Split on the first dot to separate namespace and attribute
        if "." not in placeholder:
            raise ValueError(f"Invalid placeholder format: '{placeholder}'. "
                             "Expected 'namespace.attribute'.")
        namespace, attr = placeholder.split(".", 1)

        if namespace not in {"employee", "performance"}:
            raise ValueError(f"Unknown namespace '{namespace}' in placeholder "
                             f"'{placeholder}'. Allowed namespaces: 'employee', 'performance'.")

        if attr in restricted_attrs:
            raise ValueError(f"Access to restricted field '{attr}' is not allowed.")

    # ----------------------------------------------------------------------- #
    # 3. Perform safe formatting
    try:
        formatted_report = report_template.format(
            employee=employee,
            performance=performance
        )
    except KeyError as exc:
        raise ValueError(f"Missing attribute for placeholder: {exc}") from None
    except AttributeError as exc:
        raise ValueError(f"Invalid attribute accessed in template: {exc}") from None

    return formatted_report


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage
    template = (
        "Employee Summary for {employee.name} ({employee.position})\n"
        "Department: {employee.department}\n"
        "Performance Rating: {performance.rating}/5\n"
    )
    print(compile_performance_report("E001", template))