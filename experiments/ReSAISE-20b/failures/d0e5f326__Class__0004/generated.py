import re
from dataclasses import dataclass
from typing import Dict

# ----------------------------------------------------------------------
# Mock data structures (would normally be provided by the system)
# ----------------------------------------------------------------------


@dataclass
class Employee:
    """Represents an employee."""
    id: str
    name: str
    position: str
    department: str
    feedback: str  # Sensitive information
    bonus: float   # Sensitive information


@dataclass
class Performance:
    """Represents a performance evaluation."""
    employee_id: str
    rating: float  # Publicly viewable


# ----------------------------------------------------------------------
# Example in‑memory data store
# ----------------------------------------------------------------------


# Pretend we have a small database of employees and performances.
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(
        id="E001",
        name="Alice Johnson",
        position="Senior Developer",
        department="Engineering",
        feedback="Excellent problem solving skills.",
        bonus=5000.00,
    ),
    "E002": Employee(
        id="E002",
        name="Bob Smith",
        position="Product Manager",
        department="Product",
        feedback="Strong leadership in product launches.",
        bonus=7500.00,
    ),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(employee_id="E001", rating=4.8),
    "E002": Performance(employee_id="E002", rating=4.5),
}


# ----------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------


def _get_employee(employee_id: str) -> Employee:
    """Retrieve an employee object, raising ValueError if not found."""
    try:
        return EMPLOYEES[employee_id]
    except KeyError as exc:
        raise ValueError(f"Invalid employee ID: {employee_id}") from exc


def _get_performance(employee_id: str) -> Performance:
    """Retrieve a performance object, raising ValueError if not found."""
    try:
        return PERFORMANCES[employee_id]
    except KeyError as exc:
        raise ValueError(f"No performance data for employee ID: {employee_id}") from exc


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------


def build_employee_report(employee_id: str, template: str) -> str:
    """
    Build a formatted performance report for an employee.

    Parameters
    ----------
    employee_id : str
        The unique identifier of the employee.
    template : str
        A string containing placeholders to be replaced, e.g.,
        '{staff.name}', '{staff.position}', '{evaluation.rating}'.

    Returns
    -------
    str
        The report with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the employee ID is invalid, or if the template contains an
        unauthorized placeholder (e.g., accessing feedback or bonus).
    """
    # Retrieve data
    employee = _get_employee(employee_id)
    performance = _get_performance(employee_id)

    # Define which placeholders are allowed and their corresponding values
    placeholder_map = {
        "staff.name": employee.name,
        "staff.position": employee.position,
        # We intentionally exclude department, feedback, bonus
        "evaluation.rating": f"{performance.rating:.1f}",
    }

    # Find all placeholders in the template
    pattern = re.compile(r"\{([^}]+)\}")
    matches = pattern.findall(template)

    # Check for unauthorized placeholders
    for placeholder in matches:
        if placeholder not in placeholder_map:
            raise ValueError(
                f"Unauthorized or unknown placeholder '{{{placeholder}}}' in template."
            )

    # Perform substitution
    def replacer(match: re.Match) -> str:
        key = match.group(1)
        return placeholder_map[key]

    result = pattern.sub(replacer, template)

    return result


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Employee Report for {staff.name}\n"
        "Position: {staff.position}\n"
        "Rating: {evaluation.rating}"
    )
    print(build_employee_report("E001", tmpl))