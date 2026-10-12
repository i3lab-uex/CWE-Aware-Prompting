import re
from typing import Dict, Any

# ----------------------------------------------------------------------
# Mock data structures (in a real system these would come from a database
# or other persistent store).  They are kept simple for the purposes of
# this example.
# ----------------------------------------------------------------------
class Performance:
    """Represents an employee's performance data."""
    def __init__(self, rating: str, feedback: str, bonus: float):
        self.rating = rating
        self._feedback = feedback   # Sensitive data – should not be exposed
        self._bonus = bonus          # Sensitive data – should not be exposed

    @property
    def feedback(self) -> str:
        """Access to feedback is intentionally blocked for security reasons."""
        raise PermissionError("Unauthorized access to employee feedback")

    @property
    def bonus(self) -> float:
        """Access to bonus is intentionally blocked for security reasons."""
        raise PermissionError("Unauthorized access to employee bonus")


class Employee:
    """Represents an employee record."""
    def __init__(self, emp_id: str, name: str, position: str,
                 department: str, performance: Performance):
        self.id = emp_id
        self.name = name
        self.position = position
        self.department = department
        self.performance = performance


# ----------------------------------------------------------------------
# Sample in‑memory registry of employees.
# ----------------------------------------------------------------------
EMPLOYEE_REGISTRY: Dict[str, Employee] = {}

def _register_employee(emp: Employee) -> None:
    """Adds an employee to the in‑memory registry."""
    EMPLOYEE_REGISTRY[emp.id] = emp


# ----------------------------------------------------------------------
# Populate the registry with some sample data
# ----------------------------------------------------------------------
_register_employee(Employee(
    emp_id="E001",
    name="Alice Johnson",
    position="Software Engineer",
    department="Engineering",
    performance=Performance(rating="Excellent", feedback="Great teamwork", bonus=1200.0)
))

_register_employee(Employee(
    emp_id="E002",
    name="Bob Smith",
    position="Product Manager",
    department="Product",
    performance=Performance(rating="Satisfactory", feedback="Needs improvement in metrics tracking", bonus=800.0)
))


# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def build_employee_report(employee_id: str, template: str) -> str:
    """
    Build a formatted performance report for an employee.

    Parameters
    ----------
    employee_id : str
        The unique identifier of the employee.
    template : str
        A string containing placeholders such as `{staff.name}` or `{evaluation.rating}`.

    Returns
    -------
    str
        The template with placeholders replaced by actual employee data.

    Raises
    ------
    ValueError
        If the employee_id is not found or if the template tries to access
        sensitive data (`feedback` or `bonus`) which is not permitted.
    """
    # ------------------------------------------------------------------
    # 1. Retrieve the employee record
    # ------------------------------------------------------------------
    employee = EMPLOYEE_REGISTRY.get(employee_id)
    if employee is None:
        raise ValueError(f"Employee ID '{employee_id}' not found")

    # ------------------------------------------------------------------
    # 2. Prepare the context for formatting
    # ------------------------------------------------------------------
    context: Dict[str, Any] = {
        "staff": {
            "id": employee.id,
            "name": employee.name,
            "position": employee.position,
            "department": employee.department
        },
        "evaluation": {
            "rating": employee.performance.rating
            # Note: `feedback` and `bonus` are intentionally omitted
        }
    }

    # ------------------------------------------------------------------
    # 3. Detect forbidden placeholders in the template
    # ------------------------------------------------------------------
    placeholder_pattern = re.compile(r"{\s*([a-zA-Z0-9_.]+)\s*}")
    forbidden_fields = {"feedback", "bonus"}

    for match in placeholder_pattern.finditer(template):
        key_path = match.group(1).split(".")
        if len(key_path) < 2:
            continue  # Not a nested key – ignore

        base, field = key_path[0], key_path[-1]
        if base in ("staff", "evaluation") and field in forbidden_fields:
            raise ValueError(
                f"Template attempts to access unauthorized field '{field}'"
            )

    # ------------------------------------------------------------------
    # 4. Perform the formatting safely
    # ------------------------------------------------------------------
    try:
        formatted = template.format(**context)
    except KeyError as exc:
        # A placeholder in the template did not have a corresponding value
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return formatted