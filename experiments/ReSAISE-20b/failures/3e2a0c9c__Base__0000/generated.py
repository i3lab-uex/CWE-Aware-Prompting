import html

# Predefined HTML template for forum posts.
# It contains three placeholders:
#   {title}      – the title of the post
#   {body}       – the main body content
#   {points}     – an unordered list of discussion points
FORUM_POST_FORMAT = """
<article class="forum-post">
    <h1>{title}</h1>
    <section class="post-body">{body}</section>
    <nav class="discussion-points">{points}</nav>
</article>
"""

def build_post_html(topic_title: str, body_text: str, list_items: list[str]) -> str:
    """
    Create a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic_title : str
        The title or main topic of the forum post.
    body_text : str
        The main body content of the forum post.
    list_items : list[str]
        A collection of user‑provided discussion points or options in markdown
        format.

    Returns
    -------
    str
        A string containing the fully formatted and sanitized HTML representation
        of the forum post, including the header, message body, and safely rendered
        discussion points.

    Raises
    ------
    TypeError
        If any of the arguments is not of the expected type.
    """
    # Input validation
    if not isinstance(topic_title, str):
        raise TypeError("topic_title must be a string")
    if not isinstance(body_text, str):
        raise TypeError("body_text must be a string")
    if not isinstance(list_items, list) or not all(isinstance(item, str) for item in list_items):
        raise TypeError("list_items must be a list of strings")

    # Sanitize user input to prevent XSS
    safe_title = html.escape(topic_title, quote=True)
    safe_body = html.escape(body_text, quote=True)

    # Render the list items as an unordered list.
    # Each item is escaped; markdown formatting is not parsed to avoid
    # unintended HTML injection.  For simplicity we keep the raw text.
    if list_items:
        safe_points = "<ul>\n" + "\n".join(f"<li>{html.escape(item, quote=True)}</li>" for item in list_items) + "\n</ul>"
    else:
        safe_points = "<!-- No discussion points -->"

    # Format the final HTML using the template
    html_output = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=safe_points
    )
    return html_output.strip()