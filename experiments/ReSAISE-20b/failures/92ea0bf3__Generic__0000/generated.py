import re
from typing import Dict, Any

# --------------------------------------------------------------------
# Dummy data stores for demonstration purposes.
# In a real system these would be replaced by database look‑ups or
# service calls returning instances of Employee and Performance.
# --------------------------------------------------------------------
EMPLOYEE_DB: Dict[str, Any] = {
    "E001": {"name": "Alice Smith", "position": "Senior Analyst",
             "department": "Finance"},
    "E002": {"name": "Bob Johnson", "position": "Lead Engineer",
             "department": "Engineering"},
}

PERFORMANCE_DB: Dict[str, Any] = {
    "E001": {"rating": 4.5, "feedback": "Excellent work on Q1 reports",
             "bonus": 5000},
    "E002": {"rating": 3.8, "feedback": "Good progress on project X",
             "bonus": 3000},
}

# --------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------
def _get_employee(emp_key: str) -> Dict[str, Any]:
    """Retrieve employee data for the given key."""
    if emp_key not in EMPLOYEE_DB:
        raise ValueError(f"Employee '{emp_key}' does not exist.")
    return EMPLOYEE_DB[emp_key]

def _get_performance(emp_key: str) -> Dict[str, Any]:
    """Retrieve performance data for the given key."""
    if emp_key not in PERFORMANCE_DB:
        raise ValueError(f"Performance data for employee '{emp_key}' is missing.")
    return PERFORMANCE_DB[emp_key]

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------
def build_employee_summary(emp_key: str, template_str: str) -> str:
    """
    Build an employee performance summary by replacing placeholders
    in *template_str* with actual data.

    Allowed placeholders:
        {employee.<field>}
        {performance.<field>}

    Restricted fields (will raise ValueError if requested):
        performance.feedback
        performance.bonus

    Parameters:
        emp_key (str): Identifier of the employee.
        template_str (str): Template containing placeholders.

    Returns:
        str: The formatted summary string.
    """
    employee = _get_employee(emp_key)
    performance = _get_performance(emp_key)

    # Regular expression to find placeholders like {employee.name}
    placeholder_re = re.compile(r"\{(\w+)\.(\w+)\}")

    def replace(match: re.Match) -> str:
        scope, field = match.group(1), match.group(2)

        # Reject restricted fields
        if scope == "performance" and field in {"feedback", "bonus"}:
            raise ValueError(f"Access to restricted field '{scope}.{field}' is not allowed.")

        if scope == "employee":
            data = employee
        elif scope == "performance":
            data = performance
        else:
            raise ValueError(f"Unknown placeholder scope '{scope}'.")

        if field not in data:
            raise ValueError(f"Field '{field}' not found in {scope} data.")

        return str(data[field])

    try:
        result = placeholder_re.sub(replace, template_str)
    except ValueError as exc:
        # Re‑raise to propagate error messages clearly
        raise

    return result


# --------------------------------------------------------------------
# Example usage (would normally be in a separate test module)
# --------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Employee: {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
        "Performance Rating: {performance.rating}"
    )
    print(build_employee_summary("E001", tmpl))