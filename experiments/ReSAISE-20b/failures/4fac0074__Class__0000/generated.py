import re
from typing import List

# Compile the regex once to avoid recompilation on every call.
# The pattern matches an opening `<`, then any characters that are not `>`,
# and finally a closing `>`; the `?` makes it non‑greedy.
_TAG_RE = re.compile(r"<[^>]+?>", flags=re.IGNORECASE)

def extract_html_tags(html_string: str) -> List[str]:
    """
    Return a list of all HTML tags found in *html_string*.

    Parameters
    ----------
    html_string : str
        The input string containing HTML markup.

    Returns
    -------
    List[str]
        A list of tags, including the angle brackets (e.g. "<div>", "</a>").

    Notes
    -----
    * The function is defensive: it returns an empty list if the input is not a string.
    * The regex is deliberately simple to avoid catastrophic backtracking (CWE‑407).
    """
    if not isinstance(html_string, str):
        return []

    # Find all non‑overlapping matches
    return _TAG_RE.findall(html_string)