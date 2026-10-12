import html
from typing import List

# Pre‑defined template for a forum post.  
# The placeholders {title}, {body} and {points} will be replaced by the function.
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

def build_forum_post(headline: str, content: str, items: List[str]) -> str:
    """
    Assemble a sanitized HTML forum post.

    Parameters
    ----------
    headline : str
        Title or main topic of the forum post.
    content : str
        Primary content or body text of the post. May contain newlines.
    items : list[str]
        Discussion points or options in markdown format.

    Returns
    -------
    str
        Fully formatted and sanitized HTML forum post.
    """
    # Escape user input to avoid XSS attacks
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(content, quote=True).replace('\n', '<br>')

    # Convert each markdown item into a safe <li>
    list_items = []
    for idx, item in enumerate(items):
        # Simple sanitization; more complex markdown parsing can be added if needed
        safe_item = html.escape(item, quote=True)
        list_items.append(f"<li>{safe_item}</li>")

    points_html = (
        "<ul>" + "".join(list_items) + "</ul>"
        if list_items
        else "<p>No discussion points provided.</p>"
    )

    # Format the final HTML using the template
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )