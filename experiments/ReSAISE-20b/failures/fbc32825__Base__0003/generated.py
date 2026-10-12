import re

# Compile a safe, non‑greedy pattern that matches exactly one pair of parentheses.
# The outer group captures all characters up to the first '('.
# The inner group captures any characters that are not parentheses inside the pair.
_PATTERN = re.compile(r'^([^()]+)\(([^()]*)\)$')

def match_strings(text: str):
    """
    Match a string of the form <outside>(<inside>) and return the two parts.

    Parameters
    ----------
    text : str
        Input string to be matched.

    Returns
    -------
    tuple[str, str] | None
        A tuple containing the text outside the parentheses and the text inside,
        or ``None`` if no match is found.
    """
    # Avoid raising exceptions; simply return None on failure.
    m = _pattern.match(text)
    if not m:
        return None
    # Return a copy of the matched groups to avoid accidental mutation.
    return m.group(1), m.group(2)