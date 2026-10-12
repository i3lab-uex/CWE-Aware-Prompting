import html

def build_html_page(page_content: str) -> str:
    """
    Build an HTML page by safely inserting user-provided content into a template.

    Parameters
    ----------
    page_content : str
        The dynamic content supplied by the user. It will be HTML‑escaped before being inserted.

    Returns
    -------
    str
        The final HTML string with the escaped user content embedded in the template.
    """
    # Basic HTML template with a placeholder for user content
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Safe Page</title>
</head>
<body>
    {user_content}
</body>
</html>"""

    # Escape the user content to prevent injection (CWE‑74)
    safe_content = html.escape(page_content, quote=True)

    # Insert the escaped content into the template
    final_html = html_template.format(user_content=safe_content)
    return final_html