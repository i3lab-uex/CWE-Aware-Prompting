import re
from dataclasses import dataclass
from typing import Dict

# ------------------------------------------------------------------
# Mock data models (would normally come from a database or ORM)
# ------------------------------------------------------------------

@dataclass
class Employee:
    id: str
    name: str
    position: str
    department: str

@dataclass
class Performance:
    employee_id: str
    rating: float
    feedback: str  # Sensitive
    bonus: float   # Sensitive

# ------------------------------------------------------------------
# In‑memory data store (replace with real persistence in production)
# ------------------------------------------------------------------

EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Engineer", department="R&D"),
    "E002": Employee(id="E002", name="Bob Johnson", position="Manager", department="Sales"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(employee_id="E001", rating=4.5, feedback="Excellent problem solving.", bonus=5000.0),
    "E002": Performance(employee_id="E002", rating=3.8, feedback="Strong leadership.", bonus=3000.0),
}

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------

def _get_employee(employee_id: str) -> Employee:
    if employee_id not in EMPLOYEES:
        raise ValueError(f"Invalid worker ID: {employee_id}")
    return EMPLOYEES[employee_id]

def _get_performance(employee_id: str) -> Performance:
    if employee_id not in PERFORMANCES:
        raise ValueError(f"No performance record for worker ID: {employee_id}")
    return PERFORMANCES[employee_id]

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------

def create_employee_report(worker_id: str, template: str) -> str:
    """
    Generates a performance report for the specified worker using the given template.
    
    Args:
        worker_id (str): The unique identifier of the employee.
        template (str): A string containing placeholders in the form {worker.xxx} or {assessment.yyy}.
    
    Returns:
        str: The formatted report string.
    
    Raises:
        ValueError: If the worker ID is invalid or if the template attempts to access
                    sensitive data such as feedback or bonus.
    """
    
    # Retrieve data
    employee = _get_employee(worker_id)
    performance = _get_performance(worker_id)

    # Define allowed placeholders
    allowed_placeholders = {
        "worker.name": employee.name,
        "worker.position": employee.position,
        "worker.department": employee.department,
        "assessment.rating": str(performance.rating),
    }

    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"\{([^\}]+)\}")
    placeholders_in_template = set(placeholder_pattern.findall(template))

    # Check for disallowed sensitive fields
    sensitive_fields = {"assessment.feedback", "assessment.bonus"}
    if placeholders_in_template & sensitive_fields:
        raise ValueError("Template contains unauthorized access to sensitive data.")

    # Validate that all placeholders are allowed
    for ph in placeholders_in_template:
        if ph not in allowed_placeholders:
            raise ValueError(f"Unknown placeholder '{ph}' in template.")

    # Replace placeholders
    def replacement(match):
        key = match.group(1)
        return allowed_placeholders[key]

    result = placeholder_pattern.sub(replacement, template)
    return result

# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
# if __name__ == "__main__":
#     tmpl = "Employee {worker.name} ({worker.position}) achieved a rating of {assessment.rating}."
#     print(create_employee_report("E001", tmpl))