import re

# ----------------------------------------------------------------------
# Assuming an Employee class and a global list of employees exist in the
# application context.  The following is only a minimal placeholder to
# illustrate usage; in real code this would be imported from the relevant
# module.
#
# class Employee:
#     def __init__(self, name, position, department, salary, personal_email):
#         self.name = name
#         self.position = position
#         self.department = department
#         self.salary = salary
#         self.personal_email = personal_email
#
# EMPLOYEES: List[Employee] = [...]

# ----------------------------------------------------------------------
def generate_team_roster(division_name: str, roster_template: str) -> str:
    """
    Generate a formatted employee roster for the specified division using
    the provided template.

    Parameters
    ----------
    division_name : str
        The department name to filter employees by.
    roster_template : str
        A string template containing placeholders in the form
        `{employee.<attribute>}`.  Allowed attributes are
        ``name`` and ``position``.

    Returns
    -------
    str
        A newline‑separated string containing the rendered roster.

    Raises
    ------
    ValueError
        If the template references restricted fields (``salary`` or
        ``personal_email``) or if an unexpected error occurs during
        rendering.
    """
    # ------------------------------------------------------------------
    # 1. Validate the template for restricted fields
    # ------------------------------------------------------------------
    forbidden = {"salary", "personal_email"}
    # Find all placeholders of the form {employee.<field>}
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    fields_in_template = set(placeholder_pattern.findall(roster_template))

    if forbidden & fields_in_template:
        raise ValueError(
            f"Template contains restricted fields: {forbidden & fields_in_template}"
        )

    # Only allow name and position
    allowed_fields = {"name", "position"}
    if not fields_in_template <= allowed_fields:
        raise ValueError(
            f"Template contains unsupported fields: {fields_in_template - allowed_fields}"
        )

    # ------------------------------------------------------------------
    # 2. Filter employees by division
    # ------------------------------------------------------------------
    try:
        filtered_employees = [
            emp for emp in EMPLOYEES if getattr(emp, "department", None) == division_name
        ]
    except Exception as exc:
        raise ValueError(f"Failed to filter employees: {exc}") from exc

    # ------------------------------------------------------------------
    # 3. Render each employee using the template
    # ------------------------------------------------------------------
    rendered_lines = []
    for emp in filtered_employees:
        try:
            line = roster_template.format(employee=emp)
        except Exception as exc:
            raise ValueError(f"Failed to render template for {emp.name}: {exc}") from exc
        rendered_lines.append(line)

    return "\n".join(rendered_lines)