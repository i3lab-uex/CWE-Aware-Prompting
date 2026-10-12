import html

# Pre‑defined HTML template for a forum post.
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
    {points}
  </aside>
</article>
"""

def create_forum_entry(title: str, body: str, points: list[str]) -> str:
    """
    Assemble a sanitized forum post from user input.

    Parameters
    ----------
    title : str
        The title or main topic of the forum post.
    body : str
        The primary content or body text of the post.
    points : list[str]
        A series of user‑supplied discussion points or options in markdown format.

    Returns
    -------
    str
        A fully formatted HTML string ready for rendering on a web page.
    """
    # Escape user input to prevent XSS
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True).replace('\n', '<br>')

    # Convert points into a safe unordered list
    if not isinstance(points, (list, tuple)):
        raise TypeError("points must be a list or tuple of strings")

    list_items = []
    for point in points:
        if not isinstance(point, str):
            raise TypeError("each point must be a string")
        escaped_point = html.escape(point, quote=True)
        list_items.append(f"<li>{escaped_point}</li>")

    points_html = f"<ul>\n{''.join(list_items)}\n</ul>" if list_items else ""

    # Format the final post
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )