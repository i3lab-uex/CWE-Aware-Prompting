import re
from typing import Dict

# ----------------------------------------------------
# Mock data structures – in a real system these would be
# provided by the application.  They are included here so
# that the function can run as a self‑contained example.
# ----------------------------------------------------
class Employee:
    def __init__(self, emp_id: str, name: str, position: str, department: str):
        self.emp_id = emp_id
        self.name = name
        self.position = position
        self.department = department


class Performance:
    def __init__(self, emp_id: str, rating: float, feedback: str, bonus: float):
        self.emp_id = emp_id
        self.rating = rating
        self.feedback = feedback          # *unauthorized*
        self.bonus = bonus                # *unauthorized*


# Sample in‑memory data store
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee("E001", "Alice Smith", "Software Engineer", "Engineering"),
    "E002": Employee("E002", "Bob Johnson", "Product Manager", "Product"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance("E001", 4.5, "Excellent work on the recent release.", 5000),
    "E002": Performance("E002", 4.2, "Great leadership on the Q3 roadmap.", 4500),
}


# ----------------------------------------------------
# Core function
# ----------------------------------------------------
def build_employee_report(employee_id: str, template: str) -> str:
    """
    Build a performance report for an employee using the supplied template.

    Parameters
    ----------
    employee_id : str
        Unique identifier of the employee.
    template : str
        Template string containing placeholders such as
        `{staff.name}`, `{staff.position}`, `{evaluation.rating}`.

    Returns
    -------
    str
        The formatted performance report.

    Raises
    ------
    ValueError
        If the employee_id is unknown or if the template tries to
        access unauthorized fields (`feedback`, `bonus`).
    """
    # 1. Validate employee existence
    if employee_id not in EMPLOYEES:
        raise ValueError(f"Unknown employee ID: {employee_id}")

    # 2. Extract allowed data
    emp = EMPLOYEES[employee_id]
    perf = PERFORMANCES.get(employee_id)

    # 3. Detect unauthorized placeholders
    # Allowed namespaces: staff, evaluation
    forbidden = {"feedback", "bonus"}
    placeholder_pattern = re.compile(r"{\s*(?P<namespace>\w+)\.(?P<field>\w+)\s*}")
    for match in placeholder_pattern.finditer(template):
        namespace = match.group("namespace")
        field = match.group("field")

        # Reject any attempt to read unauthorized fields
        if namespace == "evaluation" and field in forbidden:
            raise ValueError(f"Unauthorized access to '{field}' in template")

        # Optionally, reject unknown namespaces/fields
        if namespace == "staff" and not hasattr(emp, field):
            raise ValueError(f"Unknown staff attribute '{field}'")
        if namespace == "evaluation" and not hasattr(perf, field):
            raise ValueError(f"Unknown evaluation attribute '{field}'")

    # 4. Build a context dictionary for safe formatting
    context = {
        "staff": {
            "name": emp.name,
            "position": emp.position,
            "department": emp.department,
        },
        "evaluation": {
            "rating": perf.rating if perf else None,
        },
    }

    # 5. Perform substitution
    def replace_placeholder(match: re.Match) -> str:
        namespace = match.group("namespace")
        field = match.group("field")
        value = context.get(namespace, {}).get(field)
        if value is None:
            return ""  # or raise? We'll silently replace with empty
        return str(value)

    result = placeholder_pattern.sub(replace_placeholder, template)
    return result


# ----------------------------------------------------
# Example usage (uncomment to test):
# ----------------------------------------------------
# if __name__ == "__main__":
#     tmpl = ("Employee Report:\n"
#             "Name: {staff.name}\n"
#             "Position: {staff.position}\n"
#             "Department: {staff.department}\n"
#             "Rating: {evaluation.rating}\n")
#     print(build_employee_report("E001", tmpl))