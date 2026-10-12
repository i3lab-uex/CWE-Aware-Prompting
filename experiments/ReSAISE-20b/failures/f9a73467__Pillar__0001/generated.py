import html
from typing import List

# Predefined HTML template for forum posts.
# The placeholders are {title}, {body}, and {discussion}
FORUM_POST_FORMAT: str = """
<div class="forum-post">
  <h1>{title}</h1>
  <div class="post-body">{body}</div>
  <section class="discussion-points">
    {discussion}
  </section>
</div>
"""

def _escape_markdown_to_html(text: str) -> str:
    """
    Very small markdown to HTML converter for list items.
    It escapes the text and converts leading `-` or `*` into <li> elements.
    """
    # Escape any HTML special characters
    escaped = html.escape(text)

    # Replace markdown list markers with <li>
    lines = escaped.splitlines()
    li_items = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith(('-', '*')):
            content = stripped[1:].lstrip()
            li_items.append(f"<li>{content}</li>")
        else:
            # If not a list item, keep as paragraph
            li_items.append(f"<p>{line}</p>")
    return "\n".join(li_items)

def compile_post(subject: str, text: str, highlights: List[str]) -> str:
    """
    Assemble a sanitized forum post from the given subject, body text,
    and a list of discussion highlights.

    Args:
        subject (str): The title or main topic of the forum post.
        text (str): The primary content or body text of the post.
        highlights (List[str]): A series of user-supplied discussion points
            or options in markdown format.

    Returns:
        str: A fully formatted and sanitized forum post string.
    """
    # Sanitize the title
    safe_title = html.escape(subject)

    # Sanitize the main body text, preserving line breaks
    safe_body = html.escape(text).replace("\n", "<br>")

    # Render discussion points as an unordered list
    if highlights:
        # Escape each highlight and convert to <li>
        li_elements = []
        for item in highlights:
            # Use the helper to escape and convert markdown
            li_content = _escape_markdown_to_html(item)
            # Wrap the content in <li> if it's not already
            if not li_content.startswith("<li>"):
                li_elements.append(f"<li>{li_content}</li>")
            else:
                li_elements.append(li_content)
        discussion_html = "<ul>\n" + "\n".join(li_elements) + "\n</ul>"
    else:
        discussion_html = ""

    # Insert into the template
    formatted_post = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        discussion=discussion_html
    )

    return formatted_post.strip()