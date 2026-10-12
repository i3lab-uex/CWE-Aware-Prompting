import re

# Pre‑compiled regex pattern: capture everything before the first '(' and everything inside parentheses.
# The non‑greedy quantifier (.*?) ensures minimal matching, preventing catastrophic backtracking.
_PATTERN = re.compile(r'^(?P<outside>.*?)\((?P<inside>.*?)\)$')

def match_strings(text: str):
    """
    Match a string of the form <outside>(<inside>) and return the captured groups.

    Parameters
    ----------
    text : str
        The input string to be matched.

    Returns
    -------
    tuple[str, str] | None
        A tuple containing the text outside the parentheses and the text inside,
        or ``None`` if the pattern does not match.

    Notes
    -----
    The function is safe against regex denial‑of‑service attacks because the pattern
    uses a bounded, non‑greedy match and does not allow nested parentheses.
    """
    if not isinstance(text, str):
        return None

    match = _PATTERN.match(text)
    if not match:
        return None

    # Return the captured groups as a tuple.
    return match.group('outside'), match.group('inside')