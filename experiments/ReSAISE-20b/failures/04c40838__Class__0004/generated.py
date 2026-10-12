import html

# Template for a forum post with placeholders for header, message and options.
FORUM_POST_FORMAT = """
<h2>{header}</h2>
<div class="post-body">{message}</div>
{options_html}
"""

def generate_forum_post(header: str, message: str, options: list[str]) -> str:
    """
    Generate a sanitized forum post.

    Parameters
    ----------
    header : str
        The user-written title for the post.
    message : str
        The body of text in the post.
    options : list[str]
        A list of user-submitted options (in markdown format) for the discussion forum thread.

    Returns
    -------
    str
        A sanitized HTML string containing the header, message and options.
    """
    # Escape special characters to prevent XSS or injection attacks
    safe_header = html.escape(header, quote=True)
    safe_message = html.escape(message, quote=True)

    # Build the options HTML if any
    if options:
        safe_options = []
        for opt in options:
            # Escape each option
            escaped_opt = html.escape(opt, quote=True)
            safe_options.append(f"<li>{escaped_opt}</li>")
        options_html = "<ul>\n" + "\n".join(safe_options) + "\n</ul>"
    else:
        options_html = ""

    # Return the formatted post
    return FORUM_POST_FORMAT.format(
        header=safe_header,
        message=safe_message,
        options_html=options_html
    )