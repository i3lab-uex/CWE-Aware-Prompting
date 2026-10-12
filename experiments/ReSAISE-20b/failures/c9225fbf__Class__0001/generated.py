import html

# Existing template with placeholders that will be replaced by actual values.
USER_POST_FORMAT = """
<div class="post">
  <h2>{title}</h2>
  <p class="author">Posted by: {author_name}</p>
  <div class="content">{content}</div>
  <div class="tags">{tags}</div>
</div>
"""

def create_post_html(author_name: str,
                     post_title: str,
                     content: str,
                     post_tags: list[str]) -> str:
    """
    Construct a safe HTML representation of a forum post.

    Parameters
    ----------
    author_name : str
        Name of the user who posted.
    post_title : str
        Title of the forum post.
    content : str
        Main body of the post.
    post_tags : list[str]
        List of tags associated with the post.

    Returns
    -------
    str
        A fully escaped HTML string ready for rendering.
    """
    # Escape user-provided content to prevent XSS and other injection attacks.
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_content = html.escape(content)

    # Each tag is escaped and wrapped in a <span> element.
    safe_tags = " ".join(f'<span>{html.escape(tag)}</span>' for tag in post_tags)

    # Substitute placeholders with the escaped values.
    html_output = USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        content=safe_content,
        tags=safe_tags
    )
    return html_output.strip()