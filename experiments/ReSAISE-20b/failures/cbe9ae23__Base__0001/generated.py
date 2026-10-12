import html
from typing import List

# Example template; in real usage this would be defined elsewhere.
USER_POST_FORMAT = """
<div class="forum-post">
  <h2>{heading}</h2>
  <p><strong>Posted by:</strong> {poster}</p>
  <div class="post-body">{body}</div>
  <div class="post-tags">
    {labels}
  </div>
</div>
"""

def create_forum_post(poster: str, heading: str, body: str, labels: List[str]) -> str:
    """
    Generate a sanitized HTML representation of a forum post.

    Parameters
    ----------
    poster : str
        Author of the post.
    heading : str
        Title of the post.
    body : str
        Main content of the post.
    labels : list[str]
        List of tags associated with the post.

    Returns
    -------
    str
        Sanitized HTML string ready to be embedded in a web page.

    Raises
    ------
    ValueError
        If any of the required arguments are missing or empty.
    """
    if not all([poster, heading, body]) :
        raise ValueError("Poster, heading, and body must be provided")

    # Escape user-controlled input to prevent XSS
    safe_poster = html.escape(poster, quote=True)
    safe_heading = html.escape(heading, quote=True)
    safe_body = html.escape(body, quote=False)  # allow < and > inside body? escape anyway

    # Render tags as individual span elements
    safe_labels = []
    for tag in labels:
        if not isinstance(tag, str):
            continue  # skip non-string tags
        safe_tag = html.escape(tag, quote=True)
        safe_labels.append(f'<span class="tag">{safe_tag}</span>')

    labels_html = " ".join(safe_labels)

    # Format the final HTML
    post_html = USER_POST_FORMAT.format(
        poster=safe_poster,
        heading=safe_heading,
        body=safe_body,
        labels=labels_html
    )

    return post_html.strip()