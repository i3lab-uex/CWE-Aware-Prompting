import html

# Predefined HTML template for a forum post.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  {points_section}
</div>
"""

def create_forum_post(topic: str, text_body: str, points: list[str]) -> str:
    """
    Create a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic : str
        The title or main topic of the forum post.
    text_body : str
        The main body or content of the forum post.
    points : list[str]
        A collection of user‑provided discussion points or options
        in markdown format.

    Returns
    -------
    str
        A string containing the fully formatted and sanitized HTML
        representation of the forum post.
    """
    # Sanitize title and body to prevent injection (CWE‑74).
    safe_title = html.escape(topic, quote=True)
    safe_body = html.escape(text_body, quote=True)

    # Build the unordered list of points if any.
    if points:
        list_items = []
        for point in points:
            # Escape each point to neutralize HTML special characters.
            safe_point = html.escape(point, quote=True)
            list_items.append(f"<li>{safe_point}</li>")
        points_section = f"<ul>\n{''.join(list_items)}\n</ul>"
    else:
        points_section = ""

    # Format the final HTML using the predefined template.
    formatted_post = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points_section=points_section
    )
    return formatted_post.strip()