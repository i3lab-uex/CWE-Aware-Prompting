import html

# Example HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dynamic Page</title>
</head>
<body>
    {user_content}
</body>
</html>
"""

def build_html_page(page_content: str) -> str:
    """
    Return a full HTML page with the provided user content safely escaped.

    Parameters
    ----------
    page_content : str
        Dynamic content supplied by the user.  It will be HTML‑escaped before
        insertion to avoid XSS attacks.

    Returns
    -------
    str
        The final HTML string with the escaped content inserted into the
        template.
    """
    # Escape special characters to prevent injection of malicious HTML/JS.
    escaped_content = html.escape(page_content, quote=True)

    # Inject the escaped content into the template.
    return html_template.format(user_content=escaped_content)