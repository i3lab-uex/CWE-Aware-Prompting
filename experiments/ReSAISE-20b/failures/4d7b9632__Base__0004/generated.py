import html

# Example template; in real usage this would be defined elsewhere.
USER_POST_FORMAT = """
<div class="post">
    <h2>{title}</h2>
    <p class="author">Posted by: {author_name}</p>
    <div class="content">{body}</div>
    <div class="tags">{tags}</div>
</div>
"""

def render_forum_post(author_name: str, title: str,
                      body_content: str, tag_list: list[str]) -> str:
    """
    Render a forum post as safe HTML.

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
        XSS‑protected HTML representation of the forum post.
    """
    # Escape all user-controlled input to prevent XSS
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body_content, quote=False)  # preserve line breaks

    # Wrap each tag in a <span> and escape it
    escaped_tags = []
    for tag in tag_list:
        escaped_tag = html.escape(tag, quote=True)
        escaped_tags.append(f'<span class="tag">{escaped_tag}</span>')
    tags_html = " ".join(escaped_tags)

    # Populate the template with escaped values
    return USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        body=safe_body,
        tags=tags_html
    )