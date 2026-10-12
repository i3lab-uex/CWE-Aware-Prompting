import html

# Example forum post template with placeholders for title, body and discussion points.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
    <ul class="discussion-points">{points}</ul>
</div>
"""

def build_post_html(topic_title: str, body_text: str, list_items: list[str]) -> str:
    """
    Create a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic_title : str
        The title or main topic of the forum post.
    body_text : str
        The main content/body of the forum post.
    list_items : list[str]
        A collection of discussion points or options in markdown format.

    Returns
    -------
    str
        The fully formatted and sanitized HTML representation of the forum post.
    """
    # Escape all user-supplied content to prevent XSS / injection
    safe_title = html.escape(topic_title, quote=True)
    safe_body = html.escape(body_text, quote=True)

    # Build the list of discussion points as <li> elements.
    safe_list_items = []
    for item in list_items:
        # Escape the content of each list item
        safe_item = html.escape(item, quote=True)
        # Preserve simple markdown by converting a leading '-' or '*' into a list item
        safe_list_items.append(f"<li>{safe_item}</li>")

    points_html = "\n".join(safe_list_items)

    # Populate the template
    post_html = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )

    return post_html.strip()