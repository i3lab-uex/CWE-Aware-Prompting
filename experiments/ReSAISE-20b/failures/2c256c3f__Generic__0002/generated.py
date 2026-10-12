import html

# Example template (should be defined elsewhere in the actual codebase)
USER_POST_FORMAT = """
<article class="forum-post">
    <header>
        <h2>{title}</h2>
        <p class="author">Posted by: {writer_name}</p>
    </header>
    <section class="content">{body}</section>
    <footer class="tags">{tags}</footer>
</article>
"""

def generate_post_html(writer_name: str, title: str, body: str, tag_list: list[str]) -> str:
    """
    Construct an XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    writer_name : str
        The name of the post's author.
    title : str
        The headline of the user's post.
    body : str
        The primary text content of the user's post.
    tag_list : list[str]
        A collection of tags related to the post.

    Returns
    -------
    str
        XSS‑protected HTML string representing the forum post.
    """
    # Escape all user‑supplied text to avoid injection
    safe_writer_name = html.escape(writer_name, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body)

    # Build tags string: each tag wrapped in <span> and escaped
    safe_tags = "".join(f'<span class="tag">{html.escape(tag, quote=True)}</span>' for tag in tag_list)

    # Format the final HTML
    return USER_POST_FORMAT.format(
        writer_name=safe_writer_name,
        title=safe_title,
        body=safe_body,
        tags=safe_tags
    )