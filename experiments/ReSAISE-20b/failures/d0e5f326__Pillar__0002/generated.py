import re
from typing import Dict

# ------------------------------------------------------------------
# Mock data structures (in real use these would be imported)
# ------------------------------------------------------------------

class Employee:
    """Represents an employee record."""
    def __init__(self, emp_id: str, name: str, position: str, department: str):
        self.id = emp_id
        self.name = name
        self.position = position
        self.department = department


class Performance:
    """Represents a performance evaluation."""
    def __init__(self, emp_id: str, rating: float, feedback: str, bonus: float):
        self.id = emp_id
        self.rating = rating
        self.feedback = feedback
        self.bonus = bonus


# ------------------------------------------------------------------
# Sample in‑memory data store (replace with real persistence)
# ------------------------------------------------------------------

EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee("E001", "Alice Smith", "Senior Engineer", "R&D"),
    "E002": Employee("E002", "Bob Johnson", "Product Manager", "Marketing"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance("E001", 4.5, "Excellent leadership.", 5000),
    "E002": Performance("E002", 4.2, "Strong project delivery.", 4000),
}


# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------

def _extract_placeholders(template: str) -> set:
    """
    Return a set of placeholder names found in the template.
    Placeholders are expected to be in the form {object.attribute}.
    """
    pattern = r"{\s*([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}"
    return {f"{obj}.{attr}" for obj, attr in re.findall(pattern, template)}


def _build_context(employee: Employee, performance: Performance) -> dict:
    """
    Build a dictionary suitable for str.format() that contains only
    authorized fields. Raises ValueError if unauthorized data is requested.
    """
    allowed = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating,
    }

    # Identify any placeholder that is not in the allowed set
    placeholders = _extract_placeholders(template)
    unauthorized = placeholders - set(allowed.keys())
    if unauthorized:
        raise ValueError(f"Unauthorized placeholder(s) accessed: {', '.join(sorted(unauthorized))}")

    return allowed


# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------

def build_employee_report(employee_id: str, template: str) -> str:
    """
    Generate a performance report for the given employee ID using the provided template.

    Parameters
    ----------
    employee_id : str
        Unique identifier for an employee.
    template : str
        Template string containing placeholders such as '{employee.name}' or
        '{performance.rating}'. Placeholders for sensitive data like feedback
        or bonus are not permitted.

    Returns
    -------
    str
        The formatted performance report.

    Raises
    ------
    ValueError
        If the employee ID is invalid or if the template attempts to access
        unauthorized information.
    """
    # Validate employee existence
    employee = EMPLOYEES.get(employee_id)
    if not employee:
        raise ValueError(f"Employee ID '{employee_id}' is invalid.")

    performance = PERFORMANCES.get(employee_id)
    if not performance:
        raise ValueError(f"No performance record found for employee ID '{employee_id}'.")

    # Build context dictionary
    allowed_placeholders = _extract_placeholders(template)
    unauthorized = {
        ph for ph in allowed_placeholders
        if ph not in {"employee.name", "employee.position", "employee.department",
                      "performance.rating"}
    }
    if unauthorized:
        raise ValueError(f"Unauthorized placeholder(s) accessed: {', '.join(sorted(unauthorized))}")

    context = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating,
    }

    # Perform formatting
    try:
        report = template.format(**context)
    except KeyError as exc:
        # This should not happen due to the earlier check, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return report


# ------------------------------------------------------------------
# Example usage (commented out)
# ------------------------------------------------------------------

# if __name__ == "__main__":
#     tmpl = ("Employee: {employee.name}\n"
#             "Position: {employee.position}\n"
#             "Department: {employee.department}\n"
#             "Rating: {performance.rating}")
#
#     print(build_employee_report("E001", tmpl))