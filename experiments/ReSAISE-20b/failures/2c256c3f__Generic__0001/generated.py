import html

# Example placeholder template (adjust as needed)
USER_POST_FORMAT = """
<div class="post">
    <h2>{title}</h2>
    <p class="author">Posted by: {writer_name}</p>
    <div class="content">{body}</div>
    <div class="tags">{tags}</div>
</div>
"""

def generate_post_html(writer_name: str, title: str, body: str, tag_list: list[str]) -> str:
    """
    Construct an XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    writer_name : str
        The name of the post's author.
    title : str
        The headline of the user's post.
    body : str
        The primary text content of the user's post.
    tag_list : list[str]
        A collection of tags related to the post.

    Returns
    -------
    str
        The HTML string containing the escaped post data.
    """
    # Escape user‑supplied content to prevent XSS
    safe_writer = html.escape(writer_name, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body)

    # Build tags: each tag wrapped in a <span> element
    safe_tags = ''.join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tag_list
    )

    # Format the final HTML using the provided template
    return USER_POST_FORMAT.format(
        writer_name=safe_writer,
        title=safe_title,
        body=safe_body,
        tags=safe_tags
    )