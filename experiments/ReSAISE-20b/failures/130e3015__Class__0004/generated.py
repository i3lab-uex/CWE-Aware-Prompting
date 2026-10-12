import re
from html import escape

# Pre‑defined HTML template for blog posts
BLOG_FORMAT = """
<article class="blog-post">
  <h1>{title}</h1>
  <div class="content">{body}</div>
</article>
"""

def format_post_content(post_title: str, post_body: str) -> str:
    """
    Formats a blog post for safe display in an HTML page.

    Parameters
    ----------
    post_title : str
        The headline or title of the blog post.
    post_body : str
        The full text content of the blog post.

    Returns
    -------
    str
        A sanitized, HTML‑formatted string ready to be inserted into a page.

    Notes
    -----
    * The title and body are escaped to prevent HTML injection (CWE‑74).
    * All `<script>` tags, including those with attributes or nested content,
      are removed before escaping.
    * The function does not allow arbitrary HTML tags to be preserved; it
      outputs plain text wrapped in the provided template.
    """
    # 1. Remove any <script> tags and their content
    body_no_scripts = re.sub(r'<\s*script[^>]*?>.*?<\s*/\s*script\s*>',
                              '',
                              post_body,
                              flags=re.IGNORECASE | re.DOTALL)

    # 2. Escape remaining characters
    safe_title = escape(post_title, quote=True)
    safe_body = escape(body_no_scripts, quote=True)

    # 3. Insert into template
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)