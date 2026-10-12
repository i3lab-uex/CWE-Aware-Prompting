import html

# A simple HTML template for the forum post. The placeholders are replaced with escaped content.
FORUM_POST_FORMAT = """
<article class="forum-post">
    <header><h2>{title}</h2></header>
    <section class="content">{body}</section>
    <aside class="discussion-points">
        <h3>Discussion Points</h3>
        {points}
    </aside>
</article>
"""

def create_forum_post(topic: str, text_body: str, points: list[str]) -> str:
    """
    Construct a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic : str
        The title or main topic of the forum post.
    text_body : str
        The main body or content of the forum post.
    points : list[str]
        A collection of user‑provided discussion points or options in markdown format.

    Returns
    -------
    str
        The fully formatted and sanitized HTML representation of the forum post.
    """
    # Basic validation and type coercion
    if topic is None:
        topic = ""
    if text_body is None:
        text_body = ""

    # Escape user supplied strings to prevent HTML injection
    escaped_title = html.escape(str(topic), quote=True)
    escaped_body = html.escape(str(text_body), quote=True)

    # Build the list of discussion points, escaping each entry
    if not isinstance(points, (list, tuple)):
        points = []

    list_items = []
    for point in points:
        # Ensure the point is a string and escape it
        safe_point = html.escape(str(point), quote=True)
        list_items.append(f"<li>{safe_point}</li>")

    # If no points are provided, we still include an empty list to keep structure
    if not list_items:
        points_html = "<ul></ul>"
    else:
        points_html = f"<ul>{''.join(list_items)}</ul>"

    # Construct the final HTML using the template
    formatted_post = FORUM_POST_FORMAT.format(
        title=escaped_title,
        body=escaped_body,
        points=points_html
    )

    return formatted_post.strip()