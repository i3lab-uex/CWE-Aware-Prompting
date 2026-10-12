import html
from typing import List

# Example template. In a real application this would be defined elsewhere.
FORUM_POST_FORMAT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
</head>
<body>
<h1>{title}</h1>
<div class="post-body">{body}</div>
{points}
</body>
</html>
"""


def _escape_markdown(text: str) -> str:
    """
    Escape any HTML characters in a markdown string.
    The string is not parsed as Markdown – it is simply treated
    as plain text to avoid XSS vulnerabilities.
    """
    return html.escape(text)


def compile_post(subject: str, text: str, highlights: List[str]) -> str:
    """
    Assemble a forum post from the given subject, body text and
    discussion points.

    Parameters
    ----------
    subject : str
        The title or main topic of the forum post.
    text : str
        The primary content or body text of the post.
    highlights : list[str]
        A series of user‑supplied discussion points or options
        in markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized HTML forum post.
    """
    if not isinstance(subject, str):
        raise TypeError("subject must be a string")
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(highlights, list) or not all(isinstance(h, str) for h in highlights):
        raise TypeError("highlights must be a list of strings")

    # Sanitize title and body
    safe_title = html.escape(subject)
    safe_body = html.escape(text)

    # Build the discussion points list
    if highlights:
        li_items = "\n".join(
            f"  <li>{_escape_markdown(h)}</li>" for h in highlights
        )
        points_html = f"<ul>\n{li_items}\n</ul>"
    else:
        points_html = ""

    # Render the final HTML
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )