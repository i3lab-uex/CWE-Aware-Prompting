import html
from typing import List

# Example template – adjust as needed for your application.
USER_POST_FORMAT = """
<article class="forum-post">
    <header>
        <h2>{heading}</h2>
        <p class="author">Posted by: {poster}</p>
    </header>
    <section class="content">
        {body}
    </section>
    <footer class="tags">
        {labels}
    </footer>
</article>
"""

def create_forum_post(poster: str, heading: str, body: str, labels: List[str]) -> str:
    """
    Generate a sanitized HTML representation of a forum post.

    Args:
        poster: The author of the post.
        heading: The title of the post.
        body: The main content of the post (may contain line breaks and HTML‑like text).
        labels: A list of tags associated with the post.

    Returns:
        A string containing a well‑formed, HTML‑escaped representation of the post.
    """
    # Escape all user-supplied content to avoid XSS and ensure well‑formedness.
    safe_poster = html.escape(poster, quote=True)
    safe_heading = html.escape(heading, quote=True)

    # Convert newlines in body to <br> tags for display while escaping content.
    safe_body_lines = [html.escape(line, quote=True) for line in body.splitlines()]
    safe_body = "<br>".join(safe_body_lines)

    # Render each label as a separate <span>, escaping the text.
    safe_labels = " ".join(
        f'<span class="tag">{html.escape(label, quote=True)}</span>' for label in labels
    )

    # Populate the template.
    rendered = USER_POST_FORMAT.format(
        poster=safe_poster,
        heading=safe_heading,
        body=safe_body,
        labels=safe_labels
    )
    return rendered.strip()