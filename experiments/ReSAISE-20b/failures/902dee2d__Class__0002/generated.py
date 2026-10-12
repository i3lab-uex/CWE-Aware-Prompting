import html
from typing import List

# Example template; in real usage this would be defined elsewhere.
FORUM_POST_FORMAT = """
<h1>{title}</h1>
<div class="post-content">{content}</div>
{points}
"""

def build_forum_post(headline: str, content: str, items: List[str]) -> str:
    """
    Assemble a forum post from the given headline, content and discussion points.

    Parameters
    ----------
    headline : str
        The title of the forum post.
    content : str
        The main body text of the post.
    items : list[str]
        A list of discussion points supplied by the user. Each item may contain
        Markdown formatting but is rendered as plain text in an HTML list.

    Returns
    -------
    str
        The fully formatted forum post as a string, with all user supplied
        content properly escaped to prevent HTML injection.

    Raises
    ------
    TypeError
        If any argument is of an unexpected type.
    ValueError
        If `items` contains non-string elements.
    """
    # Validate argument types
    if not isinstance(headline, str):
        raise TypeError(f"headline must be a string, got {type(headline).__name__}")
    if not isinstance(content, str):
        raise TypeError(f"content must be a string, got {type(content).__name__}")
    if not isinstance(items, list):
        raise TypeError(f"items must be a list, got {type(items).__name__}")

    # Ensure all items are strings
    for i, item in enumerate(items):
        if not isinstance(item, str):
            raise ValueError(f"items[{i}] must be a string, got {type(item).__name__}")

    # Escape user supplied strings to neutralize special HTML characters
    safe_headline = html.escape(headline, quote=True)
    safe_content = html.escape(content, quote=True)

    # Build the discussion points list
    if items:
        safe_items = "".join(f"<li>{html.escape(item, quote=True)}</li>" for item in items)
        points_html = f"<ul>{safe_items}</ul>"
    else:
        # No discussion points; omit the list entirely
        points_html = ""

    # Construct the final post using the template
    post = FORUM_POST_FORMAT.format(
        title=safe_headline,
        content=safe_content,
        points=points_html
    )

    return post.strip()