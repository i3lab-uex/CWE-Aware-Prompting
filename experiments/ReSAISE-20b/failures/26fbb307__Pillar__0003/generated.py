import html
import re

def display_comment(comment: str) -> str:
    """
    Sanitise a user‑generated comment for safe display in an HTML context.

    The function performs the following steps:
        1. Removes any <script> tags and their content.
        2. Escapes all remaining HTML special characters to prevent XSS.
        3. Trims leading/trailing whitespace.

    Parameters
    ----------
    comment : str
        The raw user comment.

    Returns
    -------
    str
        A safe, sanitized string ready to be inserted into an HTML page.

    Raises
    ------
    TypeError
        If `comment` is not a string.
    """
    if not isinstance(comment, str):
        raise TypeError("comment must be a string")

    # 1. Remove <script> tags (case‑insensitive) and any content until the next </script>
    #    The regex is non‑greedy to avoid over‑matching.
    script_pattern = re.compile(r'<\s*script\b[^>]*?>.*?<\s*/\s*script\s*>',
                                flags=re.IGNORECASE | re.DOTALL)
    cleaned = script_pattern.sub('', comment)

    # 2. Escape all remaining HTML special characters
    escaped = html.escape(cleaned, quote=True)

    # 3. Trim whitespace to avoid accidental formatting issues
    return escaped.strip()