import html

# Predefined format template with placeholders for header, body and options.
FORUM_POST_FORMAT = """
<h2>{header}</h2>
<p>{body}</p>
{options}
"""

def construct_forum_content(heading: str, content: str, choices: list[str]) -> str:
    """
    Construct a sanitized forum post with an HTML unordered list of options.

    Parameters
    ----------
    heading : str
        The title or subject line of the forum post.
    content : str
        The main body text of the forum post.
    choices : list[str]
        A collection of user-provided options or discussion points in markdown format.

    Returns
    -------
    str
        A string containing the sanitized and formatted forum post, including a header,
        message body, and an unordered list of options.

    Raises
    ------
    ValueError
        If any of the arguments are not of the expected type.
    """
    # Validate argument types
    if not isinstance(heading, str):
        raise ValueError("`heading` must be a string")
    if not isinstance(content, str):
        raise ValueError("`content` must be a string")
    if not isinstance(choices, list) or not all(isinstance(c, str) for c in choices):
        raise ValueError("`choices` must be a list of strings")

    # Escape any HTML special characters to avoid injection
    safe_heading = html.escape(heading, quote=True)
    safe_content = html.escape(content, quote=True)

    # Build the unordered list of options
    if choices:
        list_items = "\n".join(f"  <li>{html.escape(choice, quote=True)}</li>" for choice in choices)
        options_html = f"<ul>\n{list_items}\n</ul>"
    else:
        options_html = ""

    # Format the final post
    forum_post = FORUM_POST_FORMAT.format(
        header=safe_heading,
        body=safe_content,
        options=options_html
    ).strip()

    return forum_post