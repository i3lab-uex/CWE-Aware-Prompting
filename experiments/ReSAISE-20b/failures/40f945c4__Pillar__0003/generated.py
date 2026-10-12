import html

# Predefined HTML template with placeholders for the post components.
USER_POST_FORMAT = """
<div class="post">
  <h2>{post_heading}</h2>
  <p class="author">Posted by: {user_name}</p>
  <div class="content">{post_content}</div>
  <div class="tags">{post_tags}</div>
</div>
"""

def build_post_html(user_name: str,
                    post_heading: str,
                    post_content: str,
                    post_tags: list[str]) -> str:
    """
    Generate a sanitized HTML representation of a forum post.

    Parameters
    ----------
    user_name : str
        Author of the post.
    post_heading : str
        Title of the post.
    post_content : str
        Main content body of the post.
    post_tags : list[str]
        List of tags associated with the post.

    Returns
    -------
    str
        Sanitized HTML string containing the formatted post.
    """
    # Escape user-supplied content to prevent XSS and ensure well‑formedness.
    safe_user_name = html.escape(user_name, quote=True)
    safe_heading = html.escape(post_heading, quote=True)
    # For content we allow line breaks but still escape HTML characters.
    safe_content = html.escape(post_content, quote=True).replace('\n', '<br>')

    # Build tags as separate <span> elements.
    safe_tags = []
    for tag in post_tags:
        escaped_tag = html.escape(tag, quote=True)
        safe_tags.append(f'<span class="tag">{escaped_tag}</span>')
    tags_html = ' '.join(safe_tags)

    # Format the final HTML.
    return USER_POST_FORMAT.format(
        user_name=safe_user_name,
        post_heading=safe_heading,
        post_content=safe_content,
        post_tags=tags_html
    )