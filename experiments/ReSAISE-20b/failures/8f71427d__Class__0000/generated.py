import html

# Predefined HTML template string.
# It should contain placeholders named `username_key`, `title_key`,
# `body_key` and `tag_elements`. For example:
USER_POST_FORMAT = """
<article class="user-post">
    <header>
        <h2>{title_key}</h2>
        <p class="author">Posted by: {username_key}</p>
    </header>
    <section class="content">
        {body_key}
    </section>
    <footer class="tags">
        {tag_elements}
    </footer>
</article>
"""

def render_user_content(
    username_key: str,
    title_key: str,
    body_key: str,
    tag_elements: list[str]
) -> str:
    """
    Render a user post as XSS‑protected HTML.

    Parameters
    ----------
    username_key : str
        Identifier of the post's creator.
    title_key : str
        Heading of the user's post.
    body_key : str
        Primary content of the user's post.
    tag_elements : list[str]
        Sequence of tags associated with the post.

    Returns
    -------
    str
        The escaped HTML representation of the forum post.
    """
    # Escape all user supplied text to neutralize special characters
    safe_username = html.escape(username_key, quote=True)
    safe_title = html.escape(title_key, quote=True)
    # The body may contain allowed formatting; escape it entirely to avoid
    # injection. If rich text is desired, a sanitizer like Bleach should be used.
    safe_body = html.escape(body_key, quote=True)

    # Wrap each tag in a <span> and escape it
    safe_tags = []
    for t in tag_elements:
        escaped_tag = html.escape(t, quote=True)
        safe_tags.append(f'<span class="tag">{escaped_tag}</span>')

    # Join tags with a space for readability
    safe_tag_elements = " ".join(safe_tags)

    # Render the final HTML using the predefined template
    rendered = USER_POST_FORMAT.format(
        username_key=safe_username,
        title_key=safe_title,
        body_key=safe_body,
        tag_elements=safe_tag_elements
    )

    return rendered.strip()