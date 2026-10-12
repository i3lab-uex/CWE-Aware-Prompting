import html

# Example template (should be defined elsewhere in your codebase)
USER_POST_FORMAT = """
<div class="post">
    <h1>{post_heading}</h1>
    <p><strong>Author:</strong> {author_id}</p>
    <div class="content">{content}</div>
    <div class="tags">{labels}</div>
</div>
"""

def render_blog_post(author_id: str, post_heading: str,
                     content: str, labels: list[str]) -> str:
    """
    Render a safe HTML representation of a blog post.

    Args:
        author_id: Identifier of the post's creator.
        post_heading: Heading/title of the post.
        content: Main body text of the post.
        labels: List of tag strings.

    Returns:
        A string containing the HTML markup for the post, with all user
        supplied data properly escaped to prevent XSS or injection attacks.
    """
    # Escape all user provided text
    safe_author = html.escape(author_id, quote=True)
    safe_heading = html.escape(post_heading, quote=True)
    safe_content = html.escape(content, quote=False)

    # Wrap each label in a <span> and escape it
    safe_labels = ''.join(
        f'<span>{html.escape(label, quote=True)}</span>'
        for label in labels
    )

    # Render the final HTML using the template
    return USER_POST_FORMAT.format(
        author_id=safe_author,
        post_heading=safe_heading,
        content=safe_content,
        labels=safe_labels
    )