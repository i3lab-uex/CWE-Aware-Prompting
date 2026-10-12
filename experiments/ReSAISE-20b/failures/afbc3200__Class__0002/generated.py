import html

# Predefined template for forum posts.
# The placeholders {title}, {body} and {points} will be replaced with escaped content.
FORUM_POST_FORMAT = """
<article class="forum-post">
    <header><h1>{title}</h1></header>
    <section class="post-body">{body}</section>
    <section class="discussion-points"><ul>{points}</ul></section>
</article>
"""

def build_forum_entry(post_title: str, post_body: str, bullet_points: list[str]) -> str:
    """
    Create a sanitized HTML representation of a forum post.

    Parameters
    ----------
    post_title : str
        The title or main topic of the forum post.
    post_body : str
        The main body or content of the forum post.
    bullet_points : list[str]
        A collection of user‑provided discussion points or options in markdown format.

    Returns
    -------
    str
        A string containing the fully formatted and sanitized HTML representation of
        the forum post, including header, message body, and safely rendered discussion points.

    Notes
    -----
    - All user input is escaped using `html.escape` to mitigate injection attacks
      (CWE‑74). No Markdown is rendered; instead, the raw text is safely escaped.
    - The function does not raise any exceptions; invalid inputs will be coerced to
      strings before escaping.
    """
    # Convert all parts to string and escape special HTML characters.
    safe_title = html.escape(str(post_title))
    safe_body = html.escape(str(post_body))

    # Build list items for bullet points, each escaped.
    safe_points = []
    for point in bullet_points:
        # Ensure point is a string and escape it.
        safe_point = html.escape(str(point))
        safe_points.append(f"<li>{safe_point}</li>")
    points_html = "\n".join(safe_points)

    # Format the final HTML using the predefined template.
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )