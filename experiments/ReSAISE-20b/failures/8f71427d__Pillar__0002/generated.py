import html

# Predefined HTML template with named placeholders.
USER_POST_FORMAT = """
<article class="user-post">
  <header>
    <h2>{title}</h2>
    <p class="author">Posted by: {username}</p>
  </header>
  <section class="content">
    {body}
  </section>
  <footer class="tags">
    {tags}
  </footer>
</article>
"""

def render_user_content(username_key: str,
                        title_key: str,
                        body_key: str,
                        tag_elements: list[str]) -> str:
    """
    Generate a secure HTML representation of a user's forum post.

    Parameters
    ----------
    username_key : str
        Identifier (display name) of the post's creator.
    title_key : str
        Title/heading of the user's post.
    body_key : str
        Main content/body of the post.
    tag_elements : list[str]
        List of tags to associate with the post.

    Returns
    -------
    str
        XSS‑protected HTML string of the rendered post.

    Raises
    ------
    TypeError
        If tag_elements is not a list.
    ValueError
        If any of the required arguments are empty or None.
    """
    # Basic validation
    if not isinstance(tag_elements, list):
        raise TypeError("tag_elements must be a list of strings.")
    for tag in tag_elements:
        if not isinstance(tag, str):
            raise TypeError("Each tag must be a string.")
    for name, value in [("username_key", username_key),
                        ("title_key", title_key),
                        ("body_key", body_key)]:
        if not isinstance(value, str) or value == "":
            raise ValueError(f"{name} must be a non-empty string.")

    # Escape all user-supplied content to prevent XSS
    escaped_username = html.escape(username_key, quote=True)
    escaped_title   = html.escape(title_key, quote=True)
    escaped_body    = html.escape(body_key, quote=False)  # preserve newlines

    # Render each tag inside a <span> element, escaping the tag text
    rendered_tags = " ".join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tag_elements
    )

    # Format the final HTML using the predefined template
    return USER_POST_FORMAT.format(
        username=escaped_username,
        title=escaped_title,
        body=escaped_body.replace("\n", "<br>"),  # preserve line breaks
        tags=rendered_tags
    )