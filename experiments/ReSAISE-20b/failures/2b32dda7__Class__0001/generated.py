import re
from typing import Dict

# ----------------------------------------------------------------------
# Sample data structures (in a real system these would be replaced by
# database look‑ups or ORM models).  They are included here only so that
# the function can be run and tested in isolation.
# ----------------------------------------------------------------------
class Employee:
    def __init__(self, emp_id: str, name: str, position: str,
                 department: str):
        self.emp_id = emp_id
        self.name = name
        self.position = position
        self.department = department


class Performance:
    def __init__(self, emp_id: str, rating: float,
                 feedback: str = None, bonus: float = None):
        self.emp_id = emp_id
        self.rating = rating
        self.feedback = feedback  # Sensitive
        self.bonus = bonus         # Sensitive


# Dummy in‑memory "database"
_EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee("E001", "Alice Smith", "Software Engineer",
                     "Engineering"),
    "E002": Employee("E002", "Bob Johnson", "Product Manager",
                     "Product"),
}

_PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance("E001", 4.5,
                        feedback="Excellent problem solving",
                        bonus=1200),
    "E002": Performance("E002", 3.8,
                        feedback="Good leadership",
                        bonus=800),
}


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_employee(emp_id: str) -> Employee:
    """Retrieve an employee object or raise ValueError."""
    try:
        return _EMPLOYEES[emp_id]
    except KeyError as exc:
        raise ValueError(f"Invalid employee ID: {emp_id}") from exc


def _get_performance(emp_id: str) -> Performance:
    """Retrieve a performance object or raise ValueError."""
    try:
        return _PERFORMANCES[emp_id]
    except KeyError as exc:
        raise ValueError(f"No performance data for employee ID: {emp_id}") from exc


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def compile_performance_report(emp_id: str, report_template: str) -> str:
    """
    Generate a performance summary for the specified employee.

    Parameters
    ----------
    emp_id : str
        Unique identifier of the employee.
    report_template : str
        Template string containing placeholders such as
        '{employee.name}', '{performance.rating}', etc.

    Returns
    -------
    str
        The formatted performance report.

    Raises
    ------
    ValueError
        If the employee ID is invalid, if restricted fields are accessed,
        or if a placeholder refers to an unknown attribute.
    """
    # Validate employee and performance records
    employee = _get_employee(emp_id)
    performance = _get_performance(emp_id)

    # Define which attributes are allowed to be exposed
    ALLOWED_EMP_ATTRS = {"name", "position", "department"}
    ALLOWED_PERF_ATTRS = {"rating"}

    # Regular expression to find placeholders of the form {something}
    placeholder_re = re.compile(r"\{([^{}]+)\}")

    def _replace_placeholder(match: re.Match) -> str:
        key = match.group(1).strip()
        # The placeholder must be of the form <source>.<attribute>
        if "." not in key:
            raise ValueError(f"Invalid placeholder format: '{key}'")

        source, attr = key.split(".", 1)

        if source == "employee":
            if attr not in ALLOWED_EMP_ATTRS:
                raise ValueError(f"Access to restricted or unknown employee field: '{attr}'")
            return getattr(employee, attr)
        elif source == "performance":
            if attr not in ALLOWED_PERF_ATTRS:
                raise ValueError(f"Access to restricted or unknown performance field: '{attr}'")
            return getattr(performance, attr)
        else:
            raise ValueError(f"Unknown data source in placeholder: '{source}'")

    # Perform the substitution safely
    try:
        formatted_report = placeholder_re.sub(_replace_placeholder, report_template)
    except ValueError as exc:
        # Re‑raise to maintain the same exception type
        raise

    return formatted_report


# ----------------------------------------------------------------------
# Example usage (commented out; remove comments to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     tmpl = (
#         "Employee: {employee.name}\n"
#         "Position: {employee.position}\n"
#         "Department: {employee.department}\n"
#         "Performance Rating: {performance.rating}"
#     )
#     print(compile_performance_report("E001", tmpl))