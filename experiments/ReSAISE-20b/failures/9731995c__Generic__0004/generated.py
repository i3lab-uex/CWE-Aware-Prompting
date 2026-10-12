import re
from dataclasses import dataclass
from typing import Dict

# --------------------------------------------------------------------------- #
# Dummy data structures – in a real system these would be replaced by ORM models
# --------------------------------------------------------------------------- #

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
    feedback: str   # Sensitive – must not be exposed
    bonus: float    # Sensitive – must not be exposed

# --------------------------------------------------------------------------- #
# In‑memory “database” for the purpose of this example
# --------------------------------------------------------------------------- #

EMPLOYEE_DB: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Senior Engineer", department="R&D"),
    "E002": Employee(id="E002", name="Bob Johnson", position="Product Manager", department="Marketing"),
}

PERFORMANCE_DB: Dict[str, Performance] = {
    "E001": Performance(employee_id="E001", rating=4.7, feedback="Excellent problem solving.", bonus=5000),
    "E002": Performance(employee_id="E002", rating=4.2, feedback="Great leadership.", bonus=3000),
}

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def generate_employee_summary(employee_id: str, template: str) -> str:
    """
    Generate a performance summary for the given employee based on the supplied template.
    
    Args:
        employee_id: The unique identifier of the employee.
        template: A string containing placeholders such as `{employee.name}` or
                  `{performance.rating}`.

    Returns:
        The rendered summary string with placeholders replaced by actual data.

    Raises:
        ValueError: If the employee or performance record cannot be found,
                    if a placeholder refers to sensitive data (`feedback` or `bonus`),
                    or if any other error occurs during rendering.
    """
    # Retrieve the data objects – raise ValueError if not found
    try:
        employee = EMPLOYEE_DB[employee_id]
    except KeyError as exc:
        raise ValueError(f"Employee with ID '{employee_id}' not found") from exc

    try:
        performance = PERFORMANCE_DB[employee_id]
    except KeyError as exc:
        raise ValueError(f"Performance record for employee '{employee_id}' not found") from exc

    # Detect sensitive placeholders
    sensitive_keywords = {"feedback", "bonus"}
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")
    for match in placeholder_pattern.finditer(template):
        expr = match.group(1).strip()
        # Only allow expressions that start with 'employee.' or 'performance.'
        if not (expr.startswith("employee.") or expr.startswith("performance.")):
            raise ValueError(f"Invalid placeholder '{match.group(0)}' in template")

        # Check for sensitive attributes
        if any(expr.endswith(f".{kw}") or expr == kw for kw in sensitive_keywords):
            raise ValueError("Access to sensitive information (feedback or bonus) is prohibited")

    # Build a mapping for allowed attributes
    context = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating,
    }

    # Replace placeholders
    def replacer(match):
        key = match.group(1).strip()
        try:
            return str(context[key])
        except KeyError as exc:
            raise ValueError(f"Unknown placeholder '{match.group(0)}'") from exc

    try:
        result = placeholder_pattern.sub(replacer, template)
    except Exception as exc:  # Catch any unforeseen errors during formatting
        raise ValueError("An error occurred while generating the summary") from exc

    return result


# --------------------------------------------------------------------------- #
# Example usage (for manual testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = (
        "Employee {employee.name} ({employee.position}) in {employee.department} "
        "has achieved a performance rating of {performance.rating}/5.0."
    )
    print(generate_employee_summary("E001", tmpl))