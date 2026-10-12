import html

# Template used to render the forum post.  The placeholders are replaced with
# escaped user content before being sent to the browser.
FORUM_POST_FORMAT = """
<h2>{header}</h2>
<p>{message}</p>
{options_html}
"""

def generate_forum_post(header: str, message: str, options: list[str]) -> str:
    """
    Create a sanitized HTML representation of a forum post.

    Parameters
    ----------
    header : str
        The title or heading the user has supplied.
    message : str
        The main body of the post.
    options : list[str]
        A list of strings (markdown formatted) that represent discussion
        options.  Each option will be rendered as a list item.

    Returns
    -------
    str
        A fully escaped HTML snippet that can safely be embedded in a page.

    Notes
    -----
    The function uses :func:`html.escape` to neutralise any characters that
    could form HTML tags or JavaScript.  This protects against CWE‑79
    (Cross‑Site Scripting).  No external libraries are required.
    """
    # Escape the header and message to prevent injection of tags or scripts
    safe_header = html.escape(header, quote=True)
    safe_message = html.escape(message, quote=True)

    # Build the options list.  Each option is escaped individually.
    if options:
        list_items = []
        for opt in options:
            safe_opt = html.escape(opt, quote=True)
            list_items.append(f"<li>{safe_opt}</li>")
        options_html = "<ul>\n" + "\n".join(list_items) + "\n</ul>"
    else:
        options_html = ""

    # Combine everything using the template
    return FORUM_POST_FORMAT.format(
        header=safe_header,
        message=safe_message,
        options_html=options_html
    )