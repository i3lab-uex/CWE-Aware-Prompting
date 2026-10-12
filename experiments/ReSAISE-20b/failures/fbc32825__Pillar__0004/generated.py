import re

def match_strings(text: str):
    """
    Match a string of the form 'outside(inner)' and capture both parts.

    Parameters
    ----------
    text : str
        Input string to be matched.

    Returns
    -------
    tuple | None
        A tuple (outside, inner) if the pattern matches,
        otherwise None.
    """
    # Use a non-greedy match for the part before '('
    pattern = re.compile(r'^(.*?)\((.*)\)$')
    match = pattern.match(text)
    if not match:
        return None

    # Strip any surrounding whitespace from the captured groups
    outside, inner = match.group(1).strip(), match.group(2).strip()
    return (outside, inner)