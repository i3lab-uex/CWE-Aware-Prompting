import html

# Predefined HTML template with placeholders.
USER_POST_FORMAT = """
<div class="post" data-author="{author_id}">
  <h2>{post_heading}</h2>
  <div class="content">{content}</div>
  <div class="tags">{labels}</div>
</div>
"""

def render_blog_post(author_id: str, post_heading: str,
                     content: str, labels: list[str]) -> str:
    """
    Generate a secure HTML representation of a forum post.

    Parameters
    ----------
    author_id : str
        Identifier of the post's creator.
    post_heading : str
        Heading/title of the post.
    content : str
        Main body text of the post.
    labels : list[str]
        List of tags/labels associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML string for the post.
    """
    # Escape all user‑controlled data
    safe_author = html.escape(author_id, quote=True)
    safe_heading = html.escape(post_heading, quote=True)
    safe_content = html.escape(content)

    # Wrap each escaped label in a <span> element
    safe_labels = "".join(
        f'<span class="tag">{html.escape(label)}</span>' for label in labels
    )

    # Format the template with escaped values
    return USER_POST_FORMAT.format(
        author_id=safe_author,
        post_heading=safe_heading,
        content=safe_content,
        labels=safe_labels
    )