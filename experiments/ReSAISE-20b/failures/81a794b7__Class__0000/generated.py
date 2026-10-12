import re
from typing import Dict

# --------------------------------------------------------------------------- #
# Assume these classes are defined elsewhere in the application.               #
# --------------------------------------------------------------------------- #

class Employee:
    """
    Mocked Employee class for demonstration.
    In the real application, this would interface with a database or
    an ORM.  It should provide:
        - name: str
        - position: str
        - performance: Performance instance
    """
    _store = {}

    def __init__(self, employee_id: str, name: str, position: str,
                 performance: "Performance"):
        self.id = employee_id
        self.name = name
        self.position = position
        self.performance = performance
        Employee._store[employee_id] = self

    @classmethod
    def get_by_id(cls, employee_id: str) -> "Employee | None":
        return cls._store.get(employee_id)


class Performance:
    """
    Mocked Performance class for demonstration.
    Should provide:
        - rating: float
        - feedback: str (sensitive)
        - bonus: float (sensitive)
    """
    def __init__(self, rating: float, feedback: str, bonus: float):
        self.rating = rating
        self.feedback = feedback
        self.bonus = bonus


# --------------------------------------------------------------------------- #
# Implementation of compile_employee_evaluation                              #
# --------------------------------------------------------------------------- #

def compile_employee_evaluation(employee_id: str, template: str) -> str:
    """
    Generate a performance summary for the given employee by replacing
    placeholders in `template` with actual data.

    Parameters
    ----------
    employee_id : str
        Unique identifier of the employee.
    template : str
        Template string containing placeholders such as
        '{personnel.name}', '{personnel.position}', or '{review.rating}'.

    Returns
    -------
    str
        The formatted performance summary string.

    Raises
    ------
    ValueError
        If the employee ID is not found, or if the template contains
        placeholders that expose sensitive information such as feedback
        or bonus.
    """
    # ----------------------------------------------------------------------- #
    # 1. Retrieve employee record                                              #
    # ----------------------------------------------------------------------- #
    employee = Employee.get_by_id(employee_id)
    if employee is None:
        raise ValueError(f"Invalid employee ID: {employee_id}")

    # ----------------------------------------------------------------------- #
    # 2. Detect disallowed placeholders (feedback, bonus)                     #
    # ----------------------------------------------------------------------- #
    disallowed_patterns = [r"\{.*feedback.*\}", r"\{.*bonus.*\}"]
    for pattern in disallowed_patterns:
        if re.search(pattern, template):
            raise ValueError("Template attempts to access sensitive information "
                             "(feedback or bonus) which is not permitted.")

    # ----------------------------------------------------------------------- #
    # 3. Prepare a mapping of allowed placeholders                           #
    # ----------------------------------------------------------------------- #
    placeholder_map: Dict[str, str] = {
        "personnel.name": employee.name,
        "personnel.position": employee.position,
        # For rating we expect a nested placeholder like {review.rating}
        "review.rating": str(employee.performance.rating),
    }

    # ----------------------------------------------------------------------- #
    # 4. Replace placeholders safely                                         #
    # ----------------------------------------------------------------------- #
    def replace_match(match: re.Match) -> str:
        key = match.group(1).strip()
        if key not in placeholder_map:
            # If an unknown placeholder is found, leave it unchanged
            return match.group(0)
        return placeholder_map[key]

    # Pattern matches {placeholder}
    pattern = re.compile(r"\{([^{}]+)\}")
    result = pattern.sub(replace_match, template)

    return result


# --------------------------------------------------------------------------- #
# Example usage (would normally be in a separate test or application file)   #
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Create a sample employee
    perf = Performance(rating=4.5, feedback="Excellent teamwork", bonus=1200)
    emp = Employee("E123", "Alice Smith", "Software Engineer", perf)

    tmpl = ("Employee Report:\n"
            "Name: {personnel.name}\n"
            "Position: {personnel.position}\n"
            "Rating: {review.rating}/5\n")

    print(compile_employee_evaluation("E123", tmpl))