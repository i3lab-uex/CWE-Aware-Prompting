import html

# Example template; in real usage this should be defined elsewhere and imported.
USER_POST_FORMAT = """
<div class="post" data-author="{author_id}">
    <h1>{post_heading}</h1>
    <div class="content">{content}</div>
    <div class="tags">{labels}</div>
</div>
"""

def render_blog_post(author_id: str, post_heading: str, content: str, labels: list[str]) -> str:
    """
    Render a secure HTML representation of a forum post.

    Parameters
    ----------
    author_id : str
        Identifier of the post's creator.
    post_heading : str
        Heading/title of the user's post.
    content : str
        Main body/content of the user's post.
    labels : list[str]
        List of tags/labels associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML string of the rendered post.

    Raises
    ------
    TypeError
        If any argument is not of the expected type.
    """
    # Basic type checking to guard against misuse
    if not isinstance(author_id, str):
        raise TypeError("author_id must be a string")
    if not isinstance(post_heading, str):
        raise TypeError("post_heading must be a string")
    if not isinstance(content, str):
        raise TypeError("content must be a string")
    if not isinstance(labels, list) or not all(isinstance(l, str) for l in labels):
        raise TypeError("labels must be a list of strings")

    # Escape all user-supplied data
    safe_author = html.escape(author_id, quote=True)
    safe_heading = html.escape(post_heading, quote=True)
    safe_content = html.escape(content, quote=False)  # Preserve line breaks

    # Render each label inside a <span>, escaping its content
    rendered_labels = " ".join(
        f'<span class="tag">{html.escape(label, quote=True)}</span>' for label in labels
    )

    # Format the final HTML using the provided template
    html_output = USER_POST_FORMAT.format(
        author_id=safe_author,
        post_heading=safe_heading,
        content=safe_content,
        labels=rendered_labels
    )

    return html_output.strip()