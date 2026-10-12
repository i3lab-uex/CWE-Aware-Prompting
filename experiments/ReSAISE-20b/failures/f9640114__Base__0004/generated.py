import html
from typing import List

# Predefined template for a forum post.
FORUM_POST_FORMAT = """
<h1>{header}</h1>
<div class="post-body">{body}</div>
<ul class="options">
{options}
</ul>
"""

def build_forum_post(title: str, post_body: str, options_list: List[str]) -> str:
    """
    Construct a sanitized forum post.

    Args:
        title: The title or subject line of the forum post.
        post_body: The main content or body of the forum post.
        options_list: A collection of user-provided options or discussion points
                      in markdown format.

    Returns:
        A string containing the sanitized and formatted forum post, including
        a header, message body, and an HTML unordered list of options.

    Raises:
        TypeError: If any argument is not of the expected type.
    """
    if not isinstance(title, str):
        raise TypeError("title must be a string")
    if not isinstance(post_body, str):
        raise TypeError("post_body must be a string")
    if not isinstance(options_list, list) or not all(isinstance(opt, str) for opt in options_list):
        raise TypeError("options_list must be a list of strings")

    # Escape user-provided content to prevent XSS.
    safe_title = html.escape(title)
    safe_body = html.escape(post_body)

    # Convert markdown options to plain text and escape them.
    safe_options = "\n".join(f"<li>{html.escape(opt)}</li>" for opt in options_list)

    # Format the final post using the predefined template.
    return FORUM_POST_FORMAT.format(
        header=safe_title,
        body=safe_body,
        options=safe_options
    )