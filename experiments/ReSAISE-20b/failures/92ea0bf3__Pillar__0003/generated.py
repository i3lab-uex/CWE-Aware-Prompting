import re
from typing import Dict

# --- Dummy data structures for demonstration ---------------------------------
# In a real system these would be replaced with proper database look‑ups or
# service calls.

class Employee:
    def __init__(self, name: str, position: str, department: str,
                 feedback: str = None, bonus: float | None = None):
        self.name = name
        self.position = position
        self.department = department
        # These are considered restricted fields
        self.feedback = feedback
        self.bonus = bonus

class Performance:
    def __init__(self, rating: str):
        self.rating = rating


# Example registries
EMPLOYEE_REGISTRY: Dict[str, Employee] = {
    "E001": Employee("Alice Smith", "Senior Engineer", "R&D",
                     feedback="Excellent collaboration.", bonus=5000),
    "E002": Employee("Bob Johnson", "Project Manager", "Operations",
                     feedback="Needs improvement in time management.", bonus=3000),
}

PERFORMANCE_REGISTRY: Dict[str, Performance] = {
    "E001": Performance("Outstanding"),
    "E002": Performance("Meets Expectations"),
}


# --- Core function -----------------------------------------------------------

def build_employee_summary(emp_key: str, template_str: str) -> str:
    """
    Build a formatted employee performance summary.

    Parameters
    ----------
    emp_key : str
        Identifier for the employee.
    template_str : str
        Template containing placeholders such as '{employee.name}',
        '{performance.rating}', etc.

    Returns
    -------
    str
        The formatted summary string.

    Raises
    ------
    ValueError
        If the employee or performance data is missing, if a placeholder
        refers to an unknown attribute, or if a restricted field is requested.
    """
    # Retrieve the employee and performance objects
    try:
        emp = EMPLOYEE_REGISTRY[emp_key]
        perf = PERFORMANCE_REGISTRY[emp_key]
    except KeyError as exc:
        raise ValueError(f"Missing data for employee key '{emp_key}'.") from exc

    # Define allowed fields and restricted fields
    ALLOWED_FIELDS = {
        "employee": {"name", "position", "department"},
        "performance": {"rating"},
    }
    RESTRICTED_FIELDS = {"feedback", "bonus"}

    # Regular expression to find placeholders like {employee.name}
    placeholder_pattern = re.compile(r"\{([^}]+)\}")

    def _replace(match: re.Match) -> str:
        """
        Replacement function for re.sub. Validates and returns the value
        corresponding to each placeholder.
        """
        full_path = match.group(1).strip()
        if "." not in full_path:
            raise ValueError(f"Invalid placeholder '{full_path}'. "
                             f"Expected format '{{object.attribute}}'.")

        obj_name, attr = full_path.split(".", 1)

        if obj_name not in ("employee", "performance"):
            raise ValueError(f"Unknown object '{obj_name}' in placeholder "
                             f"'{full_path}'. Only 'employee' and 'performance' "
                             "are supported.")

        if attr in RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted field '{attr}' is not allowed.")

        if attr not in ALLOWED_FIELDS[obj_name]:
            raise ValueError(f"Attribute '{attr}' is not allowed for object "
                             f"'{obj_name}'. Allowed attributes: {sorted(ALLOWED_FIELDS[obj_name])}")

        # Retrieve the attribute value
        if obj_name == "employee":
            return str(getattr(emp, attr))
        else:  # performance
            return str(getattr(perf, attr))

    try:
        formatted = placeholder_pattern.sub(_replace, template_str)
    except ValueError as exc:
        # Re‑raise with context
        raise ValueError(f"Failed to build summary: {exc}") from exc

    return formatted


# --- Example usage -----------------------------------------------------------

if __name__ == "__main__":
    template = ("Employee: {employee.name}\n"
                "Position: {employee.position}\n"
                "Department: {employee.department}\n"
                "Performance Rating: {performance.rating}")

    print(build_employee_summary("E001", template))