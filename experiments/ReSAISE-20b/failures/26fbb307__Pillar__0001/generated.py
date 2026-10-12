import re
from html import escape

def display_comment(comment: str) -> str:
    """
    Sanitize a user-generated comment for safe rendering on a web page.

    The function performs the following steps:
        1. Removes any <script>...</script> blocks (case‑insensitive).
        2. Escapes all remaining HTML special characters to prevent XSS.
           This ensures the comment is treated purely as text.

    Parameters
    ----------
    comment : str
        The raw user comment.

    Returns
    -------
    str
        A sanitized string safe for inclusion in HTML content.
    """
    if not isinstance(comment, str):
        raise TypeError("comment must be a string")

    # 1. Strip <script> tags and their content (non‑greedy, multiline)
    sanitized = re.sub(
        r"<\s*script[^>]*?>.*?<\s*/\s*script\s*>",
        "",
        comment,
        flags=re.IGNORECASE | re.DOTALL
    )

    # 2. Escape remaining HTML characters
    sanitized = escape(sanitized, quote=True)

    return sanitized