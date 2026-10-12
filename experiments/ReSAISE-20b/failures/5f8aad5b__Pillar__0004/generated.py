import re
from typing import List

# Compile the regex once at module load time to avoid recompilation on every call.
_TAG_RE = re.compile(r'<[^>]+>', flags=re.IGNORECASE | re.DOTALL)


def extract_html_tags(html_content: str) -> List[str]:
    """
    Extract all HTML tags from the provided string.

    Parameters
    ----------
    html_content : str
        A string containing HTML markup.

    Returns
    -------
    List[str]
        A list of all tags found in the input string, including angle brackets.
        The order is preserved as they appear in the input.

    Notes
    -----
    * This function does **not** raise exceptions for malformed input.
      If ``html_content`` is not a string, it will be coerced to ``str``
      and the regex will simply return an empty list.
    * The regular expression is intentionally simple to avoid
      excessive backtracking and potential denial‑of‑service attacks.
    """
    if not isinstance(html_content, str):
        # Coerce to string; any non‑string input results in an empty list.
        try:
            html_content = str(html_content)
        except Exception:  # pragma: no cover
            return []

    try:
        tags = _TAG_RE.findall(html_content)
    except re.error:  # pragma: no cover
        # In the unlikely event that the regex engine fails, return empty list.
        tags = []

    return tags