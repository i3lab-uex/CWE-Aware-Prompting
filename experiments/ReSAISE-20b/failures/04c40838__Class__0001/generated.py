import html
from typing import List

# Template for the forum post.  The placeholders are replaced with escaped content.
FORUM_POST_FORMAT = """
<h2>{header}</h2>
<p>{message}</p>
{options_html}
"""

def generate_forum_post(header: str, message: str, options: List[str]) -> str:
    """
    Generate a sanitized forum post.

    Parameters
    ----------
    header : str
        The title of the post.
    message : str
        The body text of the post.
    options : List[str]
        A list of user‑supplied markdown strings for discussion options.

    Returns
    -------
    str
        A string containing the sanitized forum post ready for HTML rendering.
    """
    # Escape header and message to prevent injection of arbitrary HTML or scripts
    safe_header = html.escape(header, quote=True)
    safe_message = html.escape(message, quote=True)

    # Build a sanitized unordered list of options
    if options:
        safe_options = []
        for opt in options:
            # Escape each option string; markdown is left intact but any HTML tags are neutralised
            escaped_opt = html.escape(opt, quote=True)
            safe_options.append(f"  <li>{escaped_opt}</li>")
        options_html = "<ul>\n" + "\n".join(safe_options) + "\n</ul>"
    else:
        options_html = ""

    # Format the final post
    return FORUM_POST_FORMAT.format(
        header=safe_header,
        message=safe_message,
        options_html=options_html
    )