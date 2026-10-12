import html
from typing import List

# Predefined template – replace placeholders with safe content
USER_POST_FORMAT = """
<div class="post" data-author="{author_id}">
  <h2>{post_heading}</h2>
  <div class="content">{content}</div>
  <div class="tags">{labels}</div>
</div>
"""

def _escape(value: str) -> str:
    """Return an HTML‑escaped version of *value*."""
    return html.escape(value, quote=True)

def render_blog_post(
    author_id: str,
    post_heading: str,
    content: str,
    labels: List[str]
) -> str:
    """
    Render a forum post as safe HTML.

    Parameters
    ----------
    author_id : str
        Identifier of the post's creator.
    post_heading : str
        The heading/title of the user's post.
    content : str
        The main body text of the post.
    labels : list[str]
        Labels/tags associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML representation of the post.
    """
    # Validate and escape all inputs
    safe_author = _escape(author_id or "")
    safe_heading = _escape(post_heading or "")
    safe_content = _escape(content or "")

    # Wrap each label in a <span> and escape it
    safe_labels = " ".join(
        f'<span class="tag">{_escape(label)}</span>' for label in labels or []
    )

    # Use the template, substituting escaped values
    return USER_POST_FORMAT.format(
        author_id=safe_author,
        post_heading=safe_heading,
        content=safe_content,
        labels=safe_labels
    )