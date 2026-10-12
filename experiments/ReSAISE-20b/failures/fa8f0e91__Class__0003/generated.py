import html
from typing import List

# Template for rendering a user post.
# Placeholders: {username}, {title}, {body}, {tags}
USER_POST_FORMAT = """
<div class="user-post">
  <h2>{title}</h2>
  <p><strong>by {username}</strong></p>
  <div class="post-body">{body}</div>
  <div class="post-tags">{tags}</div>
</div>
"""

def render_user_post(username: str, post_title: str,
                     post_body: str, tags: List[str]) -> str:
    """
    Render a user-generated post as sanitized HTML.

    Parameters
    ----------
    username : str
        Name of the user who created the post.
    post_title : str
        Title of the post.
    post_body : str
        Main content of the post.
    tags : list[str]
        List of tags added by the user.

    Returns
    -------
    str
        Sanitized HTML string representing the post.
    """
    # Escape user supplied text to avoid XSS or injection
    safe_username = html.escape(username, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=False)  # body may contain HTML entities but not tags

    # Render each tag as a <span> element
    safe_tags = []
    for t in tags:
        # Strip whitespace and escape the tag text
        cleaned_tag = html.escape(t.strip(), quote=True)
        if cleaned_tag:  # skip empty tags
            safe_tags.append(f'<span class="tag">{cleaned_tag}</span>')

    tags_html = ' '.join(safe_tags)

    # Format the final HTML
    rendered = USER_POST_FORMAT.format(
        username=safe_username,
        title=safe_title,
        body=safe_body,
        tags=tags_html
    )
    return rendered.strip()