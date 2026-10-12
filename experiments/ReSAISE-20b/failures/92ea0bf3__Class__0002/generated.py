import re
from dataclasses import dataclass, field
from typing import Any, Dict


# ----------------------------------------------------------------------
# Data models (minimal implementation for the example)
# ----------------------------------------------------------------------
@dataclass
class Performance:
    rating: float
    # Sensitive fields that must not be exposed via the template
    feedback: str = field(repr=False, default="")  # e.g., manager's comments
    bonus: float = field(repr=False, default=0.0)   # monetary bonus


@dataclass
class Employee:
    emp_id: str
    name: str
    position: str
    department: str
    performance: Performance


# ----------------------------------------------------------------------
# In‑memory "database" (for demonstration purposes)
# ----------------------------------------------------------------------
EMPLOYEES_DB: Dict[str, Employee] = {
    "E001": Employee(
        emp_id="E001",
        name="Alice Smith",
        position="Senior Engineer",
        department="R&D",
        performance=Performance(rating=4.5, feedback="Excellent work on project X", bonus=1200),
    ),
    "E002": Employee(
        emp_id="E002",
        name="Bob Johnson",
        position="Project Manager",
        department="Operations",
        performance=Performance(rating=3.8, feedback="Good leadership", bonus=800),
    ),
}


# ----------------------------------------------------------------------
# Helper: safe mapping for template formatting
# ----------------------------------------------------------------------
class SafeTemplateMapping(dict):
    """
    Mapping that raises ValueError when a restricted key is accessed.
    """

    _restricted_keys = {"feedback", "bonus"}

    def __getitem__(self, key: str) -> Any:
        # Split into object and attribute (e.g., 'employee.name')
        parts = key.split(".")
        if len(parts) != 2:
            raise KeyError(f"Invalid placeholder '{key}'. Expected format 'object.attribute'.")
        obj_name, attr = parts
        if obj_name != "employee":
            raise KeyError(f"Unknown object '{obj_name}'. Only 'employee' is supported.")
        if attr in self._restricted_keys:
            raise ValueError(f"Access to restricted field '{attr}' is not allowed.")
        return super().__getitem__(key)


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def build_employee_summary(emp_key: str, template_str: str) -> str:
    """
    Build a formatted employee performance summary.

    Parameters
    ----------
    emp_key : str
        The identifier of the employee.
    template_str : str
        The string containing placeholders like '{employee.name}', etc.

    Returns
    -------
    str
        The formatted summary string.

    Raises
    ------
    ValueError
        If the employee ID is not found, or if a restricted field is requested.
    """
    # Retrieve employee data
    employee = EMPLOYEES_DB.get(emp_key)
    if not employee:
        raise ValueError(f"Employee with ID '{emp_key}' does not exist.")

    # Build a mapping for all allowed attributes
    mapping: Dict[str, Any] = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        # Performance fields that are allowed
        "performance.rating": employee.performance.rating,
    }

    # Detect placeholders in the template and validate them
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")
    for match in placeholder_pattern.finditer(template_str):
        key = match.group(1)
        if key not in mapping:
            # Allow nested access like 'employee.name' or 'performance.rating'
            if key.startswith("employee.") and key.split(".")[1] in {"name", "position", "department"}:
                continue
            if key.startswith("performance.") and key.split(".")[1] == "rating":
                continue
            raise ValueError(f"Unknown placeholder '{key}' in template.")

    # Use SafeTemplateMapping to guard against restricted fields
    safe_mapping = SafeTemplateMapping(mapping)

    try:
        formatted = template_str.format_map(safe_mapping)
    except KeyError as exc:
        raise ValueError(f"Missing data for placeholder: {exc}") from None
    except ValueError as exc:
        # Propagate restricted field errors
        raise

    return formatted


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     tpl = "Employee: {employee.name}, Position: {employee.position}\nRating: {performance.rating}"
#     print(build_employee_summary("E001", tpl))