import html
from typing import List

# Pre‑defined template for forum posts.
# It contains placeholders: {title}, {body} and {points}
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h1>{title}</h1>
  <div class="post-body">{body}</div>
  <ul class="discussion-points">
    {points}
  </ul>
</div>
"""

def _escape_and_strip_markdown(text: str) -> str:
    """
    Escapes HTML special characters and removes basic markdown syntax
    that could be used for injection. This is a minimal approach to
    mitigate CWE‑707 by ensuring the output is well‑formed HTML.
    """
    # Escape all characters that have special meaning in HTML
    escaped = html.escape(text)

    # Very simple markdown cleanup: remove asterisks, hyphens and underscores
    # that might be used for bold/italic formatting. This prevents attempts to
    # inject malformed HTML via markdown.
    cleaned = (
        escaped.replace("*", "")
               .replace("_", "")
               .replace("-", "")
    )
    return cleaned

def compile_post(subject: str, text: str, highlights: List[str]) -> str:
    """
    Assemble a forum post from the given subject, body text and discussion points.
    
    Parameters
    ----------
    subject : str
        The title of the forum post.
    text : str
        Main body content of the post.
    highlights : list[str]
        Discussion points supplied in markdown format.

    Returns
    -------
    str
        A sanitized HTML string ready to be rendered in a forum.
    
    Raises
    ------
    ValueError
        If any of the inputs are not strings or if highlights is not a list.
    """
    # Basic type checks
    if not isinstance(subject, str):
        raise ValueError("subject must be a string")
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    if not isinstance(highlights, list) or any(not isinstance(h, str) for h in highlights):
        raise ValueError("highlights must be a list of strings")

    # Sanitize title and body
    safe_title = _escape_and_strip_markdown(subject)
    safe_body  = _escape_and_strip_markdown(text)

    # Build the discussion points list
    safe_points_items = []
    for point in highlights:
        cleaned_point = _escape_and_strip_markdown(point)
        safe_points_items.append(f"<li>{cleaned_point}</li>")

    # Join all list items
    safe_points = "\n".join(safe_points_items)

    # Format the final post using the template
    formatted_post = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=safe_points
    )

    return formatted_post.strip()