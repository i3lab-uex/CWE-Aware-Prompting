import html
from typing import List

# A simple template for the forum post.  The placeholders are replaced with
# escaped values to avoid injection of arbitrary HTML.
FORUM_POST_FORMAT: str = """
<h1>{title}</h1>
<div class="post-body">{body}</div>
<ul class="options">
{options}
</ul>
"""

def _escape_and_wrap_li(item: str) -> str:
    """
    Escape a single markdown item and wrap it in an <li> tag.
    We only support plain text or simple markdown links like [text](url).
    """
    # Basic link conversion
    import re

    def repl(match: re.Match) -> str:
        text, url = match.group(1), match.group(2)
        return f'<a href="{html.escape(url, quote=True)}">{html.escape(text)}</a>'

    # Convert [text](url) to <a href="...">text</a>
    item = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', repl, item)

    # Escape remaining characters
    escaped = html.escape(item)
    return f'  <li>{escaped}</li>'

def build_forum_post(title: str, post_body: str, options_list: List[str]) -> str:
    """
    Construct a sanitized forum post from the supplied title, body,
    and list of options.

    Parameters
    ----------
    title : str
        The forum post's title or subject line.
    post_body : str
        Main content of the forum post.  Markdown is **not** parsed;
        only plain text is displayed.
    options_list : list[str]
        List of discussion points or options.  Each item may contain
        simple markdown links; everything else is escaped.

    Returns
    -------
    str
        The fully formatted and safe HTML forum post.
    """
    # Escape the title and body to avoid XSS or accidental markup
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(post_body)

    # Build the options list.  Empty or None lists result in an empty <ul>.
    if not options_list:
        safe_options = ''
    else:
        li_items = [_escape_and_wrap_li(opt) for opt in options_list]
        safe_options = '\n'.join(li_items)

    # Insert into the template
    post_html = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        options=safe_options
    )
    return post_html.strip()