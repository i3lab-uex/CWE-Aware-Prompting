#!/usr/bin/env python3
"""
Utility to generate a safe HTML representation of a forum post.
"""

import html
from typing import List

# Default template if USER_POST_FORMAT is not defined elsewhere.
USER_POST_FORMAT = (
    "<article class=\"post\">\n"
    "  <header>\n"
    "    <h2>{post_heading}</h2>\n"
    "    <p class=\"author\">Posted by {user_name}</p>\n"
    "  </header>\n"
    "  <section class=\"content\">\n"
    "    {post_content}\n"
    "  </section>\n"
    "  <footer class=\"tags\">\n"
    "    {post_tags}\n"
    "  </footer>\n"
    "</article>"
)

def build_post_html(
    user_name: str,
    post_heading: str,
    post_content: str,
    post_tags: List[str]
) -> str:
    """
    Generate a sanitized HTML string for a forum post.

    Parameters
    ----------
    user_name : str
        The author of the post.
    post_heading : str
        Title of the user's post.
    post_content : str
        Main content of the user's post. May contain newlines and HTML.
    post_tags : List[str]
        A list of tags associated with the post.

    Returns
    -------
    str
        Sanitized HTML representation of the user's post.

    Notes
    -----
    - All user-provided data is escaped to prevent XSS.
    - Newlines in `post_content` are converted to <br> tags for readability.
    """
    # Escape all user-supplied strings
    safe_user_name = html.escape(user_name, quote=True)
    safe_heading = html.escape(post_heading, quote=True)

    # Convert newlines to <br> for content
    safe_content = html.escape(post_content, quote=True).replace("\n", "<br>")

    # Build tags HTML
    tag_spans = []
    for tag in post_tags:
        escaped_tag = html.escape(tag, quote=True)
        tag_spans.append(f'<span class="tag">{escaped_tag}</span>')
    safe_tags = " ".join(tag_spans)

    # Format the final HTML
    html_output = USER_POST_FORMAT.format(
        user_name=safe_user_name,
        post_heading=safe_heading,
        post_content=safe_content,
        post_tags=safe_tags
    )
    return html_output

# Example usage (for manual testing only)
if __name__ == "__main__":
    example = build_post_html(
        user_name="Alice <script>",
        post_heading="Hello & Welcome!",
        post_content="This is a test.\nNew line here.",
        post_tags=["python", "security <b>"]
    )
    print(example)