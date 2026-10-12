import re
from dataclasses import dataclass
from typing import Dict

# ----------------------------------------------------------------------
# Minimal stubs for Employee and Performance (would normally be provided)
# ----------------------------------------------------------------------
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
    feedback: str
    bonus: float


# ----------------------------------------------------------------------
# In‑memory data store (in a real system this would be replaced by DB access)
# ----------------------------------------------------------------------
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(emp_id="E001", name="Alice Smith", position="Senior Engineer", department="R&D"),
    "E002": Employee(emp_id="E002", name="Bob Johnson", position="Manager", department="Sales"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(emp_id="E001", rating=4.7, feedback="Excellent problem solving.", bonus=1200.0),
    "E002": Performance(emp_id="E002", rating=3.9, feedback="Strong leadership.", bonus=800.0),
}


# ----------------------------------------------------------------------
# Helper to parse placeholders safely
# ----------------------------------------------------------------------
PLACEHOLDER_RE = re.compile(r"{(?P<obj>\w+)\.(?P<attr>\w+)}")

# Fields that are not allowed to be exposed in the report
RESTRICTED_FIELDS = {"feedback", "bonus"}


def compile_performance_report(emp_id: str, report_template: str) -> str:
    """
    Generate a performance summary for the given employee ID using the provided
    template string.

    Parameters:
        emp_id (str): The unique employee identifier.
        report_template (str): Template containing placeholders like
                               '{employee.name}', '{performance.rating}'.

    Returns:
        str: The formatted performance report.

    Raises:
        ValueError: If the employee ID is unknown, if a restricted field
                    (feedback or bonus) is referenced in the template,
                    or if any placeholder cannot be resolved.
    """
    # ------------------------------------------------------------------
    # 1. Validate employee existence
    # ------------------------------------------------------------------
    employee = EMPLOYEES.get(emp_id)
    if not employee:
        raise ValueError(f"Unknown employee ID: {emp_id}")

    performance = PERFORMANCES.get(emp_id)
    if not performance:
        raise ValueError(f"No performance data for employee ID: {emp_id}")

    # ------------------------------------------------------------------
    # 2. Scan template for placeholders and check restrictions
    # ------------------------------------------------------------------
    for match in PLACEHOLDER_RE.finditer(report_template):
        obj_name = match.group("obj")
        attr_name = match.group("attr")

        # Reject restricted fields
        if obj_name == "performance" and attr_name in RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted field '{attr_name}' is not allowed.")

        # Ensure the attribute exists on the corresponding object
        if obj_name == "employee":
            if not hasattr(employee, attr_name):
                raise ValueError(f"Attribute '{attr_name}' does not exist on Employee.")
        elif obj_name == "performance":
            if not hasattr(performance, attr_name):
                raise ValueError(f"Attribute '{attr_name}' does not exist on Performance.")
        else:
            raise ValueError(f"Unknown placeholder object '{obj_name}' in template.")

    # ------------------------------------------------------------------
    # 3. Build context and perform formatting
    # ------------------------------------------------------------------
    context = {
        "employee": employee,
        "performance": performance,
    }

    try:
        formatted_report = report_template.format(**context)
    except KeyError as exc:
        # This should not happen due to earlier checks, but guard anyway
        raise ValueError(f"Missing placeholder in template: {exc}") from exc

    return formatted_report


# ----------------------------------------------------------------------
# Example usage (commented out)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Employee Report for {employee.name} ({employee.position})\n"
        "Department: {employee.department}\n"
        "Performance Rating: {performance.rating:.1f}/5.0\n"
    )
    print(compile_performance_report("E001", template))