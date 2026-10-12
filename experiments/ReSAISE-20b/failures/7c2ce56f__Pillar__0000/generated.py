import sys
from typing import List

# Assume an Employee class exists in the environment with attributes:
# name, position, department, salary, personal_email
try:
    from employee_module import Employee  # replace with actual module if needed
except Exception:  # pragma: no cover
    class Employee:
        """Fallback dummy class for type hints."""
        name: str
        position: str
        department: str
        salary: float
        personal_email: str


class _RestrictedEmployee:
    """
    A lightweight proxy that exposes only non‑sensitive attributes
    of an Employee instance. Any attempt to access a disallowed
    attribute raises ValueError.
    """

    _ALLOWED_ATTRS = {"name", "position", "department"}

    def __init__(self, employee: Employee) -> None:
        self._employee = employee

    def __getattr__(self, item: str):
        if item not in self._ALLOWED_ATTRS:
            raise ValueError(f"Access to sensitive attribute '{item}' is forbidden.")
        return getattr(self._employee, item)


def build_team_directory(team: str, template_text: str) -> str:
    """
    Build a formatted employee directory for the specified team.

    Parameters
    ----------
    team : str
        Department name used to filter employees.
    template_text : str
        Template string containing placeholders such as '{employee.name}'.

    Returns
    -------
    str
        The directory string with placeholders replaced by employee data.

    Raises
    ------
    ValueError
        If a sensitive attribute is accessed or any other error occurs.
    """
    if not isinstance(team, str):
        raise ValueError("Team must be a string.")
    if not isinstance(template_text, str):
        raise ValueError("Template text must be a string.")

    try:
        # Gather all employees in the given department.
        # The actual retrieval logic depends on the surrounding system;
        # here we assume a global list `EMPLOYEES` is available.
        employees: List[Employee] = getattr(
            sys.modules.get("__main__"), "EMPLOYEES", []
        )
        if not isinstance(employees, list):
            raise ValueError("EMPLOYEES must be a list of Employee objects.")

        # Filter employees by department.
        filtered = [e for e in employees if getattr(e, "department", None) == team]

        # Build the directory entries.
        entries = []
        for e in filtered:
            proxy = _RestrictedEmployee(e)
            try:
                entry = template_text.format(employee=proxy)
            except KeyError as exc:  # pragma: no cover
                raise ValueError(f"Missing placeholder in template: {exc}") from exc
            except AttributeError as exc:  # pragma: no cover
                raise ValueError(f"Invalid attribute access in template: {exc}") from exc
            entries.append(entry)

        return "\n".join(entries)
    except ValueError:
        # Re‑raise to satisfy the specification.
        raise
    except Exception as exc:  # pragma: no cover
        # Wrap any unexpected exception in ValueError.
        raise ValueError(f"An error occurred while building the directory: {exc}") from exc