# employee_report.py

from dataclasses import dataclass, field
import re
from typing import Dict

# ---------- Data models ----------
@dataclass
class Performance:
    rating: str
    feedback: str = field(repr=False)   # sensitive, should not be exposed
    bonus: float = field(default=0.0, repr=False)  # sensitive


@dataclass
class Employee:
    id: str
    name: str
    position: str
    department: str
    performance: Performance


# ---------- In‑memory “database” ----------
EMPLOYEES_DB: Dict[str, Employee] = {
    "E001": Employee(
        id="E001",
        name="Alice Smith",
        position="Software Engineer",
        department="Engineering",
        performance=Performance(
            rating="Exceeds Expectations",
            feedback="Outstanding work on the core platform.",
            bonus=1500.0,
        ),
    ),
    "E002": Employee(
        id="E002",
        name="Bob Johnson",
        position="Product Manager",
        department="Product",
        performance=Performance(
            rating="Meets Expectations",
            feedback="Good coordination with the engineering team.",
            bonus=1200.0,
        ),
    ),
}


# ---------- Utility ----------
PLACEHOLDER_PATTERN = re.compile(r"{(?P<path>[\w\.]+)}")

# Fields that are disallowed to be exposed via the template
RESTRICTED_FIELDS = {"performance.feedback", "performance.bonus"}


def _get_attr_by_path(obj, path: str):
    """
    Resolve dotted attribute access on an object.
    Raises AttributeError if any part is missing.
    """
    attrs = path.split(".")
    current = obj
    for attr in attrs:
        if not hasattr(current, attr):
            raise AttributeError(f"Attribute '{attr}' not found in {current}")
        current = getattr(current, attr)
    return current


def create_employee_report(emp_id: str, template_str: str) -> str:
    """
    Generate a performance report for the given employee ID based on
    the supplied template string.

    Parameters
    ----------
    emp_id : str
        Identifier of the employee.
    template_str : str
        Template containing placeholders like '{employee.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the employee ID is unknown, if a restricted field is requested,
        or if an invalid placeholder is used.
    """
    # 1. Retrieve employee
    try:
        emp = EMPLOYEES_DB[emp_id]
    except KeyError as exc:
        raise ValueError(f"Employee ID '{emp_id}' not found") from exc

    # 2. Prepare context
    context = {"employee": emp, "performance": emp.performance}

    # 3. Find all placeholders
    placeholders = PLACEHOLDER_PATTERN.findall(template_str)

    for path in placeholders:
        # Reject restricted fields
        if path in RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted field '{path}' is not allowed")

        # Resolve the value
        try:
            value = _get_attr_by_path(context, path)
        except AttributeError as exc:
            raise ValueError(f"Invalid placeholder '{path}' in template") from exc

        # Replace the placeholder with string representation
        template_str = template_str.replace("{" + path + "}", str(value))

    return template_str


# ---------- Example usage ----------
if __name__ == "__main__":
    tmpl = (
        "Employee Report\n"
        "---------------\n"
        "Name: {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
        "Rating: {performance.rating}\n"
    )
    print(create_employee_report("E001", tmpl))