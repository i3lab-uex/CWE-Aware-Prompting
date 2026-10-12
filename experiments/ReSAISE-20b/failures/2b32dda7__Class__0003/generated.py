import re
from dataclasses import dataclass

# ---------- Mock data structures (replace with real implementations) ----------
@dataclass
class Employee:
    emp_id: str
    name: str
    position: str
    department: str

@dataclass
class Performance:
    emp_id: str
    rating: float
    feedback: str  # sensitive
    bonus: float   # sensitive

# In a real system these would be fetched from a database
EMPLOYEES = {
    "E001": Employee("E001", "Alice Smith", "Software Engineer", "Engineering"),
    "E002": Employee("E002", "Bob Johnson", "Product Manager", "Product"),
}
PERFORMANCES = {
    "E001": Performance("E001", 4.5, "Excellent work on project X.", 5000),
    "E002": Performance("E002", 3.8, "Good leadership.", 3000),
}

# ---------- Core function ----------
def compile_performance_report(emp_id: str, report_template: str) -> str:
    """
    Generate a performance summary for the given employee using the provided template.

    :param emp_id: The unique identifier of the employee.
    :param report_template: A template string containing placeholders like
                            '{employee.name}', '{performance.rating}', etc.
    :return: A formatted string with placeholders replaced by actual values.
    :raises ValueError: If the employee ID is invalid or if the template
                        attempts to access restricted fields.
    """
    # Validate employee existence
    employee = EMPLOYEES.get(emp_id)
    performance = PERFORMANCES.get(emp_id)

    if not employee or not performance:
        raise ValueError(f"Invalid employee ID: {emp_id}")

    # Define allowed placeholders
    allowed_placeholders = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating,
    }

    # Find all placeholders in the template
    pattern = r"\{([^{}]+)\}"
    tokens = re.findall(pattern, report_template)

    # Check for restricted fields
    restricted = {"performance.feedback", "performance.bonus"}
    for token in tokens:
        if token in restricted:
            raise ValueError(f"Access to restricted field '{token}' is not allowed.")
        if token not in allowed_placeholders:
            raise ValueError(f"Unknown placeholder '{token}' in template.")

    # Replace placeholders
    def replacer(match):
        key = match.group(1)
        return str(allowed_placeholders[key])

    result = re.sub(pattern, replacer, report_template)
    return result

# ---------- Example usage ----------
if __name__ == "__main__":
    template = (
        "Employee Report:\n"
        "Name: {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
        "Performance Rating: {performance.rating}"
    )
    print(compile_performance_report("E001", template))