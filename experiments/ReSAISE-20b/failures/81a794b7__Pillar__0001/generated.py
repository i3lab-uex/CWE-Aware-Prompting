import re
from typing import Dict

# --------------------------------------------------------------------------- #
# Mock data structures (would normally be provided by the system)
# --------------------------------------------------------------------------- #

class Performance:
    """Represents performance data for an employee."""
    def __init__(self, rating: str, feedback: str, bonus: float):
        self.rating = rating          # e.g., "Excellent"
        self.feedback = feedback      # Sensitive
        self.bonus = bonus            # Sensitive


class Employee:
    """Represents an employee."""
    def __init__(self, emp_id: str, name: str, position: str,
                 department: str, performance: Performance):
        self.emp_id = emp_id
        self.name = name
        self.position = position
        self.department = department
        self.performance = performance


# --------------------------------------------------------------------------- #
# In‑memory “database” of employees (for demo purposes)
# --------------------------------------------------------------------------- #

EMPLOYEE_DB: Dict[str, Employee] = {
    "E001": Employee(
        emp_id="E001",
        name="Alice Johnson",
        position="Senior Analyst",
        department="Finance",
        performance=Performance(
            rating="Outstanding",
            feedback="Consistently exceeds expectations.",
            bonus=5000.00
        ),
    ),
    "E002": Employee(
        emp_id="E002",
        name="Bob Smith",
        position="Junior Developer",
        department="IT",
        performance=Performance(
            rating="Satisfactory",
            feedback="Meets project deadlines.",
            bonus=1200.00
        ),
    ),
}


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

PLACEHOLDER_PATTERN = re.compile(r"\{([a-zA-Z0-9_.]+)\}")


def _fetch_employee(emp_id: str) -> Employee:
    """
    Retrieve an employee from the database.
    Raises ValueError if the ID is unknown.
    """
    try:
        return EMPLOYEE_DB[emp_id]
    except KeyError as exc:
        raise ValueError(f"Employee ID '{emp_id}' is invalid.") from exc


def _build_context(employee: Employee) -> Dict[str, str]:
    """
    Construct a mapping from placeholder keys to their string values.
    Raises ValueError if an unauthorized field is requested.
    """
    context: Dict[str, str] = {
        "personnel.name": employee.name,
        "personnel.position": employee.position,
        "personnel.department": employee.department,
        "review.rating": employee.performance.rating,
    }
    return context


def _replace_placeholders(template: str, context: Dict[str, str]) -> str:
    """
    Replace placeholders in the template using the provided context.
    Raises ValueError if a placeholder references an unauthorized field
    or is not present in the context.
    """
    def repl(match: re.Match) -> str:
        key = match.group(1)
        if key not in context:
            # Detect unauthorized placeholders
            if key.startswith("performance.") or key == "review.feedback" or key == "review.bonus":
                raise ValueError(f"Unauthorized access to '{key}'.")
            raise ValueError(f"Placeholder '{key}' not found in context.")
        return context[key]

    return PLACEHOLDER_PATTERN.sub(repl, template)


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def compile_employee_evaluation(employee_id: str, template: str) -> str:
    """
    Generate a formatted employee evaluation summary.

    Parameters
    ----------
    employee_id : str
        Unique identifier for the employee.
    template : str
        Template string containing placeholders like
        '{personnel.name}', '{personnel.position}',
        and '{review.rating}'.

    Returns
    -------
    str
        The evaluation summary with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the employee ID is invalid or if the template attempts to access
        unauthorized data such as feedback or bonus.
    """
    # 1. Validate and fetch employee
    employee = _fetch_employee(employee_id)

    # 2. Build context for safe placeholders
    context = _build_context(employee)

    # 3. Replace placeholders safely
    return _replace_placeholders(template, context)


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     tmpl = (
#         "Employee: {personnel.name}\n"
#         "Position: {personnel.position}\n"
#         "Department: {personnel.department}\n"
#         "Rating: {review.rating}"
#     )
#     print(compile_employee_evaluation("E001", tmpl))