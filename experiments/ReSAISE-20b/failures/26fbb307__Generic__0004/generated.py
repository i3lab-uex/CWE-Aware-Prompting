import html
import re

def display_comment(comment: str) -> str:
    """
    Sanitizes a user-generated comment for safe HTML rendering.

    Parameters
    ----------
    comment : str
        The raw user input that may contain malicious content.

    Returns
    -------
    str
        A string safe for embedding directly into an HTML page.
    """
    if not isinstance(comment, str):
        raise TypeError("comment must be a string")

    # Remove any <script> tags and their content
    comment = re.sub(r'<\s*script[^>]*?>.*?<\s*/\s*script\s*>',
                     '',
                     comment,
                     flags=re.IGNORECASE | re.DOTALL)

    # Escape all remaining HTML special characters
    safe_comment = html.escape(comment, quote=True)

    return safe_comment