import re
from typing import List

# Assuming an Employee class exists elsewhere in the codebase.
# from employee_module import Employee  # placeholder import


RESTRICTED_FIELDS = {"salary", "personal_email"}
PLACEHOLDER_PATTERN = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def _validate_placeholder(field: str) -> None:
    """
    Ensure that the placeholder does not reference a restricted field.
    Raise ValueError if it does.
    """
    if field in RESTRICTED_FIELDS:
        raise ValueError(f"Access to restricted field '{field}' is not allowed.")


def _replace_placeholders(template: str, employee) -> str:
    """
    Replace all placeholders in the template with values from the given employee.
    """
    def repl(match):
        field_name = match.group(1)
        _validate_placeholder(field_name)
        try:
            value = getattr(employee, field_name)
        except AttributeError as exc:
            raise ValueError(f"Employee object has no attribute '{field_name}'.") from exc
        return str(value)

    try:
        result = PLACEHOLDER_PATTERN.sub(repl, template)
    except Exception as exc:
        # Catch any unexpected error during substitution
        raise ValueError("An error occurred while processing the template.") from exc

    return result


def build_worker_list(team_name: str, list_template: str) -> str:
    """
    Build a formatted employee directory for the specified department.

    Parameters
    ----------
    team_name : str
        The name of the department to filter employees by.
    list_template : str
        A string containing placeholders like '{employee.name}' and
        '{employee.position}'.  Only non‑restricted fields are allowed.

    Returns
    -------
    str
        A string containing the formatted directory for all employees in
        the specified department.

    Raises
    ------
    ValueError
        If a placeholder refers to a restricted field, an attribute is missing,
        or any other error occurs during processing.
    """
    # Import here to avoid circular dependencies if Employee imports this module
    from employee_module import Employee  # Replace with actual import

    try:
        employees: List[Employee] = [
            e for e in Employee.get_all() if e.department == team_name
        ]
    except Exception as exc:
        raise ValueError("Failed to retrieve employees.") from exc

    if not employees:
        return f"No employees found in department '{team_name}'."

    lines = []
    for emp in employees:
        try:
            line = _replace_placeholders(list_template, emp)
            lines.append(line)
        except ValueError as exc:
            # Re‑raise to surface the error to the caller
            raise

    return "\n".join(lines)