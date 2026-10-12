import html

# Example template: replace the placeholders with actual content.
USER_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <p class="author">Posted by: {author_name}</p>
  <div class="content">{body}</div>
  <div class="tags">{tags}</div>
</div>
"""

def render_forum_post(author_name: str, title: str, body_content: str,
                      tag_list: list[str]) -> str:
    """
    Return a safe HTML representation of a forum post.

    Parameters
    ----------
    author_name : str
        Identifier of the post's creator.
    title : str
        Heading of the user's post.
    body_content : str
        Primary content of the user's post.
    tag_list : list[str]
        Sequence of tags associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML string.
    """
    # Escape all user supplied strings to neutralize special characters.
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body_content, quote=False)  # preserve line breaks

    # Build tag spans, escaping each tag individually.
    escaped_tags = []
    for tag in tag_list:
        escaped_tag = html.escape(tag, quote=True)
        escaped_tags.append(f'<span class="tag">{escaped_tag}</span>')
    tags_html = ' '.join(escaped_tags)

    # Format the final HTML using the predefined template.
    return USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        body=safe_body,
        tags=tags_html
    )