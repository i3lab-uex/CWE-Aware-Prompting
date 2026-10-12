import re
from dataclasses import dataclass
from typing import Dict, Any

# --------------------------------------------------------------------
# Data model (simplified for this example)
# --------------------------------------------------------------------

@dataclass
class Employee:
    code: str
    name: str
    position: str
    department: str

@dataclass
class Performance:
    employee_code: str
    rating: float          # e.g., 4.5 out of 5
    feedback: str          # restricted field
    bonus: float           # restricted field

# --------------------------------------------------------------------
# In‑memory "database" of employees and performances
# --------------------------------------------------------------------

EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(code="E001", name="Alice Smith", position="Software Engineer",
                     department="Engineering"),
    "E002": Employee(code="E002", name="Bob Johnson", position="Product Manager",
                     department="Product"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(employee_code="E001", rating=4.7,
                        feedback="Excellent problem solving and teamwork.",
                        bonus=1200.0),
    "E002": Performance(employee_code="E002", rating=4.2,
                        feedback="Strong leadership and vision.",
                        bonus=800.0),
}

# --------------------------------------------------------------------
# Utility: allowed fields
# --------------------------------------------------------------------

ALLOWED_EMPLOYEE_FIELDS = {"name", "position", "department"}
ALLOWED_PERFORMANCE_FIELDS = {"rating"}

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------

def create_performance_report(emp_code: str, summary_template: str) -> str:
    """
    Return a formatted performance report for the employee identified by `emp_code`.

    :param emp_code: Employee identifier.
    :param summary_template: Template string containing placeholders such as
                             '{employee.name}', '{performance.rating}'.
    :return: The formatted report string.
    :raises ValueError: If the employee or performance data is missing, or
                        if a restricted field is requested in the template.
    """
    # 1. Retrieve data
    employee = EMPLOYEES.get(emp_code)
    if not employee:
        raise ValueError(f"Employee with code '{emp_code}' not found.")

    performance = PERFORMANCES.get(emp_code)
    if not performance:
        raise ValueError(f"Performance record for employee '{emp_code}' not found.")

    # 2. Detect placeholders and validate access
    placeholder_pattern = re.compile(r"{([^{}]+)}")
    for match in placeholder_pattern.finditer(summary_template):
        field = match.group(1).strip()
        # Expect format 'employee.<field>' or 'performance.<field>'
        if '.' not in field:
            raise ValueError(f"Invalid placeholder '{field}'. Expected 'entity.attribute'.")
        entity, attr = field.split('.', 1)

        if entity == "employee":
            if attr not in ALLOWED_EMPLOYEE_FIELDS:
                raise ValueError(f"Access to restricted employee field '{attr}' is not allowed.")
        elif entity == "performance":
            if attr not in ALLOWED_PERFORMANCE_FIELDS:
                raise ValueError(f"Access to restricted performance field '{attr}' is not allowed.")
        else:
            raise ValueError(f"Unknown entity '{entity}' in placeholder.")

    # 3. Build mapping for formatting
    data_map: Dict[str, Any] = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating,
    }

    # 4. Perform formatting safely
    try:
        report = summary_template.format_map(data_map)
    except KeyError as exc:
        raise ValueError(f"Missing data for placeholder: {exc}") from None

    return report

# --------------------------------------------------------------------
# Example usage (uncomment to test)
# --------------------------------------------------------------------

# if __name__ == "__main__":
#     tmpl = ("Employee: {employee.name}\n"
#             "Position: {employee.position}\n"
#             "Department: {employee.department}\n"
#             "Performance Rating: {performance.rating}/5")
#     print(create_performance_report("E001", tmpl))