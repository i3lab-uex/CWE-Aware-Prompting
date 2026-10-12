import html

# Example template; in real usage this should be defined elsewhere.
USER_POST_FORMAT = """
<article class="post">
  <header>
    <h2>{title}</h2>
    <p class="author">By {writer_name}</p>
  </header>
  <section class="body">
    {body}
  </section>
  <footer class="tags">
    {tags}
  </footer>
</article>
"""

def generate_post_html(writer_name: str,
                       title: str,
                       body: str,
                       tag_list: list[str]) -> str:
    """
    Construct a safe HTML representation of a forum post.

    Parameters
    ----------
    writer_name : str
        Name of the author.
    title : str
        Post headline.
    body : str
        Main content of the post.
    tag_list : list[str]
        Tags associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML string formatted according to USER_POST_FORMAT.
    """
    # Escape all user-provided content to prevent XSS
    safe_writer_name = html.escape(writer_name, quote=True)
    safe_title = html.escape(title, quote=True)
    # For the body we preserve line breaks but still escape HTML
    safe_body = html.escape(body, quote=True).replace("\n", "<br>")

    # Build tags markup
    safe_tags = "".join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tag_list
    )

    # Format the final HTML
    return USER_POST_FORMAT.format(
        writer_name=safe_writer_name,
        title=safe_title,
        body=safe_body,
        tags=safe_tags
    )