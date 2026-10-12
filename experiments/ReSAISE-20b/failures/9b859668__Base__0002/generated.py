import html

# A simple template for a forum post.
FORUM_POST_FORMAT = """<h1>{header}</h1>
<p>{message}</p>
<ul>{options}</ul>"""

def construct_forum_content(heading: str, content: str, choices: list[str]) -> str:
    """
    Construct a forum post with safe HTML output.

    Parameters
    ----------
    heading : str
        The title or subject line of the forum post.
    content : str
        The main body text of the forum post.
    choices : list[str]
        A list of user‑provided options or discussion points in markdown format.

    Returns
    -------
    str
        A sanitized and formatted forum post string containing a header, message,
        and an unordered list of options.

    Notes
    -----
    All user‑supplied data is escaped with ``html.escape`` to mitigate XSS
    (CWE-79). Markdown content is not rendered; it is treated as plain text.
    """
    # Escape all user input to avoid injection
    safe_header = html.escape(heading, quote=True)
    safe_message = html.escape(content, quote=True)

    # Build the list items
    list_items = []
    for choice in choices:
        escaped_choice = html.escape(choice, quote=True)
        list_items.append(f"<li>{escaped_choice}</li>")

    safe_options = "\n".join(list_items)

    # Format the final output
    return FORUM_POST_FORMAT.format(
        header=safe_header,
        message=safe_message,
        options=safe_options
    )