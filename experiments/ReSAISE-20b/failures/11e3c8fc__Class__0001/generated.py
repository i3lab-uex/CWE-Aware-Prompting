import html

# Example template; in real usage this should be defined elsewhere.
USER_POST_FORMAT = """
<div class="post" data-author="{author_id}">
    <h1>{post_heading}</h1>
    <div class="content">{content}</div>
    <div class="tags">{labels}</div>
</div>
"""

def render_blog_post(author_id: str,
                     post_heading: str,
                     content: str,
                     labels: list[str]) -> str:
    """
    Render a secure, XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    author_id : str
        Identifier of the post's creator.
    post_heading : str
        Heading/title of the user's post.
    content : str
        Main body/content of the post.
    labels : list[str]
        List of tags/labels associated with the post.

    Returns
    -------
    str
        HTML string safely escaped and formatted for display.
    """
    # Escape all user supplied data to prevent injection
    safe_author_id = html.escape(author_id, quote=True)
    safe_heading = html.escape(post_heading, quote=True)
    safe_content = html.escape(content)

    # Wrap each label in a <span> element, escaping its content
    safe_labels = "".join(
        f'<span class="tag">{html.escape(label, quote=True)}</span>'
        for label in labels
    )

    # Format the final HTML using the provided template.
    return USER_POST_FORMAT.format(
        author_id=safe_author_id,
        post_heading=safe_heading,
        content=safe_content,
        labels=safe_labels
    )