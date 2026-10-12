import html

# Example template; in real usage this would be defined elsewhere.
USER_POST_FORMAT = """
<div class="post">
  <h2>{title}</h2>
  <p class="author">Posted by: {author_name}</p>
  <div class="content">{content}</div>
  <div class="tags">
    {tags}
  </div>
</div>
"""

def create_post_html(author_name: str,
                     post_title: str,
                     content: str,
                     post_tags: list[str]) -> str:
    """
    Construct an XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    author_name : str
        Name of the post's author.
    post_title : str
        Title/headline of the post.
    content : str
        Main body text of the post.
    post_tags : list[str]
        List of tags associated with the post.

    Returns
    -------
    str
        HTML string with escaped content and tags.
    """
    # Escape all user supplied strings to prevent XSS
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_content = html.escape(content)

    # Build tags string: each tag wrapped in <span> with escaped text
    safe_tags = ''.join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in post_tags
    )

    # Format the final HTML using the predefined template
    return USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        content=safe_content,
        tags=safe_tags
    )