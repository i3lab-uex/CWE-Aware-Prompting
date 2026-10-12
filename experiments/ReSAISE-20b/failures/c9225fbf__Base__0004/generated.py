import html

# Pre‑defined template with placeholders for author, title, content and tags.
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
    Construct an XSS‑safe HTML representation of a forum post.

    Parameters
    ----------
    author_name : str
        The name of the user who created the post.
    post_title : str
        The headline of the post.
    content : str
        Main body text of the post.
    post_tags : list[str]
        List of tags to associate with the post.

    Returns
    -------
    str
        The HTML string containing escaped user input.
    """
    # Escape all user‑controlled inputs to prevent XSS (CWE‑79)
    safe_author = html.escape(author_name, quote=True)
    safe_title  = html.escape(post_title, quote=True)
    safe_content = html.escape(content, quote=False)

    # Escape tags individually and wrap each in a <span>
    safe_tags = ''.join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in post_tags
    )

    # Format the template with escaped values
    return USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        content=safe_content,
        tags=safe_tags
    )