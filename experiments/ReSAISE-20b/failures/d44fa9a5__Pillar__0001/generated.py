import re
from typing import Dict

# ------------------------------------------------------------------
# Mocked domain classes (in real usage these would be imported from the
# application's data layer).  They are deliberately minimal to keep the
# example self‑contained.
# ------------------------------------------------------------------
class Employee:
    def __init__(self, emp_id: str, name: str, position: str,
                 department: str):
        self.id = emp_id
        self.name = name
        self.position = position
        self.department = department

class Performance:
    def __init__(self, employee: Employee,
                 rating: str, feedback: str = None,
                 bonus: float | None = None):
        self.employee = employee
        self.rating = rating
        # Feedback and bonus are considered sensitive.  They should only be
        # accessed if explicitly requested via a safe interface.
        self._feedback = feedback
        self._bonus = bonus

    @property
    def feedback(self):
        raise PermissionError("Direct access to feedback is prohibited")

    @property
    def bonus(self):
        raise PermissionError("Direct access to bonus is prohibited")

# ------------------------------------------------------------------
# In‑memory data store – in a real system this would be replaced with
# database queries or an ORM.
# ------------------------------------------------------------------
EMPLOYEES: Dict[str, Employee] = {}
PERFORMANCES: Dict[str, Performance] = {}

def register_employee(emp_id: str,
                      name: str,
                      position: str,
                      department: str) -> None:
    """Utility helper to populate the in‑memory store."""
    emp = Employee(emp_id, name, position, department)
    EMPLOYEES[emp_id] = emp

def record_performance(emp_id: str,
                       rating: str,
                       feedback: str | None = None,
                       bonus: float | None = None) -> None:
    """Utility helper to populate the in‑memory store."""
    if emp_id not in EMPLOYEES:
        raise KeyError(f"Unknown employee id: {emp_id}")
    perf = Performance(EMPLOYEES[emp_id], rating, feedback, bonus)
    PERFORMANCES[emp_id] = perf

# ------------------------------------------------------------------
# Core functionality
# ------------------------------------------------------------------
PLACEHOLDER_RE = re.compile(r"{([^{}]+)}")

def create_employee_report(worker_id: str, template: str) -> str:
    """
    Generate a formatted performance report for the given employee.

    Parameters
    ----------
    worker_id : str
        The unique identifier of the employee.
    template : str
        A string containing placeholders such as '{worker.name}',
        '{assessment.rating}', etc.

    Returns
    -------
    str
        The fully formatted report string.

    Raises
    ------
    ValueError
        If the worker ID is unknown, or if the template contains a
        placeholder that references restricted data (feedback or bonus).
    """
    # Validate worker existence early to avoid unnecessary work.
    if worker_id not in EMPLOYEES:
        raise ValueError(f"Invalid worker id: {worker_id}")

    employee = EMPLOYEES[worker_id]
    performance = PERFORMANCES.get(worker_id)
    if not performance:
        raise ValueError(f"No performance record for worker id: {worker_id}")

    # Build a mapping of allowed placeholders to values.
    context = {
        "worker.name": employee.name,
        "worker.position": employee.position,
        "worker.department": employee.department,
        "assessment.rating": performance.rating
    }

    # Detect forbidden placeholders before substitution.
    for placeholder in PLACEHOLDER_RE.findall(template):
        if placeholder not in context:
            # The only forbidden placeholders are those that expose
            # sensitive data.  Any other unknown placeholder is also an error.
            if placeholder in {"assessment.feedback", "assessment.bonus"}:
                raise ValueError(
                    f"Unauthorized access to sensitive data: "
                    f"{placeholder}"
                )
            raise ValueError(f"Unknown placeholder in template: {placeholder}")

    # Perform substitution safely.  We use a lambda to avoid evaluating
    # arbitrary expressions.
    def repl(match: re.Match) -> str:
        key = match.group(1)
        return context[key]

    result = PLACEHOLDER_RE.sub(repl, template)
    return result

# ------------------------------------------------------------------
# Example usage (would normally be in a separate test module)
# ------------------------------------------------------------------
if __name__ == "__main__":
    # Setup sample data
    register_employee("E001", "Alice Smith", "Software Engineer",
                      "Engineering")
    record_performance("E001", rating="Exceeds Expectations",
                       feedback="Excellent problem‑solving skills.",
                       bonus=1500.00)

    tmpl = (
        "Employee Report:\n"
        "Name: {worker.name}\n"
        "Position: {worker.position}\n"
        "Department: {worker.department}\n"
        "Rating: {assessment.rating}"
    )

    print(create_employee_report("E001", tmpl))