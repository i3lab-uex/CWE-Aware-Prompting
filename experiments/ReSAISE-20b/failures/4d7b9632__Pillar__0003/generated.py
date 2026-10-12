import html
from typing import List

# Example template – in real usage this would be imported or defined elsewhere.
USER_POST_FORMAT: str = (
    "<article class=\"forum-post\">\n"
    "  <header>\n"
    "    <h1>{title}</h1>\n"
    "    <p class=\"author\">Posted by: {author_name}</p>\n"
    "  </header>\n"
    "  <section class=\"content\">\n"
    "    {body}\n"
    "  </section>\n"
    "  <footer class=\"tags\">\n"
    "    {tags}\n"
    "  </footer>\n"
"</article>"
)

def render_forum_post(
    author_name: str,
    title: str,
    body_content: str,
    tag_list: List[str]
) -> str:
    """
    Generate a safe, well‑formed HTML representation of a forum post.

    Parameters
    ----------
    author_name : str
        Identifier of the post's creator.
    title : str
        Heading of the user's post.
    body_content : str
        Primary content of the user's post.
    tag_list : List[str]
        Sequence of tags associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML string of the forum post.

    Raises
    ------
    ValueError
        If any required argument is missing or not a string.
    """
    # Basic type checks – defensive programming
    if not isinstance(author_name, str):
        raise ValueError("author_name must be a string")
    if not isinstance(title, str):
        raise ValueError("title must be a string")
    if not isinstance(body_content, str):
        raise ValueError("body_content must be a string")
    if not isinstance(tag_list, list) or not all(isinstance(t, str) for t in tag_list):
        raise ValueError("tag_list must be a list of strings")

    # Escape all user supplied content to prevent XSS
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(title, quote=True)
    # Body may contain line breaks; preserve them with <br> after escaping
    safe_body = html.escape(body_content, quote=True).replace("\n", "<br>")

    # Wrap each tag in a <span>, escape the tag text, and concatenate
    safe_tags = " ".join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tag_list
    )

    # Format the final HTML using a secure template
    rendered = USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        body=safe_body,
        tags=safe_tags
    )

    # Ensure the output is well‑formed: minimal validation
    if not rendered.strip():
        raise ValueError("Rendered HTML is empty")

    return rendered