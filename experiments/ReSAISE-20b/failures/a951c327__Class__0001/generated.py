import html

# Predefined template – replace placeholders with actual content.
USER_POST_FORMAT = """
<div class="post">
    <h2>{title}</h2>
    <p class="author">Posted by: {author}</p>
    <div class="body">{body}</div>
    <div class="tags">
        {tags}
    </div>
</div>
"""

def generate_post_html(author: str, title: str, body: str, post_tags: list[str]) -> str:
    """
    Generate a sanitized HTML representation of a forum post.

    Parameters
    ----------
    author : str
        The name of the user who posted.
    title : str
        The post's title.
    body : str
        The main content of the post.
    post_tags : list[str]
        A list of tags associated with the post.

    Returns
    -------
    str
        Sanitized HTML string ready for rendering in a browser.
    """
    # Escape all user-supplied content to prevent XSS / injection attacks
    safe_author = html.escape(author, quote=True)
    safe_title  = html.escape(title,   quote=True)
    safe_body   = html.escape(body,   quote=False).replace("\n", "<br>")

    # Render each tag as a <span>, escaping the tag text
    safe_tags = " ".join(f'<span class="tag">{html.escape(tag, quote=True)}</span>'
                         for tag in post_tags)

    # Build the final HTML
    return USER_POST_FORMAT.format(
        title=safe_title,
        author=safe_author,
        body=safe_body,
        tags=safe_tags
    )