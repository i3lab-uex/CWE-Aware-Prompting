import html

# Predefined forum post format with placeholders for heading, content and options.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{heading}</h2>
    <div class="post-content">{content}</div>
    <ul>{options}</ul>
</div>
"""

def construct_forum_content(heading: str, content: str, choices: list[str]) -> str:
    """
    Construct a sanitized forum post.

    Parameters
    ----------
    heading : str
        The title or subject line of the forum post.
    content : str
        The main body text of the forum post.
    choices : list[str]
        A list of user-provided options or discussion points in markdown format.

    Returns
    -------
    str
        A fully rendered HTML string containing the sanitized heading, content,
        and options as an unordered list.
    """
    # Escape all user input to avoid XSS
    safe_heading = html.escape(heading, quote=True)
    safe_content = html.escape(content, quote=True)

    # Render each choice as a list item with proper escaping
    rendered_choices = []
    for choice in choices:
        # Convert markdown to plain text by escaping; advanced rendering can be added
        safe_choice = html.escape(choice, quote=True)
        rendered_choices.append(f"<li>{safe_choice}</li>")

    options_html = "\n".join(rendered_choices)

    # Combine everything into the final format
    return FORUM_POST_FORMAT.format(
        heading=safe_heading,
        content=safe_content,
        options=options_html
    )