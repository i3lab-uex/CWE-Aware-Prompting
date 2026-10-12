import html
from typing import List

# Template used to format a forum post.
FORUM_POST_FORMAT = """
<h1>{header}</h1>
<p>{message}</p>
{options}
"""

def _escape_html(text: str) -> str:
    """
    Escape HTML special characters to prevent XSS.
    """
    return html.escape(text, quote=True)

def generate_forum_post(header: str, message: str, options: List[str]) -> str:
    """
    Generate a sanitized forum post from user input.

    Parameters
    ----------
    header : str
        The title of the forum post.
    message : str
        The body text of the post.
    options : List[str]
        A list of user‑submitted options (in markdown format).

    Returns
    -------
    str
        A sanitized HTML string representing the forum post.

    Raises
    ------
    ValueError
        If any argument is not of the expected type.
    """
    # Basic type checking
    if not isinstance(header, str):
        raise ValueError("header must be a string")
    if not isinstance(message, str):
        raise ValueError("message must be a string")
    if not isinstance(options, list) or not all(isinstance(opt, str) for opt in options):
        raise ValueError("options must be a list of strings")

    # Escape all user supplied content
    safe_header = _escape_html(header)
    safe_message = _escape_html(message)

    # Build the options list as an unordered list
    if options:
        safe_options_items = [
            f"<li>{_escape_html(opt)}</li>" for opt in options
        ]
        safe_options = "<ul>\n" + "\n".join(safe_options_items) + "\n</ul>"
    else:
        safe_options = ""

    # Format the final post
    return FORUM_POST_FORMAT.format(
        header=safe_header,
        message=safe_message,
        options=safe_options
    ).strip()