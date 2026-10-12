import html

# A simple template for the forum post.
FORUM_POST_FORMAT = (
    "<h1>{header}</h1>\n"
    "<div class=\"post-body\">{message}</div>\n"
    "<ul>{options}</ul>"
)

def construct_forum_content(heading: str, content: str, choices: list[str]) -> str:
    """
    Construct a safe, formatted forum post.

    Parameters
    ----------
    heading : str
        The title or subject line of the forum post.
    content : str
        The main body text of the forum post.
    choices : list[str]
        A collection of user‑provided options or discussion points
        in markdown format.  The function will escape any HTML
        characters and render each item as a list element.

    Returns
    -------
    str
        The sanitized forum post ready for rendering in a browser.

    Notes
    -----
    - All user input is escaped using `html.escape` to prevent
      injection of HTML or JavaScript.
    - The function does not perform full Markdown parsing; it simply
      escapes the text and places each choice in an <li> element.
    """
    # Escape heading and content to neutralize special characters
    safe_heading = html.escape(heading, quote=True)
    safe_content = html.escape(content, quote=True)

    # Render each choice as a list item, escaping any special characters
    rendered_choices = []
    for choice in choices:
        escaped_choice = html.escape(choice, quote=True)
        rendered_choices.append(f"<li>{escaped_choice}</li>")

    options_html = "\n".join(rendered_choices)

    # Populate the template
    forum_post = FORUM_POST_FORMAT.format(
        header=safe_heading,
        message=safe_content,
        options=options_html
    )
    return forum_post