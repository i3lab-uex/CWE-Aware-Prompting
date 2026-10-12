import html

# Example template – adjust placeholders as needed.
USER_POST_FORMAT = """
<article class="post">
  <h1>{title}</h1>
  <p class="author">Posted by: {writer_name}</p>
  <div class="content">{body}</div>
  <div class="tags">{tags}</div>
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
        A well‑formed HTML string containing the post with escaped content.
    """
    # Escape all user supplied strings to avoid injection
    safe_writer_name = html.escape(writer_name, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=False)

    # Build tags string – each tag wrapped in a <span>
    escaped_tags = [f"<span>{html.escape(tag, quote=True)}</span>" for tag in tag_list]
    tags_html = " ".join(escaped_tags)

    # Populate the template
    post_html = USER_POST_FORMAT.format(
        writer_name=safe_writer_name,
        title=safe_title,
        body=safe_body,
        tags=tags_html
    )

    return post_html.strip()