import html

# Example template; in a real application this would be defined elsewhere.
USER_POST_FORMAT = """
<div class="blog-post" data-author="{author_id}">
  <h2>{post_heading}</h2>
  <div class="content">{content}</div>
  <div class="tags">{labels}</div>
</div>
"""

def render_blog_post(author_id: str, post_heading: str,
                     content: str, labels: list[str]) -> str:
    """
    Render a forum post as XSS‑protected HTML.

    Parameters
    ----------
    author_id : str
        Identifier of the post's creator.
    post_heading : str
        The heading/title of the post.
    content : str
        Main body of the post.
    labels : list[str]
        Tags associated with the post.

    Returns
    -------
    str
        A safe HTML string representing the post.
    """
    # Escape all user‑supplied values
    esc_author_id = html.escape(author_id, quote=True)
    esc_heading   = html.escape(post_heading, quote=True)
    esc_content   = html.escape(content, quote=False)

    # Wrap each escaped label in a <span>
    esc_labels = ''.join(
        f'<span class="tag">{html.escape(label, quote=True)}</span>'
        for label in labels
    )

    # Format the template with the escaped values
    return USER_POST_FORMAT.format(
        author_id=esc_author_id,
        post_heading=esc_heading,
        content=esc_content,
        labels=esc_labels
    )