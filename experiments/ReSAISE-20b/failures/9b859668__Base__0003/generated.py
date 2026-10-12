import html

# Predefined template for a forum post.
FORUM_POST_FORMAT = """<div class="forum-post">
  <h1>{header}</h1>
  <div class="post-content">{message}</div>
  {options}
</div>"""

def construct_forum_content(heading: str, content: str, choices: list[str]) -> str:
    """
    Construct a sanitized and formatted forum post.

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
        A string containing the sanitized and formatted forum post.
    """
    # Escape any HTML characters in user input to prevent XSS
    safe_heading = html.escape(heading, quote=True)
    safe_content = html.escape(content, quote=True)

    # Convert each choice to a list item with escaped content
    if choices:
        safe_choices = []
        for idx, choice in enumerate(choices):
            # Escape the markdown content; we are not rendering markdown,
            # only ensuring no raw HTML is injected.
            escaped_choice = html.escape(choice, quote=True)
            safe_choices.append(f'  <li>{escaped_choice}</li>')
        options_html = "<ul>\n" + "\n".join(safe_choices) + "\n</ul>"
    else:
        options_html = ""

    # Format the final post using the predefined template
    return FORUM_POST_FORMAT.format(
        header=safe_heading,
        message=safe_content,
        options=options_html
    )