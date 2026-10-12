import re
from typing import Optional, Tuple

# Compile the regex once for efficiency. It captures everything before the first '('
# and everything inside the parentheses until the last ')'.
_PATTERN = re.compile(r'^(?P<outside>.*?)\((?P<inside>.*)\)$')

def match_strings(text: str) -> Optional[Tuple[str, str]]:
    """
    Match a string of the form <outside>(<inside>) and return a tuple
    containing the parts outside and inside the parentheses.

    Parameters
    ----------
    text : str
        The input string to be matched.

    Returns
    -------
    Optional[Tuple[str, str]]
        A tuple (outside, inside) if the pattern matches; otherwise None.
    """
    match = _PATTERN.match(text)
    if not match:
        return None

    # Strip any surrounding whitespace from the captured groups
    outside = match.group('outside').strip()
    inside = match.group('inside').strip()

    return outside, inside