import re
from typing import Any

# Assume these classes are defined elsewhere in the codebase.
try:
    from company.models import Employee, Performance
except Exception:  # pragma: no cover
    # Minimal stubs for type checking / example usage
    class Performance:
        def __init__(self, rating: str, feedback: str, bonus: float):
            self.rating = rating
            self.feedback = feedback
            self.bonus = bonus

    class Employee:
        def __init__(self, employee_id: str, name: str, position: str,
                     department: str, performance: Performance):
            self.id = employee_id
            self.name = name
            self.position = position
            self.department = department
            self.performance = performance

        @staticmethod
        def get_by_id(emp_id: str) -> "Employee":
            # Dummy implementation – replace with real lookup logic
            if emp_id == "12345":
                perf = Performance("Excellent", "Great work!", 5000.0)
                return Employee(emp_id, "Alice Smith", "Software Engineer",
                                "Engineering", perf)
            raise ValueError(f"Employee with ID {emp_id} not found.")


# ---------------------------------------------------------------------------

RESTRICTED_FIELDS = {"feedback", "bonus"}
PLACEHOLDER_PATTERN = re.compile(r"{([^{}]+)}")


def _resolve_placeholder(obj: Any, path: str) -> str:
    """
    Resolve a dotted attribute path on an object.
    Raises AttributeError if any part of the chain is missing.
    """
    attrs = path.split(".")
    value: Any = obj
    for attr in attrs:
        if not hasattr(value, attr):
            raise AttributeError(f"Attribute '{attr}' not found in {value!r}")
        value = getattr(value, attr)
    return str(value)


def construct_employee_report(employee_id: str, report_template: str) -> str:
    """
    Construct a performance report for the given employee using the supplied template.

    Parameters
    ----------
    employee_id : str
        Unique identifier of the employee.
    report_template : str
        Template string containing placeholders such as '{employee.name}' or
        '{performance.rating}'. Placeholders that refer to restricted fields
        (e.g. 'feedback' or 'bonus') are disallowed.

    Returns
    -------
    str
        The fully formatted report string.

    Raises
    ------
    ValueError
        If the employee ID is invalid or if a restricted field is referenced.
    """
    # Retrieve the employee instance
    try:
        employee = Employee.get_by_id(employee_id)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Invalid employee ID '{employee_id}'.") from exc

    # Find all placeholders in the template
    placeholders = PLACEHOLDER_PATTERN.findall(report_template)

    # Validate and replace each placeholder
    for placeholder in placeholders:
        if any(field in placeholder.split(".") for field in RESTRICTED_FIELDS):
            raise ValueError(
                f"Access to restricted field(s) in placeholder '{placeholder}'."
            )

        # Resolve the value
        try:
            if placeholder.startswith("employee."):
                value = _resolve_placeholder(employee, placeholder.replace("employee.", ""))
            elif placeholder.startswith("performance."):
                value = _resolve_placeholder(employee.performance, placeholder.replace("performance.", ""))
            else:
                raise ValueError(f"Unsupported placeholder prefix in '{placeholder}'.")
        except AttributeError as exc:  # pragma: no cover
            raise ValueError(f"Invalid placeholder '{placeholder}'.") from exc

        # Replace all occurrences of the placeholder
        report_template = report_template.replace(f"{{{placeholder}}}", value)

    return report_template


# ---------------------------------------------------------------------------
# Example usage (for local testing only – remove or guard with __name__ == "__main__")
if __name__ == "__main__":
    tmpl = (
        "Employee Report for {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
        "Performance Rating: {performance.rating}\n"
    )
    print(construct_employee_report("12345", tmpl))