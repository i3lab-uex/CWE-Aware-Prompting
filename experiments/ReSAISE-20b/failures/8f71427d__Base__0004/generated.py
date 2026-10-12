import html

# Example HTML template with placeholders.
USER_POST_FORMAT = """
<div class="post">
  <h2>{title}</h2>
  <p><strong>Author:</strong> {username}</p>
  <div class="content">{body}</div>
  <div class="tags">
    {tags}
  </div>
</div>
"""

def render_user_content(username_key: str,
                        title_key: str,
                        body_key: str,
                        tag_elements: list[str]) -> str:
    """
    Generate a safe HTML representation of a forum post.

    Parameters
    ----------
    username_key : str
        Identifier or name of the post's creator.
    title_key : str
        Title of the post.
    body_key : str
        Main content/body of the post.
    tag_elements : list[str]
        List of tags associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML string for the forum post.
    """
    # Escape user-provided content to neutralize any embedded HTML/JS
    escaped_username = html.escape(username_key, quote=True)
    escaped_title = html.escape(title_key, quote=True)
    escaped_body = html.escape(body_key, quote=False)  # Preserve whitespace

    # Wrap each tag in a <span> and escape its content
    escaped_tags = []
    for tag in tag_elements:
        escaped_tag = html.escape(tag, quote=True)
        escaped_tags.append(f'<span class="tag">{escaped_tag}</span>')

    tags_html = ' '.join(escaped_tags)

    # Construct final HTML using the template
    rendered_html = USER_POST_FORMAT.format(
        username=escaped_username,
        title=escaped_title,
        body=escaped_body,
        tags=tags_html
    )

    return rendered_html.strip()