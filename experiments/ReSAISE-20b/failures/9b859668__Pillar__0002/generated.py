import html

# Predefined template for a forum post.  Placeholders are {header}, {body} and {options}.
FORUM_POST_FORMAT = (
    "<div class='forum-post'>\n"
    "  <h2>{header}</h2>\n"
    "  <div class='post-body'>{body}</div>\n"
    "  {options}\n"
    "</div>"
)

def construct_forum_content(heading: str, content: str, choices: list[str]) -> str:
    """
    Construct a safe and formatted forum post.

    Parameters
    ----------
    heading : str
        The title or subject line of the forum post.
    content : str
        The main body text of the forum post.
    choices : list[str]
        A collection of user‑provided options or discussion points in markdown format.

    Returns
    -------
    str
        A sanitized HTML string containing the header, body, and options rendered as an unordered list.

    Raises
    ------
    TypeError
        If any argument is of an unexpected type.
    """
    # Validate input types
    if not isinstance(heading, str):
        raise TypeError("heading must be a string")
    if not isinstance(content, str):
        raise TypeError("content must be a string")
    if not isinstance(choices, list) or not all(isinstance(c, str) for c in choices):
        raise TypeError("choices must be a list of strings")

    # Escape all user supplied content to prevent XSS
    safe_heading = html.escape(heading, quote=True)
    safe_content = html.escape(content, quote=True)

    # Build the options list
    if choices:
        li_items = "\n".join(f"      <li>{html.escape(choice, quote=True)}</li>" for choice in choices)
        options_html = f"  <ul>\n{li_items}\n    </ul>"
    else:
        options_html = ""

    # Format the final output
    forum_post = FORUM_POST_FORMAT.format(
        header=safe_heading,
        body=safe_content,
        options=options_html
    )

    return forum_post