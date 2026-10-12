import re
from typing import List

# Assume the Employee class is defined elsewhere with the following attributes:
# name: str
# position: str
# department: str
# salary: float
# personal_email: str

def compile_department_roster(division: str, template_str: str) -> str:
    """
    Build a formatted employee directory for the given department.

    Parameters
    ----------
    division : str
        The name of the department to filter employees by.
    template_str : str
        A string containing placeholders such as '{employee.name}' or
        '{employee.position}'.  Placeholders for sensitive attributes
        (salary, personal_email) are disallowed.

    Returns
    -------
    str
        The directory string with placeholders replaced by employee data.

    Raises
    ------
    ValueError
        If a placeholder references a sensitive attribute or if any error
        occurs during processing.
    """
    # Collect employees belonging to the specified division.  The list
    # `EMPLOYEES` is assumed to be defined in the surrounding module.
    try:
        employees: List[Employee] = [
            e for e in EMPLOYEES if e.department == division
        ]
    except Exception as exc:
        raise ValueError(f"Failed to filter employees: {exc}") from exc

    # Regex for placeholders of the form {employee.attribute}
    placeholder_re = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    # Check for forbidden attributes
    forbidden = {"salary", "personal_email"}
    matches = placeholder_re.findall(template_str)
    for attr in set(matches):
        if attr in forbidden:
            raise ValueError(f"Access to sensitive attribute '{attr}' is not allowed.")

    # Prepare the output
    try:
        lines = []
        for emp in employees:
            line = template_str

            # Replace each placeholder with the corresponding attribute
            def repl(match: re.Match) -> str:
                attr_name = match.group(1)
                value = getattr(emp, attr_name)
                return str(value)

            line = placeholder_re.sub(repl, line)
            lines.append(line)

        return "\n".join(lines)
    except Exception as exc:
        raise ValueError(f"Error while compiling roster: {exc}") from exc