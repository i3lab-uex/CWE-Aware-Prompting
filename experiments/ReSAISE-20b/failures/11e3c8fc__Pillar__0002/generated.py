# -*- coding: utf-8 -*-
"""
Secure rendering of a forum post.

The function `render_blog_post` takes the components of a blog post
(author, title, content and tags) and returns an HTML string that is
safe from XSS attacks.  All user‑supplied text is escaped with
`html.escape`, and each tag is wrapped in a `<span>` element.
"""

import html

# Example format string.  The placeholders must match the arguments
# used in `render_blog_post`.  Adjust as necessary for your project.
USER_POST_FORMAT = (
    '<article class="blog-post">'
    '  <header>'
    '    <h1>{post_heading}</h1>'
    '    <p class="author">Posted by: {author_id}</p>'
    '  </header>'
    '  <section class="content">{content}</section>'
    '  <footer class="tags">{labels}</footer>'
    '</article>'
)

def render_blog_post(author_id: str,
                     post_heading: str,
                     content: str,
                     labels: list[str]) -> str:
    """
    Return a XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    author_id : str
        Identifier of the post's creator.
    post_heading : str
        Heading/title of the post.
    content : str
        Main body text of the post.
    labels : list[str]
        List of tags/labels associated with the post.

    Returns
    -------
    str
        The rendered HTML string, fully escaped to prevent XSS.

    Raises
    ------
    TypeError
        If any of the arguments are not of the expected type.
    """
    # Basic type validation
    if not isinstance(author_id, str):
        raise TypeError("author_id must be a string")
    if not isinstance(post_heading, str):
        raise TypeError("post_heading must be a string")
    if not isinstance(content, str):
        raise TypeError("content must be a string")
    if not isinstance(labels, list) or any(not isinstance(l, str) for l in labels):
        raise TypeError("labels must be a list of strings")

    # Escape all user‑supplied data
    esc_author = html.escape(author_id, quote=True)
    esc_heading = html.escape(post_heading, quote=True)
    esc_content = html.escape(content, quote=True)

    # Render tags: each tag is wrapped in a <span>, escaped individually
    rendered_tags = ''.join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in labels
    )

    # Fill the template
    rendered_html = USER_POST_FORMAT.format(
        author_id=esc_author,
        post_heading=esc_heading,
        content=esc_content,
        labels=rendered_tags
    )

    return rendered_html

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    html_output = render_blog_post(
        author_id="user123",
        post_heading="<Hello & World>",
        content="This is a <b>bold</b> move!",
        labels=["python", "security & privacy"]
    )
    print(html_output)