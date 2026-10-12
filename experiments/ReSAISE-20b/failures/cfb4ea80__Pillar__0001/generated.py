import html
from typing import List

# Pre‑defined template with placeholders for title, body and points.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
    {points_section}
</div>
"""

def _markdown_to_html(markdown: str) -> str:
    """
    Very small markdown → HTML converter that only supports
    headings, bold, italic and unordered lists. It is intentionally
    minimal to avoid external dependencies while preventing XSS.
    """
    # Escape all characters first
    escaped = html.escape(markdown)

    # Convert **bold** and *italic*
    escaped = escaped.replace(r"\*\*", "<b>").replace(r"</b>", "</b>")
    escaped = escaped.replace(r"\*", "<i>").replace(r"</i>", "</i>")

    # Convert unordered list items
    lines = escaped.splitlines()
    in_list = False
    result_lines = []
    for line in lines:
        if line.startswith("- "):
            if not in_list:
                result_lines.append("<ul>")
                in_list = True
            item = line[2:].strip()
            result_lines.append(f"<li>{item}</li>")
        else:
            if in_list:
                result_lines.append("</ul>")
                in_list = False
            result_lines.append(line)
    if in_list:
        result_lines.append("</ul>")
    return "\n".join(result_lines)

def create_forum_entry(title: str, body: str, points: List[str]) -> str:
    """
    Assemble a sanitized forum post from the given title, body and
    discussion points. The points are rendered as an HTML unordered
    list after converting any minimal markdown.

    Parameters:
        title (str): The post's title.
        body (str): The main content of the post.
        points (List[str]): A list of discussion points in markdown.

    Returns:
        str: The fully formatted, safe HTML forum post.
    """
    # Sanitize title and body
    safe_title = html.escape(title)
    safe_body = _markdown_to_html(body)

    # Render points as an unordered list
    if points:
        rendered_points = []
        for point in points:
            # Convert markdown to HTML and escape it
            rendered_points.append(_markdown_to_html(point))
        points_section = "<ul>\n" + "\n".join(f"<li>{p}</li>" for p in rendered_points) + "\n</ul>"
    else:
        points_section = ""

    # Build the final HTML
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points_section=points_section
    )