import html
from typing import List

# Example template with placeholders.  In a real application this would be defined elsewhere.
USER_POST_FORMAT = (
    "<article class=\"post\">\n"
    "  <h1>{title}</h1>\n"
    "  <p class=\"author\">Posted by {writer_name}</p>\n"
    "  <div class=\"body\">{body}</div>\n"
    "  <footer class=\"tags\">{tags}</footer>\n"
    "</article>"
)

def generate_post_html(
    writer_name: str,
    title: str,
    body: str,
    tag_list: List[str]
) -> str:
    """
    Construct an XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    writer_name : str
        The name of the author.
    title : str
        The post's headline.
    body : str
        The main content of the post.
    tag_list : list[str]
        A collection of tags associated with the post.

    Returns
    -------
    str
        The fully formatted HTML string.
    """
    # Escape all user‑supplied content to prevent XSS and ensure well‑formedness.
    safe_writer = html.escape(writer_name, quote=True)
    safe_title  = html.escape(title, quote=True)
    safe_body   = html.escape(body)

    # Wrap each tag in a <span> element.  Each tag is escaped individually.
    safe_tags = " ".join(
        f"<span class=\"tag\">{html.escape(tag, quote=True)}</span>"
        for tag in tag_list
    )

    # Format the final HTML using the provided template.
    return USER_POST_FORMAT.format(
        writer_name=safe_writer,
        title=safe_title,
        body=safe_body,
        tags=safe_tags
    )