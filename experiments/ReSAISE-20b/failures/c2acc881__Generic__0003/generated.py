import re
from typing import List

# ------------------------------------------------------------------
# The Employee class is assumed to exist elsewhere in the project.
# It must expose at least the following attributes:
#   - name: str
#   - position: str
#   - department: str
#   - salary: float (sensitive)
#   - personal_email: str (sensitive)
#
# For the purpose of this implementation we only reference these
# attributes; no concrete definition is required here.
#
# ------------------------------------------------------------------
# A global list of all employees.  In a real project this would
# be populated from a database or another data source.
EMPLOYEES: List["Employee"] = []   # type: ignore

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------
def _extract_placeholders(template: str) -> List[str]:
    """
    Return a list of placeholder names found in the template.
    Placeholders are expected to be in the form {employee.<attr>}.
    """
    pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    return pattern.findall(template)

def _validate_placeholders(placeholders: List[str]) -> None:
    """
    Raise ValueError if any placeholder refers to a sensitive attribute.
    """
    SENSITIVE = {"salary", "personal_email"}
    for attr in placeholders:
        if attr in SENSITIVE:
            raise ValueError(f"Attempt to expose sensitive data: '{attr}'")

def _format_employee(employee, template: str) -> str:
    """
    Format the template for a single employee.
    """
    # Build a mapping of allowed attributes
    attrs = {
        "name": getattr(employee, "name"),
        "position": getattr(employee, "position"),
        "department": getattr(employee, "department"),
    }
    try:
        return template.format(**{f"employee.{k}": v for k, v in attrs.items()})
    except Exception as exc:
        # Any formatting error is treated as a generic processing failure
        raise ValueError(f"Formatting failed: {exc}") from exc

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def compile_department_roster(division: str, template_str: str) -> str:
    """
    Generate a formatted employee directory for the given department.

    Parameters
    ----------
    division : str
        The department name used to filter employees.
    template_str : str
        A string containing placeholders in the form {employee.<attr>}.

    Returns
    -------
    str
        The concatenated formatted directory for all employees in the
        specified department.

    Raises
    ------
    ValueError
        If a placeholder refers to sensitive data or if any error occurs
        during processing.
    """
    # Validate placeholders before proceeding
    placeholders = _extract_placeholders(template_str)
    _validate_placeholders(placeholders)

    # Filter employees by department
    relevant = [emp for emp in EMPLOYEES if getattr(emp, "department", None) == division]

    # Format each employee's details
    formatted_entries = []
    for emp in relevant:
        try:
            formatted_entries.append(_format_employee(emp, template_str))
        except ValueError as exc:
            # Propagate formatting errors
            raise

    return "\n".join(formatted_entries)