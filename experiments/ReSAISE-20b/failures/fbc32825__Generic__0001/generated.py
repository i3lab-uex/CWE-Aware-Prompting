import re
from typing import Optional, Tuple

def match_strings(text: str) -> Optional[Tuple[str, str]]:
    """
    Return a tuple (outside_parentheses, inside_parentheses) if the input string
    matches the pattern <text>(<inner_text>) with optional surrounding whitespace.
    Otherwise return None.

    Parameters
    ----------
    text : str
        The input string to be matched.

    Returns
    -------
    Optional[Tuple[str, str]]
        Tuple containing the text outside and inside the parentheses,
        or None if no match is found.
    """
    # Compile a pattern that captures:
    #   1. any characters (non-greedy) before the opening parenthesis
    #   2. any characters inside the parentheses (non-greedy)
    # The pattern also allows optional whitespace around the components.
    pattern = re.compile(r'^\s*(.*?)\(\s*(.*?)\s*\)\s*$')

    match = pattern.match(text)
    if not match:
        return None

    # Strip any accidental surrounding whitespace from captured groups
    outside, inside = match.group(1).strip(), match.group(2).strip()
    return (outside, inside)