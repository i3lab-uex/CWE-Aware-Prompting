import re

# Regular expression that captures:
#   1. any characters except parentheses before the first '('
#   2. any characters (including none) inside a single pair of parentheses
# The pattern is anchored to the start and end of the string to avoid accidental partial matches.
_PATTERN = re.compile(r'^(?P<outside>[^()]+)\((?P<inside>[^()]*)\)$')


def match_strings(text: str):
    """
    Match a string of the form <outside>(<inside>) and return a tuple
    containing the parts outside and inside the parentheses.

    Parameters:
        text (str): The input string to be matched.

    Returns:
        tuple[str, str] | None: A 2‑tuple (outside, inside) if the pattern matches,
        otherwise None.

    The function never raises an exception; any invalid input simply results in
    a return value of None.
    """
    if not isinstance(text, str):
        # Defensive check: non‑string input cannot match the pattern.
        return None

    m = _PATTEN.match(text)
    if not m:
        return None
    return m.group('outside'), m.group('inside')