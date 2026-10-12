import html
from typing import List

# A simple HTML template for a forum post.
# The placeholders `{title}`, `{body}` and `{points}` will be replaced
# by the function below.
FORUM_POST_FORMAT = """
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

def build_post_html(topic_title: str, body_text: str, list_items: List[str]) -> str:
    """
    Create a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic_title : str
        The title or main topic of the forum post.
    body_text : str
        The main content of the forum post.
    list_items : List[str]
        A collection of user-provided discussion points or options in
        markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized HTML representation of the forum post.

    Notes
    -----
    * All user input is escaped using `html.escape` to prevent XSS attacks.
    * Markdown is not rendered; items are treated as plain text.  If you
      need markdown rendering, integrate a safe Markdown library.
    """
    # Escape the title and body to ensure no raw HTML is injected.
    safe_title = html.escape(topic_title, quote=True)
    safe_body = html.escape(body_text, quote=True)

    # Build the unordered list of discussion points.
    if list_items:
        escaped_items = [f"<li>{html.escape(item, quote=True)}</li>" for item in list_items]
        points_html = f"<ul>{''.join(escaped_items)}</ul>"
    else:
        # If no items are provided, we still include an empty list for consistency.
        points_html = "<ul></ul>"

    # Format the final HTML using the template.
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )