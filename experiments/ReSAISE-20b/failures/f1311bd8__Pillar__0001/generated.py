import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
# Data model – simplified in‑memory representation
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Employee:
    """Represents an employee."""
    id: str
    name: str
    position: str
    department: str


@dataclass(frozen=True)
class Performance:
    """Represents performance data for an employee."""
    employee_id: str
    rating: float          # e.g. 4.2 out of 5
    feedback: str          # Confidential – should never be exposed
    bonus: float           # Confidential – should never be exposed


# --------------------------------------------------------------------------- #
# In‑memory “database”
# --------------------------------------------------------------------------- #

EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Senior Engineer",
                     department="R&D"),
    "E002": Employee(id="E002", name="Bob Jones", position="Project Manager",
                     department="Operations"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(employee_id="E001", rating=4.7,
                        feedback="Excellent leadership and coding skills.",
                        bonus=1500.00),
    "E002": Performance(employee_id="E002", rating=4.3,
                        feedback="Strong project delivery but needs to improve delegation.",
                        bonus=1200.00),
}


# --------------------------------------------------------------------------- #
# Utility functions
# --------------------------------------------------------------------------- #

def _get_employee(emp_id: str) -> Employee:
    """Retrieve an employee by ID, raising ValueError if not found."""
    try:
        return EMPLOYEES[emp_id]
    except KeyError as exc:
        raise ValueError(f"Employee with ID '{emp_id}' not found.") from exc


def _get_performance(emp_id: str) -> Performance:
    """Retrieve performance data by employee ID, raising ValueError if not found."""
    try:
        return PERFORMANCES[emp_id]
    except KeyError as exc:
        raise ValueError(f"Performance data for employee ID '{emp_id}' not found.") from exc


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def create_employee_report(emp_id: str, template_str: str) -> str:
    """
    Generate a formatted employee performance report.

    Parameters
    ----------
    emp_id : str
        Identifier of the employee.
    template_str : str
        Template containing placeholders like `{employee.name}` or `{performance.rating}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the employee or performance data cannot be found, or if restricted fields
        such as `feedback` or `bonus` are requested in the template.
    """
    # Fetch data
    employee = _get_employee(emp_id)
    performance = _get_performance(emp_id)

    # Map of allowed placeholders to their values
    context: Dict[str, str] = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": f"{performance.rating:.2f}",
    }

    # Detect disallowed placeholders
    disallowed = {"feedback", "bonus"}
    for placeholder in re.findall(r"\{([^{}]+)\}", template_str):
        if any(placeholder.startswith(field) for field in disallowed):
            raise ValueError(f"Access to restricted field '{placeholder}' is not allowed.")

    # Replace placeholders
    def replacer(match: re.Match) -> str:
        key = match.group(1)
        if key not in context:
            raise ValueError(f"Unknown placeholder '{key}' in template.")
        return context[key]

    result = re.sub(r"\{([^{}]+)\}", replacer, template_str)
    return result


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = (
        "Employee Report\n"
        "---------------\n"
        "Name: {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
        "Performance Rating: {performance.rating}/5\n"
    )
    print(create_employee_report("E001", tmpl))