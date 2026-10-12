import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
# Mock data structures (in a real system these would be imported from the
# company's data layer). The `Employee` object contains a nested
# `Performance` instance.
# --------------------------------------------------------------------------- #

@dataclass
class Performance:
    rating: str
    feedback: str
    bonus: float

@dataclass
class Employee:
    emp_id: str
    name: str
    position: str
    department: str
    performance: Performance

# --------------------------------------------------------------------------- #
# In‑memory registry of employees for demo purposes.  Replace with real
# persistence / service lookups in production.
# --------------------------------------------------------------------------- #

EMPLOYEE_REGISTRY: Dict[str, Employee] = {
    "E001": Employee(
        emp_id="E001",
        name="Alice Smith",
        position="Senior Engineer",
        department="R&D",
        performance=Performance(
            rating="Excellent",
            feedback="Outstanding contribution to project X.",
            bonus=5000.00,
        ),
    ),
    "E002": Employee(
        emp_id="E002",
        name="Bob Johnson",
        position="Junior Analyst",
        department="Finance",
        performance=Performance(
            rating="Satisfactory",
            feedback="Meets expectations.",
            bonus=1500.00,
        ),
    ),
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _get_employee(emp_id: str) -> Employee:
    """
    Retrieve an employee by ID. Raises ValueError if the ID is unknown.
    """
    try:
        return EMPLOYEE_REGISTRY[emp_id]
    except KeyError as exc:
        raise ValueError(f"Unknown employee ID: {emp_id}") from exc

_RE_PLACEHOLDER = re.compile(r"\{([^{}]+)\}")

def _replace_placeholder(match: re.Match, context: Dict[str, str]) -> str:
    """
    Replace a single placeholder with its corresponding value from the
    context dictionary. Raises ValueError if the key is missing.
    """
    key = match.group(1).strip()
    if key not in context:
        raise ValueError(f"Unknown placeholder: {key}")
    return str(context[key])

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def compile_performance_report(emp_id: str, report_template: str) -> str:
    """
    Generate a performance summary for the specified employee using
    `report_template`. Placeholders of the form `{employee.field}` or
    `{performance.field}` are replaced with actual values.

    Restricted fields (`feedback` and `bonus`) are disallowed; attempting
    to use them will raise ValueError.

    Parameters:
        emp_id (str): Unique identifier of the employee.
        report_template (str): Template containing placeholders.

    Returns:
        str: The formatted performance summary.

    Raises:
        ValueError: If the employee ID is invalid or a restricted field
                    is referenced.
    """
    # 1. Retrieve employee data
    employee = _get_employee(emp_id)

    # 2. Build a flat context mapping placeholder names to values
    context: Dict[str, str] = {
        # Employee attributes
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        # Performance attributes
        "performance.rating": employee.performance.rating,
    }

    # 3. Disallow restricted fields
    for restricted in ("performance.feedback", "performance.bonus"):
        if restricted in report_template:
            raise ValueError(f"Access to restricted field '{restricted}' is not allowed")

    # 4. Perform substitution
    try:
        result = _RE_PLACEHOLDER.sub(lambda m: _replace_placeholder(m, context), report_template)
    except ValueError as exc:
        raise  # re‑raise to propagate the error

    return result