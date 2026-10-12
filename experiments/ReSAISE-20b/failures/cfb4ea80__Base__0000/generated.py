import html

# Predefined HTML template for a forum post.
# The placeholders {title}, {body} and {points} will be replaced
# with the sanitized content.
FORUM_POST_FORMAT = """
<article class="forum-post">
  <header>
    <h1>{title}</h1>
  </header>
  <section class="post-body">
    {body}
  </section>
  <aside class="discussion-points">
    <h2>Discussion Points</h2>
    <ul>
      {points}
    </ul>
  </aside>
</article>
"""

def create_forum_entry(title: str, body: str, points: list[str]) -> str:
    """
    Assemble a sanitized forum post from user supplied content.

    Parameters
    ----------
    title : str
        The title or main topic of the forum post.
    body : str
        The primary content or body text of the post.
    points : list[str]
        A series of user-supplied discussion points or options in markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized forum post ready for HTML rendering.
    """
    # Escape all user-provided strings to prevent XSS (CWE-79)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=False)

    # Build the list items for discussion points
    safe_points = []
    for point in points:
        # Escape each point individually
        escaped_point = html.escape(point, quote=False)
        safe_points.append(f"<li>{escaped_point}</li>")

    points_html = "\n      ".join(safe_points)

    # Format the final HTML using the template
    formatted_post = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )

    return formatted_post.strip()