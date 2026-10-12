import html
from typing import List

# Predefined template for the forum post.
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

def build_post_html(topic_title: str, body_text: str, list_items: List[str]) -> str:
    """
    Build a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic_title : str
        The title or main topic of the forum post.
    body_text : str
        The main body or content of the forum post.
    list_items : List[str]
        A collection of user‑provided discussion points or options in markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized HTML representation of the forum post.
    """
    # Escape all user input to prevent XSS or injection attacks
    safe_title = html.escape(topic_title, quote=True)
    safe_body = html.escape(body_text, quote=True)

    # Build the <ul> of discussion points
    if list_items:
        safe_points = ["<li>{}</li>".format(html.escape(item, quote=True)) for item in list_items]
        points_html = "<ul>\n" + "\n".join(safe_points) + "\n</ul>"
    else:
        points_html = "<p>No discussion points provided.</p>"

    # Format the final HTML
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )