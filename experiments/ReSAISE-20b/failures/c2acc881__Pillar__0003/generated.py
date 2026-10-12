import string
from dataclasses import dataclass, field
from typing import List

# ----------------------------------------------------------------------
# Data model (normally provided elsewhere in the application)
# ----------------------------------------------------------------------
@dataclass
class Employee:
    name: str
    position: str
    department: str
    salary: float = field(repr=False)          # sensitive
    personal_email: str = field(repr=False)   # sensitive

# Example global employee pool (in a real system this would come from a DB)
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000.0, "alice.smith@example.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 120000.0, "bob.johnson@example.com"),
    Employee("Carol Williams", "Analyst", "Finance", 80000.0, "carol.williams@example.com"),
]

# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def compile_department_roster(division: str, template_str: str) -> str:
    """
    Generate a formatted employee directory for the specified division.

    Parameters
    ----------
    division : str
        The department name used to filter employees.
    template_str : str
        A string containing placeholders like '{employee.name}' or
        '{employee.position}'. Only non‑sensitive attributes are allowed.

    Returns
    -------
    str
        The concatenated directory entries for all employees in the
        specified division.

    Raises
    ------
    ValueError
        If a placeholder references a sensitive attribute or if any
        error occurs during formatting.
    """
    # ------------------------------------------------------------------
    # Validate placeholders – disallow sensitive attributes
    # ------------------------------------------------------------------
    allowed_attrs = {"name", "position", "department"}
    formatter = string.Formatter()

    for literal_text, field_name, format_spec, conversion in formatter.parse(template_str):
        if not field_name:
            continue

        # Field names are expected to be of the form 'employee.attr'
        parts = field_name.split(".")
        if len(parts) != 2 or parts[0] != "employee":
            raise ValueError(f"Unsupported placeholder format: '{field_name}'")

        attr = parts[1]
        if attr not in allowed_attrs:
            raise ValueError(f"Access to sensitive attribute '{attr}' is forbidden.")

    # ------------------------------------------------------------------
    # Build the directory
    # ------------------------------------------------------------------
    entries: List[str] = []

    for emp in EMPLOYEES:
        if getattr(emp, "department", None) != division:
            continue

        try:
            entry = template_str.format(employee=emp)
        except Exception as exc:  # pragma: no cover
            raise ValueError(
                f"Failed to format entry for employee '{emp.name}': {exc}"
            ) from exc

        entries.append(entry)

    return "\n".join(entries)