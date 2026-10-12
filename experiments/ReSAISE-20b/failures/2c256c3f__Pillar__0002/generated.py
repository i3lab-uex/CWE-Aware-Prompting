import html
from typing import List

# Pre‑defined template with named placeholders.
USER_POST_FORMAT = """
<article class="forum-post">
    <header>
        <h1>{title}</h1>
        <p class="author">Posted by: {writer_name}</p>
    </header>
    <section class="content">
        {body}
    </section>
    <footer class="tags">
        {tags_html}
    </footer>
</article>
"""

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
        Name of the post's author.
    title : str
        Headline of the user's post.
    body : str
        Primary text content of the post. May contain line breaks or HTML‑like
        markup that must be escaped.
    tag_list : List[str]
        Collection of tags related to the post. Each tag is rendered inside
        a <span> element.

    Returns
    -------
    str
        A fully escaped HTML string ready to be embedded in a web page.

    Raises
    ------
    TypeError
        If any argument is not of the expected type.
    """
    # Basic type checks to guard against misuse
    if not isinstance(writer_name, str):
        raise TypeError("writer_name must be a string")
    if not isinstance(title, str):
        raise TypeError("title must be a string")
    if not isinstance(body, str):
        raise TypeError("body must be a string")
    if not isinstance(tag_list, list) or not all(isinstance(t, str) for t in tag_list):
        raise TypeError("tag_list must be a list of strings")

    # Escape all user‑supplied content to prevent XSS.
    escaped_writer = html.escape(writer_name, quote=True)
    escaped_title  = html.escape(title, quote=True)

    # Preserve line breaks in the body by converting \n to <br>.
    escaped_body = html.escape(body, quote=True).replace("\n", "<br>")

    # Build tag HTML; each tag is wrapped in a <span>.
    tags_html_parts = []
    for tag in tag_list:
        escaped_tag = html.escape(tag, quote=True)
        tags_html_parts.append(f'<span class="tag">{escaped_tag}</span>')
    tags_html = " ".join(tags_html_parts)

    # Format the final HTML using the predefined template.
    return USER_POST_FORMAT.format(
        writer_name=escaped_writer,
        title=escaped_title,
        body=escaped_body,
        tags_html=tags_html
    )