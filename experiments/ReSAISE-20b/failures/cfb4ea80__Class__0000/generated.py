import html
from typing import List

# Pre‑defined HTML template for a forum post.
# The placeholders {title}, {body} and {points} will be substituted
# by the `create_forum_entry` function.
FORUM_POST_FORMAT: str = """
<article class="forum-post">
  <header>
    <h1>{title}</h1>
  </header>
  <section class="post-body">
    {body}
  </section>
  <footer class="discussion-points">
    <h2>Discussion Points</h2>
    {points}
  </footer>
</article>
"""

def create_forum_entry(title: str, body: str, points: List[str]) -> str:
    """
    Assemble a safe, well‑formatted forum post.

    Parameters
    ----------
    title : str
        The main topic or heading of the forum post.
    body : str
        Primary content of the post. May contain user‑supplied text.
    points : List[str]
        A list of discussion points or options, each expressed in markdown
        format. Markdown is stripped to plain text and escaped.

    Returns
    -------
    str
        The fully formatted HTML forum post, with all user input safely escaped.

    Raises
    ------
    TypeError
        If any argument is of an unexpected type.
    """
    # Validate input types
    if not isinstance(title, str):
        raise TypeError("title must be a string")
    if not isinstance(body, str):
        raise TypeError("body must be a string")
    if not isinstance(points, list) or not all(isinstance(p, str) for p in points):
        raise TypeError("points must be a list of strings")

    # Escape title and body to prevent injection
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Convert each point to a list item.
    # Strip markdown by removing common inline markup characters.
    def strip_markdown(text: str) -> str:
        # Very simple markdown stripping: remove *, _, `, and > characters.
        # This is sufficient for basic safety; more complex parsing can be added
        # if needed.
        return text.replace("*", "").replace("_", "").replace("`", "").replace(">", "")

    list_items = []
    for point in points:
        cleaned = strip_markdown(point)
        escaped = html.escape(cleaned, quote=True)
        list_items.append(f"<li>{escaped}</li>")

    points_html = "<ul>\n" + "\n".join(list_items) + "\n</ul>"

    # Format the final HTML post
    formatted_post = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )

    return formatted_post.strip()