import re
from dataclasses import dataclass

# --- Data models -------------------------------------------------------------

@dataclass(frozen=True)
class Employee:
    """Basic employee information."""
    id: str
    name: str
    position: str
    department: str


@dataclass(frozen=True)
class Performance:
    """Performance metrics for an employee."""
    rating: str
    # Sensitive fields that must never be exposed in a report
    feedback: str = ""
    bonus: float = 0.0


# --- In‑memory data store (for demonstration) ------------------------------

EMPLOYEES = {
    "E001": Employee(id="E001", name="Alice Smith", position="Senior Analyst",
                     department="Finance"),
    "E002": Employee(id="E002", name="Bob Johnson", position="Developer",
                     department="Engineering"),
}

PERFORMANCES = {
    "E001": Performance(rating="Exceeds Expectations", feedback="Great work!", bonus=1200.0),
    "E002": Performance(rating="Meets Expectations", feedback="Solid performance.", bonus=800.0),
}


# --- Helper functions -------------------------------------------------------

def _get_employee(emp_id: str) -> Employee:
    try:
        return EMPLOYEES[emp_id]
    except KeyError as exc:
        raise ValueError(f"Employee ID '{emp_id}' not found") from exc


def _get_performance(emp_id: str) -> Performance:
    try:
        return PERFORMANCES[emp_id]
    except KeyError as exc:
        raise ValueError(f"Performance data for employee ID '{emp_id}' not found") from exc


# --- Main function ----------------------------------------------------------

def create_employee_report(emp_id: str, template_str: str) -> str:
    """
    Generate a performance report for the given employee using the supplied template.

    Parameters
    ----------
    emp_id : str
        Identifier of the employee.
    template_str : str
        Template string containing placeholders such as '{employee.name}' or
        '{performance.rating}'. Allowed placeholders:
            - employee.name
            - employee.position
            - employee.department
            - performance.rating

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the employee or performance data cannot be found, or if the template
        references disallowed fields (e.g., feedback, bonus).
    """
    employee = _get_employee(emp_id)
    performance = _get_performance(emp_id)

    # Map of allowed placeholders to their actual values
    placeholder_map = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating,
    }

    # Regular expression to find placeholders of the form {key}
    pattern = re.compile(r"\{([^{}]+)\}")

    def replace(match: re.Match) -> str:
        key = match.group(1)
        if key not in placeholder_map:
            # Disallowed or unknown field – raise an error
            raise ValueError(f"Disallowed placeholder '{key}' in template")
        return str(placeholder_map[key])

    try:
        result = pattern.sub(replace, template_str)
    except ValueError as exc:
        # Re‑raise with context
        raise ValueError(f"Invalid template: {exc}") from exc

    return result


# --- Example usage ----------------------------------------------------------

if __name__ == "__main__":
    template = (
        "Employee Report\n"
        "----------------\n"
        "Name: {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
        "Performance Rating: {performance.rating}\n"
    )
    print(create_employee_report("E001", template))