import html
from typing import List

# Pre‑defined template for a forum post.
# The placeholders `{title}`, `{body}` and `{points}` will be
# substituted by the function below.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    {points}
</div>
"""

def compile_post(subject: str, text: str, highlights: List[str]) -> str:
    """
    Assemble a safe, well‑formed forum post from user input.

    Parameters
    ----------
    subject : str
        Title or main topic of the forum post.
    text : str
        Primary content/body of the post.
    highlights : list[str]
        Discussion points or options in markdown format.

    Returns
    -------
    str
        A fully formatted HTML string ready for rendering in a forum.

    Notes
    -----
    All user input is escaped to prevent injection attacks (CWE‑74).
    """
    # Escape all user supplied strings
    safe_subject = html.escape(subject, quote=True)
    safe_body = html.escape(text, quote=True)

    # Convert each highlight to a list item; escape its content.
    li_items = []
    for point in highlights:
        escaped_point = html.escape(point, quote=True)
        li_items.append(f"<li>{escaped_point}</li>")

    points_html = ""
    if li_items:
        # Wrap the list items in an unordered list
        points_html = f"<ul>\n{''.join(li_items)}\n</ul>"

    # Render the final template
    post_html = FORUM_POST_FORMAT.format(
        title=safe_subject,
        body=safe_body,
        points=points_html
    )

    return post_html.strip()