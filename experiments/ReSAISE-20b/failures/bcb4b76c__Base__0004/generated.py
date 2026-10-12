import html

# Predefined HTML template for a forum post.
FORUM_POST_FORMAT = """
<article class="forum-post">
    <header>
        <h1>{title}</h1>
    </header>
    <section class="content">
        {body}
    </section>
    <footer class="discussion-points">
        <h2>Discussion Points</h2>
        {points}
    </footer>
</article>
"""

def create_forum_post(topic: str, text_body: str, points: list[str]) -> str:
    """
    Create a sanitized HTML representation of a forum post.

    Args:
        topic (str): The title or main topic of the forum post.
        text_body (str): The main body or content of the forum post.
        points (list[str]): A collection of user-provided discussion points
                            or options in markdown format.

    Returns:
        str: Fully formatted and sanitized HTML string for the forum post.
    """
    # Escape user-provided strings to prevent XSS
    safe_title = html.escape(topic, quote=True)
    safe_body = html.escape(text_body, quote=True)

    # Convert markdown points to sanitized <li> elements
    safe_points = []
    for point in points:
        # Escape the point text and then wrap it in <li>
        escaped_point = html.escape(point, quote=True)
        safe_points.append(f"<li>{escaped_point}</li>")

    # Join the list items into a single string
    points_html = "<ul>\n" + "\n".join(safe_points) + "\n</ul>"

    # Format the final HTML using the predefined template
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )