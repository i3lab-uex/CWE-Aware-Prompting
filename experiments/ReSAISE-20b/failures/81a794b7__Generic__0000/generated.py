import re
from typing import Any

# ----------------------------------------------------------------------
# Dummy data structures – in a real system these would be imported
# from the application's models or database layer.
# ----------------------------------------------------------------------
class Performance:
    """Represents an employee's performance record."""
    def __init__(self, rating: str, feedback: str, bonus: float):
        self.rating = rating          # public
        self.feedback = feedback      # private – should not be exposed
        self.bonus = bonus            # private – should not be exposed

class Employee:
    """Represents an employee."""
    _registry = {}

    def __init__(self, emp_id: str, name: str, position: str,
                 department: str, performance: Performance):
        self.id = emp_id
        self.name = name
        self.position = position
        self.department = department
        self.performance = performance

    @classmethod
    def get_by_id(cls, emp_id: str) -> "Employee":
        """Retrieve an employee instance by ID or raise ValueError."""
        try:
            return cls._registry[emp_id]
        except KeyError as exc:
            raise ValueError(f"Invalid employee ID: {emp_id}") from exc

    @classmethod
    def register(cls, emp: "Employee"):
        cls._registry[emp.id] = emp

# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
PLACEHOLDER_PATTERN = re.compile(r"\{([^\{\}]+)\}")

ALLOWED_ATTRIBUTES = {
    "employee": {"id", "name", "position", "department"},
    "performance": {"rating"},  # only rating is allowed
}

def _resolve_path(obj: Any, path_parts: list[str]) -> Any:
    """
    Resolve a dotted attribute path on an object.
    Raises ValueError if any part is disallowed or missing.
    """
    for part in path_parts:
        # Security check: only allow predefined attributes
        obj_type = type(obj).__name__.lower()
        allowed = ALLOWED_ATTRIBUTES.get(obj_type, set())
        if part not in allowed:
            raise ValueError(f"Unauthorized access to '{obj_type}.{part}'")
        try:
            obj = getattr(obj, part)
        except AttributeError as exc:
            raise ValueError(f"Attribute '{part}' not found on {obj_type}") from exc
    return obj

def compile_employee_evaluation(employee_id: str, template: str) -> str:
    """
    Generate a performance summary for an employee by replacing placeholders
    in the provided template with actual data.

    Parameters:
        employee_id (str): Unique identifier for the employee.
        template (str): Template string containing placeholders such as
                        '{employee.name}', '{performance.rating}'.

    Returns:
        str: The formatted performance summary.

    Raises:
        ValueError: If the employee ID is invalid or if the template
                    attempts to access disallowed data (e.g., feedback,
                    bonus, or any other unauthorized attribute).
    """
    # Retrieve the employee instance
    employee = Employee.get_by_id(employee_id)

    def _replacement(match: re.Match) -> str:
        placeholder = match.group(1).strip()
        # Expected format: <object>.<attribute>
        if "." not in placeholder:
            raise ValueError(f"Malformed placeholder: '{placeholder}'")
        obj_name, attr_path = placeholder.split(".", 1)
        # Resolve the base object
        if obj_name == "employee":
            base_obj = employee
        elif obj_name == "performance":
            base_obj = employee.performance
        else:
            raise ValueError(f"Unknown placeholder object: '{obj_name}'")

        # Resolve the attribute chain safely
        value = _resolve_path(base_obj, attr_path.split("."))
        return str(value)

    # Perform substitution
    try:
        result = PLACEHOLDER_PATTERN.sub(_replacement, template)
    except ValueError as exc:
        # Re‑raise with a clear message
        raise ValueError(f"Failed to compile evaluation: {exc}") from exc

    return result

# ----------------------------------------------------------------------
# Example usage (would normally be in a separate test module)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Setup dummy data
    perf = Performance(rating="Excellent", feedback="Great teamwork", bonus=5000.0)
    emp = Employee(emp_id="E123", name="Alice Smith",
                   position="Software Engineer", department="R&D", performance=perf)
    Employee.register(emp)

    tmpl = ("Employee: {employee.name}\n"
            "Position: {employee.position}\n"
            "Department: {employee.department}\n"
            "Performance Rating: {performance.rating}")

    print(compile_employee_evaluation("E123", tmpl))