import html

# Example template – in real usage this would be defined elsewhere
USER_POST_FORMAT = """
<article class="post">
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
    Construct an XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    writer_name : str
        The name of the author.
    title : str
        The headline of the post.
    body : str
        The main content of the post. May contain user‑supplied text.
    tag_list : list[str]
        A collection of tags. Each will be wrapped in a <span> element.

    Returns
    -------
    str
        A fully escaped HTML string that can be safely inserted into a page.
    """
    # Escape all user‑supplied text to neutralize HTML/JS injection
    safe_writer_name = html.escape(writer_name, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=False)  # Preserve line breaks as &lt;br&gt; if needed

    # Build tag HTML – each tag is escaped and wrapped in <span>
    safe_tags = "".join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>' for tag in tag_list
    )

    # Format the final HTML using the template
    return USER_POST_FORMAT.format(
        writer_name=safe_writer_name,
        title=safe_title,
        body=safe_body.replace("\n", "<br>"),
        tags=safe_tags
    )