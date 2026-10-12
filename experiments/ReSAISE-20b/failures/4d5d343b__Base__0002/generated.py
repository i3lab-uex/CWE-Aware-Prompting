import re
from typing import List

# Pre-compiled, non-greedy regex to match simple HTML tags.
# It matches an opening '<', followed by any characters that are not '>' (non-greedy),
# and then a closing '>'. This avoids catastrophic backtracking.
_TAG_REGEX = re.compile(r'<[^>]+?>')

def grab_html_tags(html_code: str) -> List[str]:
    """
    Scan the provided HTML string and return a list of all detected tags.

    Parameters
    ----------
    html_code : str
        The input HTML string to parse.

    Returns
    -------
    List[str]
        A list of all tag substrings found in the input.  The order
        corresponds to their appearance in the original string.
    """
    # Guard against non-string input by converting to str (fails silently).
    try:
        if not isinstance(html_code, str):
            html_code = str(html_code)
    except Exception:
        # If conversion fails, return empty list to avoid raising.
        return []

    # Find all non-overlapping matches of the tag pattern.
    tags = _TAG_REGEX.findall(html_code)

    # Return a copy to avoid accidental external mutation.
    return list(tags)