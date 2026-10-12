import html

# Example template (this would normally be defined elsewhere in the application)
USER_POST_FORMAT = """
<div class="post">
  <h2>{post_heading}</h2>
  <p class="author">Posted by: {author_id}</p>
  <div class="content">{content}</div>
  <div class="tags">{labels}</div>
</div>
"""

def render_blog_post(author_id: str, post_heading: str, content: str, labels: list[str]) -> str:
    """
    Generate a safe HTML representation of a blog post.

    Parameters
    ----------
    author_id : str
        Identifier of the post's creator.
    post_heading : str
        Title of the user's post.
    content : str
        Primary content of the user's post.
    labels : list[str]
        Sequence of tags associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML string of the forum post.
    """
    # Escape all user-supplied data to prevent XSS
    safe_author_id = html.escape(author_id, quote=True)
    safe_post_heading = html.escape(post_heading, quote=True)
    safe_content = html.escape(content)

    # Wrap each label in a <span> element, escaping the label itself
    safe_labels = ' '.join(
        f'<span class="tag">{html.escape(label, quote=True)}</span>'
        for label in labels
    )

    # Format the final HTML using the predefined template
    return USER_POST_FORMAT.format(
        author_id=safe_author_id,
        post_heading=safe_post_heading,
        content=safe_content,
        labels=safe_labels
    )