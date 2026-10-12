import re
from dataclasses import dataclass
from typing import Dict, Any

# ----------------------------------------------------------------------
# Domain model definitions (minimal stubs for the task)
# ----------------------------------------------------------------------
@dataclass
class Employee:
    """Represents an employee."""
    id: str
    name: str
    position: str
    department: str

@dataclass
class Performance:
    """Represents performance data for an employee."""
    rating: str
    feedback: str  # Sensitive
    bonus: float   # Sensitive

# ----------------------------------------------------------------------
# In‑memory data store (simulating a database)
# ----------------------------------------------------------------------
_EMPLOYEE_DB: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Software Engineer", department="Engineering"),
    "E002": Employee(id="E002", name="Bob Johnson", position="Product Manager", department="Product"),
}

_PERFORMANCE_DB: Dict[str, Performance] = {
    "E001": Performance(rating="Excellent", feedback="Outstanding contributions to the core platform.", bonus=1200.0),
    "E002": Performance(rating="Satisfactory", feedback="Met project deadlines.", bonus=800.0),
}

# ----------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------
def _get_employee(employee_id: str) -> Employee:
    """Retrieve an employee from the data store."""
    try:
        return _EMPLOYEE_DB[employee_id]
    except KeyError as exc:
        raise ValueError(f"Invalid employee ID: {employee_id}") from exc

def _get_performance(employee_id: str) -> Performance:
    """Retrieve performance data for an employee."""
    try:
        return _PERFORMANCE_DB[employee_id]
    except KeyError as exc:
        # In practice this should never happen if employee IDs are validated first
        raise ValueError(f"No performance data for employee ID: {employee_id}") from exc

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def build_employee_report(employee_id: str, template: str) -> str:
    """
    Build a performance report for the specified employee.

    Args:
        employee_id: Unique identifier of the employee.
        template: Template string containing placeholders such as
                  '{staff.name}', '{performance.rating}'.

    Returns:
        A formatted string with placeholders replaced by actual data.

    Raises:
        ValueError: If the employee ID is invalid or if the template
                    attempts to access sensitive fields like feedback or bonus.
    """
    # 1. Validate employee existence
    employee = _get_employee(employee_id)
    performance = _get_performance(employee_id)

    # 2. Detect unauthorized placeholders
    placeholder_pattern = re.compile(r"\{([^}]+)\}")
    for match in placeholder_pattern.finditer(template):
        key = match.group(1).strip()
        # Reject any attempt to access sensitive data
        if key.startswith("performance.") and key.split(".", 1)[1] in {"feedback", "bonus"}:
            raise ValueError(f"Unauthorized access to sensitive field: {key}")

    # 3. Build a context dictionary for safe formatting
    context: Dict[str, Any] = {
        "staff.name": employee.name,
        "staff.position": employee.position,
        "staff.department": employee.department,
        "performance.rating": performance.rating,
    }

    # 4. Replace placeholders using a safe approach
    def replace(match: re.Match) -> str:
        key = match.group(1).strip()
        if key not in context:
            raise ValueError(f"Unknown placeholder: {key}")
        return str(context[key])

    result = placeholder_pattern.sub(replace, template)
    return result

# ----------------------------------------------------------------------
# Example usage (commented out – for reference only)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     tmpl = ("Employee: {staff.name}\n"
#             "Position: {staff.position}\n"
#             "Department: {staff.department}\n"
#             "Rating: {performance.rating}")
#     print(build_employee_report("E001", tmpl))