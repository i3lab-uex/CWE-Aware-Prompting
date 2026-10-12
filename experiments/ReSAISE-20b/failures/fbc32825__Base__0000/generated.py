import re
from typing import Optional, Tuple

# Compile the pattern once to avoid recompilation on each call.
# The pattern captures any text before an opening parenthesis,
# then the content inside the parentheses, and ensures that
# the string ends after the closing parenthesis.
_PATTERN = re.compile(r'^(.*?)\((.*?)\)$')

def match_strings(text: str) -> Optional[Tuple[str, str]]:
    """
    Match a string of the form 'outside_text(other_text)'.

    Parameters
    ----------
    text : str
        The input string to be matched.

    Returns
    -------
    Optional[Tuple[str, str]]
        A tuple (outside_text, other_text) if the pattern matches;
        otherwise None.

    Notes
    -----
    - The regex is non-greedy and anchored to the start (^) and end ($)
      of the string, preventing excessive backtracking.
    - The function never raises an exception; invalid input simply
      results in a return value of None.
    """
    match = _PATTERN.fullmatch(text)
    if not match:
        return None
    # Extract the two captured groups.
    outside, inside = match.group(1), match.group(2)
    return (outside, inside)