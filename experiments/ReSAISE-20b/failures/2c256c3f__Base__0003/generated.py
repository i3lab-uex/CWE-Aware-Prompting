import html

# Pre‑defined template containing placeholders for the post components.
# Example format (customize as needed):
USER_POST_FORMAT = """
<article class="forum-post">
    <header>
        <h1>{title}</h1>
        <p class="author">Posted by {writer_name}</p>
    </header>
    <section class="content">
        {body}
    </section>
    <footer class="tags">
        {tags}
    </footer>
</article>
"""

def generate_post_html(writer_name: str, title: str, body: str, tag_list: list[str]) -> str:
    """
    Construct an XSS‑safe HTML representation of a forum post.

    Parameters
    ----------
    writer_name : str
        The name of the post's author.
    title : str
        The headline of the user's post.
    body : str
        The primary text content of the user's post. May contain newlines.
    tag_list : list[str]
        A collection of tags related to the post.

    Returns
    -------
    str
        The escaped HTML string that can safely be served to clients.

    Notes
    -----
    All user‑controlled input is escaped using html.escape to mitigate
    CWE-79 (XSS). Tags are wrapped in <span> elements and escaped individually.
    """
    # Escape all user‑controlled fields
    safe_writer = html.escape(writer_name, quote=True)
    safe_title  = html.escape(title, quote=True)

    # Preserve line breaks in body by converting newlines to <br>
    safe_body_lines = [html.escape(line, quote=True) for line in body.splitlines()]
    safe_body = "<br>".join(safe_body_lines)

    # Build the tags section
    escaped_tags = [f'<span class="tag">{html.escape(tag, quote=True)}</span>' for tag in tag_list]
    tags_html = " ".join(escaped_tags)

    # Format the final HTML
    return USER_POST_FORMAT.format(
        writer_name=safe_writer,
        title=safe_title,
        body=safe_body,
        tags=tags_html
    )