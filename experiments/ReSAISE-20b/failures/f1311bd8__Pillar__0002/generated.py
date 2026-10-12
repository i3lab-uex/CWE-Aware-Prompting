import re
from dataclasses import dataclass, fields

# ----------------------------------------------------------------------
# Domain model definitions
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Employee:
    """Represents an employee's basic information."""
    emp_id: str
    name: str
    position: str
    department: str

@dataclass(frozen=True)
class Performance:
    """Represents an employee's performance record."""
    rating: str
    feedback: str  # Sensitive
    bonus: float   # Sensitive

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
_RE_PLACEHOLDER = re.compile(r'\{([^}]+)\}')

def _extract_placeholders(template: str) -> set[str]:
    """Return a set of placeholder names found in the template."""
    return {m.group(1) for m in _RE_PLACEHOLDER.finditer(template)}

def _validate_placeholders(placeholders: set[str]) -> None:
    """Ensure that only allowed fields are referenced."""
    # Disallow any field containing 'feedback' or 'bonus'
    restricted = {'performance.feedback', 'performance.bonus'}
    for p in placeholders:
        if p in restricted or any(r in p for r in ('feedback', 'bonus')):
            raise ValueError(f"Access to restricted field '{p}' is not allowed")

def _safe_format(template: str, mapping: dict) -> str:
    """
    Perform a safe format operation.  All placeholders must be present in
    the mapping; otherwise raise ValueError.
    """
    # Verify all placeholders exist in mapping keys
    placeholders = _extract_placeholders(template)
    missing = [p for p in placeholders if p not in mapping]
    if missing:
        raise ValueError(f"Missing values for placeholders: {missing}")
    return template.format(**mapping)

# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def create_employee_report(emp_id: str, template_str: str) -> str:
    """
    Generate a performance report for the employee with ID `emp_id` using
    the provided template string.

    Parameters
    ----------
    emp_id : str
        Identifier of the employee to report on.
    template_str : str
        Template containing placeholders like '{employee.name}',
        '{performance.rating}', etc.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the template references restricted fields or if any placeholder
        cannot be resolved.
    """
    # ------------------------------------------------------------------
    # 1. Retrieve data (here we mock a simple in‑memory store)
    # ------------------------------------------------------------------
    # In a real system this would query a database or external service.
    _EMPLOYEE_DB = {
        "E001": Employee(emp_id="E001", name="Alice Smith",
                         position="Senior Analyst", department="Finance"),
        "E002": Employee(emp_id="E002", name="Bob Johnson",
                         position="Developer", department="Engineering"),
    }

    _PERFORMANCE_DB = {
        "E001": Performance(rating="Exceeds Expectations",
                            feedback="Outstanding analytical skills.",
                            bonus=1200.00),
        "E002": Performance(rating="Meets Expectations",
                            feedback="Solid coding practices.",
                            bonus=800.00),
    }

    employee = _EMPLOYEE_DB.get(emp_id)
    performance = _PERFORMANCE_DB.get(emp_id)

    if employee is None or performance is None:
        raise ValueError(f"Employee data for ID '{emp_id}' not found")

    # ------------------------------------------------------------------
    # 2. Validate template placeholders
    # ------------------------------------------------------------------
    placeholders = _extract_placeholders(template_str)
    _validate_placeholders(placeholders)

    # ------------------------------------------------------------------
    # 3. Prepare mapping for formatting
    # ------------------------------------------------------------------
    mapping = {
        "employee": employee,
        "performance": performance,
    }

    # ------------------------------------------------------------------
    # 4. Perform safe formatting
    # ------------------------------------------------------------------
    return _safe_format(template_str, mapping)

# ----------------------------------------------------------------------
# Example usage (commented out to avoid accidental execution)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     tmpl = ("Employee: {employee.name}\n"
#             "Position: {employee.position}\n"
#             "Rating: {performance.rating}")
#     print(create_employee_report("E001", tmpl))