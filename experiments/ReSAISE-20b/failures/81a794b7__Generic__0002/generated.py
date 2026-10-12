import re
from dataclasses import dataclass
from typing import Dict

# ------------------------------------------------------------------
# Dummy data models (in real code these would be imported from the
# application's domain layer)
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
    # In a real system other sensitive fields (feedback, bonus) would exist
    # but are intentionally omitted here.

# ------------------------------------------------------------------
# In-memory "database" for demo purposes
# ------------------------------------------------------------------
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Software Engineer", department="R&D"),
    "E002": Employee(id="E002", name="Bob Johnson", position="Product Manager", department="Product"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(employee_id="E001", rating=4.5),
    "E002": Performance(employee_id="E002", rating=3.8),
}

# ------------------------------------------------------------------
# Core function
# ------------------------------------------------------------------
PLACEHOLDER_PATTERN = re.compile(r"\{([a-zA-Z_][a-zA-Z0-9_.]*)\}")

def compile_employee_evaluation(employee_id: str, template: str) -> str:
    """
    Replace placeholders in `template` with employee and performance data.

    Supported placeholders:
        {personnel.name}      -> Employee.name
        {personnel.position}  -> Employee.position
        {personnel.department}-> Employee.department
        {review.rating}       -> Performance.rating

    Raises:
        ValueError: If the employee_id is unknown or if an unauthorized
                    placeholder (e.g., containing 'feedback' or 'bonus')
                    is present in the template.
    """
    # ------------------------------------------------------------------
    # Validate employee ID
    # ------------------------------------------------------------------
    employee = EMPLOYEES.get(employee_id)
    if not employee:
        raise ValueError(f"Unknown employee ID: {employee_id}")

    performance = PERFORMANCES.get(employee_id)
    if not performance:
        raise ValueError(f"No performance record for employee ID: {employee_id}")

    # ------------------------------------------------------------------
    # Process placeholders
    # ------------------------------------------------------------------
    def replacement(match: re.Match) -> str:
        key = match.group(1)

        # Reject any placeholder that might expose sensitive data
        if re.search(r"(feedback|bonus)", key, flags=re.IGNORECASE):
            raise ValueError(f"Unauthorized placeholder detected: {key}")

        # Map keys to actual values
        if key == "personnel.name":
            return employee.name
        elif key == "personnel.position":
            return employee.position
        elif key == "personnel.department":
            return employee.department
        elif key == "review.rating":
            # Format rating to one decimal place
            return f"{performance.rating:.1f}"
        else:
            # Unknown placeholder; keep it unchanged or raise an error
            raise ValueError(f"Unknown placeholder: {key}")

    # ------------------------------------------------------------------
    # Apply replacements
    # ------------------------------------------------------------------
    try:
        result = PLACEHOLDER_PATTERN.sub(replacement, template)
    except re.error as exc:
        raise ValueError(f"Template processing error: {exc}") from exc

    return result


# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Employee Report:\n"
        "Name: {personnel.name}\n"
        "Position: {personnel.position}\n"
        "Department: {personnel.department}\n"
        "Performance Rating: {review.rating}"
    )
    print(compile_employee_evaluation("E001", tmpl))