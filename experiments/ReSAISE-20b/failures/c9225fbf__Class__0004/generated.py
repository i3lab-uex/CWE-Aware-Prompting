import html

# Example template – adjust placeholders as needed.
USER_POST_FORMAT = """
<article class="forum-post">
  <header>
    <h1>{post_title}</h1>
    <p class="author">Posted by: {author_name}</p>
  </header>
  <section class="content">
    {content}
  </section>
  <footer class="tags">
    {tags}
  </footer>
</article>
"""

def create_post_html(author_name: str,
                     post_title: str,
                     content: str,
                     post_tags: list[str]) -> str:
    """
    Construct an XSS‑protected HTML representation of a forum post.

    Args:
        author_name: The name of the post's author.
        post_title: The headline of the user's post.
        content: The primary text content of the user's post.
        post_tags: A collection of tags related to the post.

    Returns:
        A string containing the sanitized HTML representation.
    """
    # Escape all user‑supplied text to neutralize special characters.
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_content = html.escape(content, quote=False)  # Preserve newlines if needed

    # Build the tags section: each tag is wrapped in a <span>.
    safe_tags = []
    for tag in post_tags:
        # Escape the tag text; we don't need to escape quotes inside <span>.
        escaped_tag = html.escape(tag, quote=True)
        safe_tags.append(f'<span class="tag">{escaped_tag}</span>')
    tags_html = ' '.join(safe_tags)

    # Insert the escaped values into the template.
    html_output = USER_POST_FORMAT.format(
        post_title=safe_title,
        author_name=safe_author,
        content=safe_content,
        tags=tags_html
    )
    return html_output.strip()