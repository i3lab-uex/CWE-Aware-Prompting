import html
import re

# Example template – replace with the actual forum post format used in your system.
FORUM_POST_FORMAT = """
<html>
<head><title>{subject}</title></head>
<body>
<h1>{subject}</h1>
<div class="post-body">{text}</div>
<ul class="highlights">{highlights}</ul>
</body>
</html>
"""

def _sanitize_text(raw: str) -> str:
    """
    Basic sanitization to prevent XSS:
      * Escape HTML special characters.
      * Remove <script> tags and their content.
    """
    # Remove script blocks
    cleaned = re.sub(r'<script.*?>.*?</script>', '', raw, flags=re.DOTALL | re.IGNORECASE)
    # Escape remaining HTML
    return html.escape(cleaned, quote=True)

def compile_post(subject: str, text: str, highlights: list[str]) -> str:
    """
    Assemble a forum post from the given components.

    Parameters
    ----------
    subject : str
        The title or main topic of the forum post.
    text : str
        The primary content or body text of the post.
    highlights : list[str]
        Discussion points or options in markdown format.

    Returns
    -------
    str
        The fully formatted and sanitized forum post as an HTML string.
    """
    # Sanitize the title, body text
    safe_subject = _sanitize_text(subject)
    safe_text = _sanitize_text(text)

    # Convert each highlight into a safe <li> element
    safe_items = []
    for item in highlights:
        # Escape the content to avoid XSS; no further markdown parsing is performed.
        escaped = _sanitize_text(item)
        safe_items.append(f"<li>{escaped}</li>")
    safe_highlights = "\n".join(safe_items)

    # Render the final post using the template
    return FORUM_POST_FORMAT.format(
        subject=safe_subject,
        text=safe_text,
        highlights=safe_highlights
    )