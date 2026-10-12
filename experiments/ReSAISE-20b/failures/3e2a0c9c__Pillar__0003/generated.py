import html
from typing import List

# Predefined HTML template for forum posts.
# The placeholders {title}, {body} and {points} will be replaced with the
# sanitized content.  The template should not contain any user‑supplied data
# directly to avoid injection attacks.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  {points}
</div>
"""

def build_post_html(topic_title: str,
                    body_text: str,
                    list_items: List[str]) -> str:
    """
    Build a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic_title : str
        The title or main topic of the forum post.
    body_text : str
        The main body/content of the forum post.
    list_items : List[str]
        A collection of discussion points or options.  Each item is
        expected to be plain text; it may contain markdown characters,
        but no HTML.

    Returns
    -------
    str
        A fully formatted, safe HTML string containing the title,
        body and an unordered list of discussion points.

    Notes
    -----
    * All user supplied strings are escaped using :func:`html.escape`
      to prevent injection of malicious markup.
    * The function does not attempt to render markdown; it simply
      escapes any characters that could be interpreted as HTML.
    * The function verifies that the template contains all required
      placeholders; if not, it raises a :class:`ValueError`.
    """
    # Validate that the template contains the required placeholders.
    if not all(placeholder in FORUM_POST_FORMAT for placeholder in ("{title}", "{body}", "{points}")):
        raise ValueError("FORUM_POST_FORMAT does not contain required placeholders.")

    # Escape user supplied strings.
    safe_title = html.escape(topic_title, quote=True)
    safe_body = html.escape(body_text, quote=True)

    # Build the unordered list of discussion points.
    if list_items:
        safe_list = "\n".join(
            f"  <li>{html.escape(item, quote=True)}</li>" for item in list_items
        )
        points_html = f"\n<ul>\n{safe_list}\n</ul>"
    else:
        points_html = ""  # No list if no items were supplied.

    # Substitute placeholders with sanitized content.
    final_html = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )

    return final_html.strip()