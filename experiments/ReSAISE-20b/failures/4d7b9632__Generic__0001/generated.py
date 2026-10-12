import html

# Example template; in real usage this should be defined elsewhere.
USER_POST_FORMAT = """
<article class="forum-post">
    <header>
        <h1>{title}</h1>
        <p class="author">Posted by: {author_name}</p>
    </header>
    <section class="content">
        {body}
    </section>
    <footer class="tags">
        {tags}
    </footer>
</article>
"""

def render_forum_post(author_name: str, title: str, body_content: str,
                      tag_list: list[str]) -> str:
    """
    Render a forum post as secure HTML.

    Parameters
    ----------
    author_name : str
        Identifier of the post's creator.
    title : str
        Heading of the user's post.
    body_content : str
        Primary content of the user's post.
    tag_list : list[str]
        Sequence of tags associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML representation of the forum post.
    """
    # Escape all user supplied data
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(title, quote=True)

    # For the body we allow line breaks but strip any tags.
    safe_body = html.escape(body_content, quote=True).replace('\n', '<br>')

    # Render tags as individual <span> elements
    safe_tags = ' '.join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tag_list
    )

    # Format the final HTML using the predefined template
    rendered = USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        body=safe_body,
        tags=safe_tags
    )
    return rendered.strip()