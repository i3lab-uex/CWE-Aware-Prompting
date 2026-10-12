import html

# Default template for a forum post.
FORUM_POST_FORMAT = """
<h2>{header}</h2>
<p>{message}</p>
{options_block}
"""

def generate_forum_post(header: str, message: str, options: list[str]) -> str:
    """
    Render a forum post from user supplied header, message and options.
    
    Parameters
    ----------
    header : str
        The title of the forum post.
    message : str
        Body text of the post.
    options : list[str]
        List of discussion options in markdown format.
    
    Returns
    -------
    str
        A sanitized HTML string representing the forum post.
    """
    # Sanitize header and message to avoid XSS
    safe_header = html.escape(header, quote=True)
    safe_message = html.escape(message, quote=True)

    # Build unordered list of options
    if options:
        sanitized_options = []
        for opt in options:
            # Escape each option
            escaped_opt = html.escape(opt, quote=True)
            sanitized_options.append(f"<li>{escaped_opt}</li>")
        options_block = f"<ul>\n{''.join(sanitized_options)}\n</ul>"
    else:
        options_block = ""

    # Format the final post
    return FORUM_POST_FORMAT.format(
        header=safe_header,
        message=safe_message,
        options_block=options_block
    )