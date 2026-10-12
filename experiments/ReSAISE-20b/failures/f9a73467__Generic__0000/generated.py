import html
from typing import List

# Example template – the real one should be defined elsewhere in your project.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  {points_section}
</div>
"""

def compile_post(subject: str, text: str, highlights: List[str]) -> str:
    """
    Assemble a forum post from the given subject, body text and discussion points.

    Parameters
    ----------
    subject : str
        The title or main topic of the forum post.
    text : str
        The primary content or body text of the post.
    highlights : list[str]
        A series of user-supplied discussion points or options in markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized forum post, including the header,
        message body, and safely rendered discussion points.

    Raises
    ------
    TypeError
        If `highlights` is not a list or contains non-string elements.
    """
    # Validate input types
    if not isinstance(highlights, list):
        raise TypeError("highlights must be a list of strings")
    if not all(isinstance(item, str) for item in highlights):
        raise TypeError("all items in highlights must be strings")

    # Escape subject and body to prevent XSS
    safe_title = html.escape(subject, quote=True)
    safe_body = html.escape(text, quote=True)

    # Build the discussion points section
    if highlights:
        list_items = []
        for point in highlights:
            # Escape each point and strip surrounding markdown bullet symbols
            cleaned = point.strip()
            if cleaned.startswith(('- ', '* ')):
                cleaned = cleaned[2:].strip()
            escaped_point = html.escape(cleaned, quote=True)
            list_items.append(f"<li>{escaped_point}</li>")
        points_section = (
            '<div class="post-highlights"><h3>Discussion Points</h3><ul>'
            + "".join(list_items)
            + "</ul></div>"
        )
    else:
        points_section = ""

    # Render the final post
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points_section=points_section,
    )