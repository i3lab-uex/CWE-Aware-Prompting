import html
from typing import List

# Example template – replace with the actual one used in your project.
USER_POST_FORMAT = """
<article class="post">
  <header>
    <h1>{title}</h1>
    <p class="author">Posted by {writer_name}</p>
  </header>
  <section class="content">
    {body}
  </section>
  <footer class="tags">
    {tags}
  </footer>
</article>
"""

def generate_post_html(writer_name: str, title: str, body: str,
                       tag_list: List[str]) -> str:
    """
    Construct an XSS‑safe HTML representation of a forum post.

    Parameters
    ----------
    writer_name : str
        Name of the author.
    title : str
        Title/headline of the post.
    body : str
        Main content of the post. May contain line breaks and HTML‑like syntax.
    tag_list : List[str]
        Collection of tags. Each will be wrapped in a <span>.

    Returns
    -------
    str
        A string containing the escaped and formatted HTML.
    """
    # Escape all user‑controllable content to prevent XSS.
    esc_writer = html.escape(writer_name, quote=True)
    esc_title = html.escape(title, quote=True)

    # Body may contain newlines; preserve them as <br> for readability.
    esc_body_lines = [html.escape(line, quote=True) for line in body.splitlines()]
    esc_body = "<br>".join(esc_body_lines)

    # Build tags: each tag is escaped and wrapped in a <span>.
    esc_tags = " ".join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tag_list
    )

    # Render the final HTML using the template.
    return USER_POST_FORMAT.format(
        writer_name=esc_writer,
        title=esc_title,
        body=esc_body,
        tags=esc_tags
    )