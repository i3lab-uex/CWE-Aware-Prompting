import html

# Predefined HTML template for a forum post. 
# It uses `{title}`, `{content}` and `{points}` as placeholders.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{content}</div>
  {points}
</div>
"""

def compile_post(subject: str, text: str, highlights: list[str]) -> str:
    """
    Assemble a forum post from the given subject, text and highlights.
    
    Parameters
    ----------
    subject : str
        Title or main topic of the forum post.
    text : str
        Primary content/body of the post.
    highlights : list[str]
        Discussion points or options, expected in markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized HTML string ready for rendering.
    
    Raises
    ------
    ValueError
        If any argument is not of the expected type.
    """
    # Basic type validation
    if not isinstance(subject, str):
        raise ValueError("subject must be a string")
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    if not isinstance(highlights, list) or not all(isinstance(h, str) for h in highlights):
        raise ValueError("highlights must be a list of strings")

    # Escape user input to prevent XSS
    safe_title = html.escape(subject, quote=True)
    safe_content = html.escape(text, quote=True)

    # Render highlights as an HTML unordered list
    if highlights:
        safe_items = "".join(f"<li>{html.escape(item, quote=True)}</li>" for item in highlights)
        safe_points = f"<ul>{safe_items}</ul>"
    else:
        safe_points = ""

    # Format the final post
    formatted_post = FORUM_POST_FORMAT.format(
        title=safe_title,
        content=safe_content,
        points=safe_points
    )
    
    return formatted_post.strip()