import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
# Domain model (minimal implementation for the example)
# --------------------------------------------------------------------------- #

@dataclass
class Performance:
    rating: str
    feedback: str = field(repr=False)  # sensitive, should not be exposed
    bonus: float = field(default=0.0)   # sensitive, should not be exposed


@dataclass
class Employee:
    code: str
    name: str
    position: str
    department: str
    performance: Performance


# --------------------------------------------------------------------------- #
# In‑memory "database" of employees (for demonstration purposes)
# --------------------------------------------------------------------------- #

EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(
        code="E001",
        name="Alice Smith",
        position="Senior Engineer",
        department="R&D",
        performance=Performance(
            rating="Excellent",
            feedback="Outstanding project leadership.",
            bonus=12000.0,
        ),
    ),
    "E002": Employee(
        code="E002",
        name="Bob Johnson",
        position="Marketing Lead",
        department="Marketing",
        performance=Performance(
            rating="Good",
            feedback="Strong campaign execution.",
            bonus=8000.0,
        ),
    ),
}


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

_ALLOWED_PLACEHOLDERS = {
    "employee.name",
    "employee.position",
    "employee.department",
    "performance.rating",
}

_PLACEHOLDER_PATTERN = re.compile(r"\{([^{}]+)\}")


def _resolve_placeholder(placeholder: str, employee: Employee) -> str:
    """
    Resolve a single placeholder against the employee object.
    Raises ValueError if the placeholder is not allowed or cannot be resolved.
    """
    if placeholder not in _ALLOWED_PLACEHOLDERS:
        raise ValueError(f"Disallowed or unknown placeholder: {{{placeholder}}}")

    if placeholder == "employee.name":
        return employee.name
    if placeholder == "employee.position":
        return employee.position
    if placeholder == "employee.department":
        return employee.department
    if placeholder == "performance.rating":
        return employee.performance.rating

    # Should never reach here due to the allowed set
    raise ValueError(f"Unhandled placeholder: {{{placeholder}}}")


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def create_performance_report(emp_code: str, summary_template: str) -> str:
    """
    Return a formatted performance report string for the given employee.
    
    Parameters
    ----------
    emp_code : str
        The unique identifier of the employee.
    summary_template : str
        A template string containing placeholders such as
        '{employee.name}', '{performance.rating}', etc.
    
    Returns
    -------
    str
        The template with placeholders substituted by actual data.
    
    Raises
    ------
    ValueError
        If the employee code is unknown, or if the template contains a
        disallowed or invalid placeholder.
    """
    # ----------------------------------------------------------------------- #
    # 1. Retrieve the employee
    # ----------------------------------------------------------------------- #
    employee = EMPLOYEES.get(emp_code)
    if not employee:
        raise ValueError(f"Unknown employee code: {emp_code}")

    # ----------------------------------------------------------------------- #
    # 2. Find and replace placeholders
    # ----------------------------------------------------------------------- #
    def replacement(match: re.Match) -> str:
        placeholder = match.group(1)
        return _resolve_placeholder(placeholder, employee)

    try:
        result = _PLACEHOLDER_PATTERN.sub(replacement, summary_template)
    except re.error as exc:
        # Catch regex compilation errors (unlikely but defensive)
        raise ValueError(f"Invalid template format: {exc}") from exc

    return result


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     template = (
#         "Employee: {employee.name}\n"
#         "Position: {employee.position}\n"
#         "Department: {employee.department}\n"
#         "Rating: {performance.rating}"
#     )
#     print(create_performance_report("E001", template))