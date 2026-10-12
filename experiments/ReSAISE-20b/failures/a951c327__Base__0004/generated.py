import html

# Example template – replace placeholders with actual values.
USER_POST_FORMAT = """
<div class="post">
  <h2>{title}</h2>
  <p class="author">by {author}</p>
  <div class="body">{body}</div>
  <div class="tags">
    {tags}
  </div>
</div>
"""

def generate_post_html(author: str, title: str, body: str, post_tags: list[str]) -> str:
    """
    Generate a sanitized HTML representation of a user's post.

    Args:
        author (str): The author of the post.
        title (str): The title of the user's post.
        body (str): The main content of the user's post.
        post_tags (list[str]): A list of tags associated with the post.

    Returns:
        str: The sanitized HTML string for the post.
    """
    # Escape all user-provided content to prevent XSS
    safe_author = html.escape(author, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=False)

    # Build the tags section
    tag_spans = []
    for tag in post_tags:
        safe_tag = html.escape(tag, quote=True)
        tag_spans.append(f'<span class="tag">{safe_tag}</span>')
    tags_html = " ".join(tag_spans)

    # Render the template with sanitized values
    html_output = USER_POST_FORMAT.format(
        title=safe_title,
        author=safe_author,
        body=safe_body,
        tags=tags_html
    )

    return html_output.strip()