import html

# Example template: placeholders are replaced using format().
USER_POST_FORMAT = (
    "<article class='post'>"
    "  <h1>{title}</h1>"
    "  <p class='author'>By {writer_name}</p>"
    "  <div class='body'>{body}</div>"
    "  <footer class='tags'>Tags: {tags}</footer>"
    "</article>"
)

def generate_post_html(writer_name: str,
                       title: str,
                       body: str,
                       tag_list: list[str]) -> str:
    """
    Construct an XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    writer_name : str
        Name of the author.
    title : str
        Title of the post.
    body : str
        Main content of the post.
    tag_list : list[str]
        Tags associated with the post.

    Returns
    -------
    str
        A safe HTML string for rendering.
    """
    # Escape all user‑supplied content to prevent injection
    safe_writer = html.escape(writer_name, quote=True)
    safe_title  = html.escape(title, quote=True)
    safe_body   = html.escape(body, quote=False)

    # Build tag spans; escape each tag individually
    safe_tags = " ".join(
        f"<span>{html.escape(tag, quote=True)}</span>"
        for tag in tag_list
    )

    # Format the template with safe values
    return USER_POST_FORMAT.format(
        writer_name=safe_writer,
        title=safe_title,
        body=safe_body,
        tags=safe_tags
    )