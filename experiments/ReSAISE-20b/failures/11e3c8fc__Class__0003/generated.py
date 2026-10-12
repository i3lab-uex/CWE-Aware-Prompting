import html
from typing import List

# Predefined HTML template with placeholders.
USER_POST_FORMAT = """
<div class="post" data-author="{author_id}">
  <h2>{post_heading}</h2>
  <div class="content">{content}</div>
  <div class="tags">{labels}</div>
</div>
"""

def render_blog_post(
    author_id: str,
    post_heading: str,
    content: str,
    labels: List[str]
) -> str:
    """
    Render a secure HTML representation of a forum post.

    Parameters
    ----------
    author_id : str
        Identifier of the post's creator.
    post_heading : str
        The heading/title of the user's post.
    content : str
        Primary textual content of the post.
    labels : list[str]
        Sequence of tags/labels associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML string of the formatted post.

    Notes
    -----
    All user supplied data is escaped using `html.escape` to neutralize any
    special characters that could lead to injection attacks (CWE‑74).
    """
    # Escape all user input to avoid HTML injection
    safe_author_id = html.escape(author_id, quote=True)
    safe_heading = html.escape(post_heading, quote=True)
    safe_content = html.escape(content)

    # Escape each label and wrap it in a <span> element
    escaped_labels = [
        f'<span class="tag">{html.escape(label, quote=True)}</span>'
        for label in labels
    ]
    safe_labels = " ".join(escaped_labels)

    # Format the final HTML using the predefined template
    rendered = USER_POST_FORMAT.format(
        author_id=safe_author_id,
        post_heading=safe_heading,
        content=safe_content,
        labels=safe_labels
    )

    return rendered.strip()