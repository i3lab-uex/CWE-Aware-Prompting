import re
from typing import Dict

# ------------------------------------------------------------------
# Mock data structures (in the real system these would be replaced by
# actual ORM models or database access layers).
# ------------------------------------------------------------------
class Employee:
    def __init__(self, emp_id: str, name: str, position: str,
                 department: str):
        self.emp_id = emp_id
        self.name = name
        self.position = position
        self.department = department

class Performance:
    def __init__(self, emp_id: str, rating: float,
                 feedback: str, bonus: float):
        self.emp_id = emp_id
        self.rating = rating
        self.feedback = feedback
        self.bonus = bonus

# In-memory "database" of employees and their performance data.
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee("E001", "Alice Smith", "Senior Engineer",
                     "Research & Development"),
    "E002": Employee("E002", "Bob Johnson", "Product Manager",
                     "Marketing"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance("E001", 4.7,
                        "Excellent problem solving and teamwork.",
                        12000.0),
    "E002": Performance("E002", 3.9,
                        "Strong leadership but needs to improve on time‑management.",
                        8000.0),
}

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------
def _get_employee_and_performance(emp_id: str):
    """Retrieve employee and performance objects for a given ID."""
    emp = EMPLOYEES.get(emp_id)
    perf = PERFORMANCES.get(emp_id)
    if not emp or not perf:
        raise ValueError(f"Employee ID '{emp_id}' does not exist.")
    return emp, perf


def _sanitize_template(template: str):
    """Ensure that restricted fields are not accessed."""
    # Disallowed placeholders (case‑insensitive)
    disallowed = {"feedback", "bonus"}
    # Find all placeholders of the form {something}
    placeholders = re.findall(r"\{([^{}]+)\}", template)
    for ph in placeholders:
        # Normalize to lower case and split on dots
        parts = ph.lower().split(".")
        if any(part in disallowed for part in parts):
            raise ValueError(
                f"Access to restricted field '{ph}' is not allowed."
            )


def _build_context(emp: Employee, perf: Performance) -> Dict[str, object]:
    """Build a flat context dictionary for formatting."""
    return {
        "employee.name": emp.name,
        "employee.position": emp.position,
        "employee.department": emp.department,
        "performance.rating": perf.rating,
    }


def _safe_format(template: str, context: Dict[str, object]) -> str:
    """
    Perform a safe string formatting operation.
    Only placeholders that exist in the context are replaced; unknown
    placeholders raise a KeyError.
    """
    class SafeDict(dict):
        def __missing__(self, key):
            raise KeyError(f"Unknown placeholder '{key}' in template.")

    return template.format_map(SafeDict(context))


# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def compile_performance_report(emp_id: str, report_template: str) -> str:
    """
    Generate a performance summary for the given employee ID using
    the provided template string.

    Parameters
    ----------
    emp_id : str
        Unique identifier of the employee.
    report_template : str
        Template containing placeholders such as '{employee.name}',
        '{performance.rating}', etc.

    Returns
    -------
    str
        The formatted performance summary.

    Raises
    ------
    ValueError
        If the employee ID is invalid, or if the template attempts to
        access restricted fields (feedback or bonus).
    KeyError
        If the template contains placeholders that are not present in
        the context.
    """
    # 1. Validate and retrieve data
    emp, perf = _get_employee_and_performance(emp_id)

    # 2. Sanitize template for disallowed fields
    _sanitize_template(report_template)

    # 3. Build context and format safely
    context = _build_context(emp, perf)
    return _safe_format(report_template, context)


# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Employee: {employee.name}\n"
        "Position: {employee.position} in {employee.department}\n"
        "Performance Rating: {performance.rating}"
    )
    print(compile_performance_report("E001", template))