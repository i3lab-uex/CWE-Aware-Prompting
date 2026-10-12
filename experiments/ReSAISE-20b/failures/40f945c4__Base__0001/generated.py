import html

# Predefined HTML template with placeholders.
USER_POST_FORMAT = """
<div class="post">
  <h2>{post_heading}</h2>
  <p class="author">Posted by: {user_name}</p>
  <div class="content">{post_content}</div>
  <div class="tags">
    {post_tags}
  </div>
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
        Author's name.
    post_heading : str
        Title of the post.
    post_content : str
        Main body of the post.
    post_tags : list[str]
        List of tags associated with the post.

    Returns
    -------
    str
        A string containing a safe HTML snippet for rendering the post.

    Raises
    ------
    ValueError
        If any of the required arguments are missing or empty.
    """
    # Basic validation to avoid generating malformed HTML
    if not all([user_name, post_heading, post_content]) or post_tags is None:
        raise ValueError("All arguments must be provided and non-empty")

    # Escape user-provided data to prevent XSS
    esc_user_name = html.escape(user_name, quote=True)
    esc_post_heading = html.escape(post_heading, quote=True)
    esc_post_content = html.escape(post_content, quote=False)

    # Render each tag as a <span> element and escape the tag text
    escaped_tags = []
    for tag in post_tags:
        if not isinstance(tag, str):
            continue  # skip non-string tags
        escaped_tag = html.escape(tag, quote=True)
        escaped_tags.append(f'<span class="tag">{escaped_tag}</span>')

    post_tags_html = ' '.join(escaped_tags)

    # Substitute placeholders in the template
    html_output = USER_POST_FORMAT.format(
        user_name=esc_user_name,
        post_heading=esc_post_heading,
        post_content=esc_post_content,
        post_tags=post_tags_html
    )

    return html_output.strip()