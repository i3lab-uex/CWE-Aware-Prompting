import html
from typing import List

# Predefined template with named placeholders.
USER_POST_FORMAT = (
    "<article class=\"forum-post\">\n"
    "  <header>\n"
    "    <h2>{title}</h2>\n"
    "    <p class=\"author\">Posted by {author_name}</p>\n"
    "  </header>\n"
    "  <section class=\"content\">\n"
    "    {body}\n"
    "  </section>\n"
    "  <footer class=\"tags\">\n"
    "    {tags}\n"
    "  </footer>\n"
"</article>"
)

def _escape_and_format(value: str) -> str:
    """
    Escape a string for inclusion in HTML and strip any dangerous
    control characters that might affect the structure.
    """
    # html.escape handles &, <, >, ", '
    escaped = html.escape(value, quote=True)
    # Remove any remaining null bytes or control characters
    return "".join(ch for ch in escaped if 32 <= ord(ch) <= 126)

def render_forum_post(
    author_name: str,
    title: str,
    body_content: str,
    tag_list: List[str]
) -> str:
    """
    Generate a secure, XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    author_name : str
        Identifier of the post's creator.
    title : str
        Heading of the user's post.
    body_content : str
        Primary content of the user's post.
    tag_list : list[str]
        Sequence of tags associated with the post.

    Returns
    -------
    str
        The formatted, escaped HTML string.

    Raises
    ------
    ValueError
        If any required placeholder is missing from the template.
    """
    # Escape user supplied values
    safe_author = _escape_and_format(author_name)
    safe_title = _escape_and_format(title)
    # Body content may contain paragraphs, lists etc.; we escape it but
    # allow newlines to be preserved as <br> for readability.
    safe_body = html.escape(body_content, quote=True).replace("\n", "<br>")
    # Wrap each tag in a <span> and escape the tag text
    safe_tags = " ".join(
        f"<span class=\"tag\">{_escape_and_format(tag)}</span>"
        for tag in tag_list
    )

    # Verify that all placeholders are present to avoid CWE-707
    required_placeholders = {"author_name", "title", "body", "tags"}
    missing = required_placeholders - set(USER_POST_FORMAT.split("{")[1:])
    if missing:
        raise ValueError(f"Missing placeholders in template: {missing}")

    # Format the final string
    formatted = USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        body=safe_body,
        tags=safe_tags
    )
    return formatted