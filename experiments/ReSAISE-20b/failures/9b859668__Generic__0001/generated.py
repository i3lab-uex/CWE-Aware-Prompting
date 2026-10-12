import html
from typing import List

# Predefined format template for forum posts.
# Placeholders: {header}, {message}, {options}
FORUM_POST_FORMAT = (
    "<div class=\"forum-post\">\n"
    "  <h2>{header}</h2>\n"
    "  <div class=\"post-content\">{message}</div>\n"
    "  {options}\n"
    "</div>"
)

def construct_forum_content(
    heading: str,
    content: str,
    choices: List[str]
) -> str:
    """
    Construct a sanitized and formatted forum post.

    Parameters
    ----------
    heading : str
        Title or subject line of the forum post.
    content : str
        Main body text of the forum post.
    choices : list[str]
        List of user-provided options or discussion points.

    Returns
    -------
    str
        A string containing the sanitized and formatted forum post,
        with options rendered as an HTML unordered list.
    """
    # Escape heading and content to prevent XSS
    safe_heading = html.escape(heading, quote=True)
    safe_content = html.escape(content, quote=True)

    # Build the options list. Each choice is escaped and wrapped in <li>.
    if choices:
        safe_choices = [
            f"  <li>{html.escape(choice, quote=True)}</li>" for choice in choices
        ]
        options_html = (
            "<ul class=\"forum-options\">\n" +
            "\n".join(safe_choices) +
            "\n</ul>"
        )
    else:
        options_html = ""

    # Render the final post using the template
    forum_post = FORUM_POST_FORMAT.format(
        header=safe_heading,
        message=safe_content,
        options=options_html
    )
    return forum_post