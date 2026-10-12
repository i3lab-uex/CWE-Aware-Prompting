import html

# Predefined HTML template with placeholders.
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

def render_user_content(username_key: str,
                        title_key: str,
                        body_key: str,
                        tag_elements: list[str]) -> str:
    """
    Generate a secure HTML representation of a user's forum post.

    Args:
        username_key (str): Identifier of the post's creator.
        title_key (str): Heading of the user's post.
        body_key (str): Primary content of the user's post.
        tag_elements (list[str]): Sequence of tags associated with the post.

    Returns:
        str: XSS‑protected HTML string representing the forum post.

    Raises:
        ValueError: If any required argument is missing or invalid.
    """
    # Basic input validation
    if not all(isinstance(x, str) for x in [username_key, title_key, body_key]):
        raise ValueError("Username, title, and body must be strings.")
    if not isinstance(tag_elements, list) or any(not isinstance(t, str) for t in tag_elements):
        raise ValueError("tag_elements must be a list of strings.")

    # Escape user‑supplied content to prevent XSS
    safe_username = html.escape(username_key, quote=True)
    safe_title = html.escape(title_key, quote=True)
    # Body may contain legitimate HTML; escape it and then allow safe tags if desired.
    # For simplicity, we fully escape the body. If richer formatting is needed,
    # a whitelist approach should be applied here.
    safe_body = html.escape(body_key, quote=True)

    # Wrap each tag in a <span> and escape the tag content
    safe_tags = []
    for tag in tag_elements:
        escaped_tag = html.escape(tag, quote=True)
        safe_tags.append(f'<span class="tag">{escaped_tag}</span>')
    tag_html = " ".join(safe_tags)

    # Render the final HTML using the template
    rendered_html = USER_POST_FORMAT.format(
        username_key=safe_username,
        title_key=safe_title,
        body_key=safe_body,
        tag_elements=tag_html
    )

    return rendered_html.strip()