import re

def match_strings(text: str):
    """
    Return a tuple containing the text outside parentheses and the text inside
    parentheses from an input string of the form 'outside(in)'. If the pattern
    does not match, return None. No exceptions are raised.

    Parameters
    ----------
    text : str
        The input string to be matched.

    Returns
    -------
    tuple[str, str] | None
        A two‑element tuple (outside_text, inside_text) if the pattern matches,
        otherwise None.
    """
    try:
        # The regex captures everything before the first '(' and everything
        # inside the parentheses until the last ')'.
        pattern = r'^(.*?)\((.*?)\)$'
        match = re.match(pattern, text)
        if match:
            return match.group(1), match.group(2)
    except Exception:
        # Silently ignore any unexpected errors (e.g., invalid regex, bad input)
        pass
    return None