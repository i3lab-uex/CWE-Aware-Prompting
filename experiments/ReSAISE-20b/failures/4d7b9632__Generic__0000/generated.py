import html

# Example template; replace with the actual one in your codebase.
USER_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <p><strong>Author:</strong> {author_name}</p>
    <div class="post-body">{body}</div>
    <div class="post-tags">{tags}</div>
</div>
"""

def render_forum_post(author_name: str,
                      title: str,
                      body_content: str,
                      tag_list: list[str]) -> str:
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
    # Escape all user-supplied text to prevent XSS
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body_content)

    # Wrap each tag in a <span> element and escape the tag text
    safe_tags = ' '.join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tag_list
    )

    # Format the final HTML using the predefined template
    return USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        body=safe_body,
        tags=safe_tags
    )