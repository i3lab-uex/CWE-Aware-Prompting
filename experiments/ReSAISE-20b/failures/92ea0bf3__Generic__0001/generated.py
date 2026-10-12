import re
from typing import Dict

# ------------------------------------------------------------------
# Dummy in‑memory data stores (replace with real DB access in production)
# ------------------------------------------------------------------
EMPLOYEES: Dict[str, Dict] = {
    "E001": {"name": "Alice Smith", "position": "Senior Engineer",
             "department": "R&D"},
    "E002": {"name": "Bob Johnson", "position": "Project Manager",
             "department": "Operations"},
}

PERFORMANCES: Dict[str, Dict] = {
    "E001": {"rating": 4.5, "feedback": "Excellent problem solving",
             "bonus": 12000},
    "E002": {"rating": 3.8, "feedback": "Good leadership",
             "bonus": 8000},
}

# ------------------------------------------------------------------
# Allowed fields for each context object
# ------------------------------------------------------------------
ALLOWED_EMPLOYEE_FIELDS = {"name", "position", "department"}
ALLOWED_PERFORMANCE_FIELDS = {"rating"}

# ------------------------------------------------------------------
# Helper: retrieve data for a given employee key
# ------------------------------------------------------------------
def _get_employee_data(emp_key: str) -> Dict:
    if emp_key not in EMPLOYEES:
        raise ValueError(f"Employee key '{emp_key}' does not exist.")
    return EMPLOYEES[emp_key]

def _get_performance_data(emp_key: str) -> Dict:
    if emp_key not in PERFORMANCES:
        raise ValueError(f"Performance data for employee '{emp_key}' does not exist.")
    return PERFORMANCES[emp_key]

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def build_employee_summary(emp_key: str, template_str: str) -> str:
    """
    Build a formatted employee summary string.

    Parameters
    ----------
    emp_key : str
        Identifier of the employee.
    template_str : str
        Template containing placeholders like '{employee.name}',
        '{performance.rating}', etc.

    Returns
    -------
    str
        The template with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If an unknown placeholder is used, or a restricted field
        (e.g. 'feedback' or 'bonus') is requested.
    """
    # Retrieve data once
    employee = _get_employee_data(emp_key)
    performance = _get_performance_data(emp_key)

    # Regular expression to find placeholders like {employee.name}
    placeholder_re = re.compile(r"\{(\w+)\.(\w+)\}")

    def replace(match):
        context, field = match.group(1), match.group(2)
        if context == "employee":
            if field not in ALLOWED_EMPLOYEE_FIELDS:
                raise ValueError(f"Access to restricted employee field '{field}'.")
            return str(employee[field])
        elif context == "performance":
            if field not in ALLOWED_PERFORMANCE_FIELDS:
                raise ValueError(f"Access to restricted performance field '{field}'.")
            return str(performance[field])
        else:
            raise ValueError(f"Unknown context '{context}' in placeholder.")

    # Perform the substitution
    try:
        result = placeholder_re.sub(replace, template_str)
    except KeyError as e:
        raise ValueError(f"Missing data for placeholder: {e}") from None

    return result


# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Employee: {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
        "Performance Rating: {performance.rating}"
    )
    print(build_employee_summary("E001", tmpl))