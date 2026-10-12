import html

# Predefined HTML template for forum posts.
# It contains placeholders `{title}`, `{body}` and `{points}` that will be
# substituted by the function.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  {points}
</div>
"""

def build_forum_entry(post_title: str, post_body: str, bullet_points: list[str]) -> str:
    """
    Build a sanitized HTML representation of a forum post.

    Parameters
    ----------
    post_title : str
        The title or main topic of the forum post.
    post_body : str
        The main body or content of the forum post.
    bullet_points : list[str]
        A collection of user-provided discussion points or options in markdown
        format. Each item will be rendered as an <li> element inside a <ul>.

    Returns
    -------
    str
        A fully formatted and sanitized HTML string that can safely be embedded
        in a web page.

    Notes
    -----
    - All user input is escaped using :func:`html.escape` to prevent XSS
      (CWE-79).
    - The function does not perform markdown rendering; it simply escapes the
      content and wraps each bullet point in a list item.
    """
    # Basic validation: ensure we have iterable bullet_points
    if not isinstance(bullet_points, list):
        raise TypeError("bullet_points must be a list of strings")

    # Escape title and body
    safe_title = html.escape(post_title or "")
    safe_body = html.escape(post_body or "")

    # Build the unordered list of discussion points
    if bullet_points:
        escaped_items = [f"<li>{html.escape(bp)}</li>" for bp in bullet_points]
        points_html = f"\n<ul>\n{''.join(escaped_items)}\n</ul>"
    else:
        points_html = ""

    # Format the final HTML
    return FORUM_POST_FORMAT.format(title=safe_title, body=safe_body, points=points_html)