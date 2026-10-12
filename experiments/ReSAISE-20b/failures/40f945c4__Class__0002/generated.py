import html

# Predefined template with placeholders for the post components.
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
    Generate a sanitized HTML representation of a user's forum post.

    Parameters
    ----------
    user_name : str
        The author of the post.
    post_heading : str
        The title of the user's post.
    post_content : str
        The main content of the user's post.
    post_tags : list[str]
        A list of tags associated with the post.

    Returns
    -------
    str
        A string containing the sanitized HTML representation of the user's post.

    Raises
    ------
    TypeError
        If any argument is not of the expected type.
    """
    # Validate input types
    if not isinstance(user_name, str):
        raise TypeError("user_name must be a string")
    if not isinstance(post_heading, str):
        raise TypeError("post_heading must be a string")
    if not isinstance(post_content, str):
        raise TypeError("post_content must be a string")
    if not isinstance(post_tags, list) or not all(isinstance(t, str) for t in post_tags):
        raise TypeError("post_tags must be a list of strings")

    # Escape all user-supplied content to neutralize HTML injection
    safe_user_name = html.escape(user_name, quote=True)
    safe_post_heading = html.escape(post_heading, quote=True)
    safe_post_content = html.escape(post_content, quote=False)  # Preserve newlines if desired

    # Build tag spans
    safe_tags = []
    for tag in post_tags:
        escaped_tag = html.escape(tag, quote=True)
        safe_tags.append(f'<span class="tag">{escaped_tag}</span>')
    tags_html = ' '.join(safe_tags)

    # Format the final HTML
    post_html = USER_POST_FORMAT.format(
        user_name=safe_user_name,
        post_heading=safe_post_heading,
        post_content=safe_post_content,
        post_tags=tags_html
    )

    return post_html.strip()