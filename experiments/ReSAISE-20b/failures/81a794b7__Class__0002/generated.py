import re
from typing import Dict

# --------------------------------------------------------------------------- #
# Mock data structures – in a real system these would be replaced by ORM models
# --------------------------------------------------------------------------- #

class Employee:
    def __init__(self, employee_id: str, name: str, position: str, department: str):
        self.id = employee_id
        self.name = name
        self.position = position
        self.department = department


class Performance:
    def __init__(self, employee_id: str, rating: float,
                 feedback: str = None, bonus: float = None):
        self.employee_id = employee_id
        self.rating = rating          # public
        self.feedback = feedback      # sensitive
        self.bonus = bonus            # sensitive


# Example in‑memory "database"
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee("E001", "Alice Smith", "Software Engineer", "Engineering"),
    "E002": Employee("E002", "Bob Johnson", "Product Manager", "Product"),
}

PERFORMANCE_DB: Dict[str, Performance] = {
    "E001": Performance("E001", 4.5, feedback="Excellent teamwork.", bonus=1200),
    "E002": Performance("E002", 3.8, feedback="Good leadership.", bonus=800),
}


# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def compile_employee_evaluation(employee_id: str, template: str) -> str:
    """
    Generate a performance summary for the specified employee by replacing
    placeholders in *template* with actual data.

    Allowed placeholders:
        {employee.name}
        {employee.position}
        {employee.department}
        {performance.rating}

    Attempting to access sensitive fields such as feedback or bonus will raise
    a ValueError.

    Parameters:
        employee_id (str): Unique identifier for the employee.
        template (str): Template containing placeholders.

    Returns:
        str: The formatted performance summary.

    Raises:
        ValueError: If the employee ID is unknown, or if a forbidden
                    placeholder is used.
    """
    # 1. Validate employee existence
    emp = EMPLOYEES.get(employee_id)
    if not emp:
        raise ValueError(f"Unknown employee ID: {employee_id}")

    perf = PERFORMANCE_DB.get(employee_id)
    if not perf:
        raise ValueError(f"No performance data for employee ID: {employee_id}")

    # 2. Prepare a context dictionary with only allowed fields
    context = {
        "employee.name": emp.name,
        "employee.position": emp.position,
        "employee.department": emp.department,
        "performance.rating": perf.rating,
    }

    # 3. Find all placeholders in the template
    placeholder_pattern = re.compile(r"\{([^}]+)\}")
    placeholders = set(placeholder_pattern.findall(template))

    # 4. Validate that all placeholders are permitted
    for ph in placeholders:
        if ph not in context:
            # Detect forbidden sensitive fields
            if ph.startswith("performance.") and ph not in {"performance.rating"}:
                raise ValueError(f"Unauthorized access to sensitive field: {ph}")
            else:
                raise ValueError(f"Unknown placeholder in template: {ph}")

    # 5. Perform the substitution safely
    def replacement(match):
        key = match.group(1)
        return str(context[key])

    result = placeholder_pattern.sub(replacement, template)
    return result


# --------------------------------------------------------------------------- #
# Example usage
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = (
        "Employee Report for {employee.name}:\n"
        "- Position: {employee.position}\n"
        "- Department: {employee.department}\n"
        "- Performance Rating: {performance.rating}\n"
    )
    print(compile_employee_evaluation("E001", tmpl))