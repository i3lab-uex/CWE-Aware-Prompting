import html
from typing import List

# Example template; in a real application this would be defined elsewhere.
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
    Build a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic_title : str
        The title or main topic of the forum post.
    body_text : str
        The main body or content of the forum post.
    list_items : List[str]
        A collection of user-provided discussion points or options in markdown format.

    Returns
    -------
    str
        The fully formatted and sanitized HTML representation of the forum post.
    """
    # Escape all user-controlled content to prevent XSS
    safe_title = html.escape(topic_title, quote=True)
    safe_body = html.escape(body_text, quote=True)

    # Convert each list item to a sanitized <li> element
    safe_list_items = []
    for item in list_items:
        escaped_item = html.escape(item, quote=True)
        safe_list_items.append(f"<li>{escaped_item}</li>")

    # Join the list items into a single <ul>
    if safe_list_items:
        points_html = f"<ul>{''.join(safe_list_items)}</ul>"
    else:
        points_html = "<p>No discussion points provided.</p>"

    # Format the final HTML using the predefined template
    post_html = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )

    return post_html.strip()