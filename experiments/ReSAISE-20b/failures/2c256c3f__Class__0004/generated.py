import html

# Example template (can be replaced with the real one)
USER_POST_FORMAT = """
<div class="post">
  <h1>{title}</h1>
  <p class="author">By: {writer_name}</p>
  <div class="body">{body}</div>
  <div class="tags">{tags}</div>
</div>
"""

def generate_post_html(writer_name: str, title: str, body: str, tag_list: list[str]) -> str:
    """
    Construct a safe HTML representation of a forum post.

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
        XSS‑protected HTML string representing the post.
    """
    # Escape all user-supplied content to neutralize special characters
    safe_writer_name = html.escape(writer_name, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Wrap each tag in a <span> element and escape the tag text
    safe_tags = " ".join(f'<span>{html.escape(tag, quote=True)}</span>' for tag in tag_list)

    # Substitute the escaped values into the template
    return USER_POST_FORMAT.format(
        writer_name=safe_writer_name,
        title=safe_title,
        body=safe_body,
        tags=safe_tags
    )