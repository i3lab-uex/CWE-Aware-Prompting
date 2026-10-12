import html

# Example template; in real usage this could be loaded from a file or defined elsewhere
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Safe Page</title>
</head>
<body>
    <!-- User content goes here -->
    {user_content}
</body>
</html>
"""

def build_html_page(page_content: str) -> str:
    """
    Build a complete HTML page by safely inserting user-supplied content.

    Parameters
    ----------
    page_content : str
        The raw string provided by the user that should appear in the body of the page.

    Returns
    -------
    str
        The final HTML string with user content properly escaped to prevent injection.
    """
    # Escape special characters in the user content
    safe_content = html.escape(page_content, quote=True)

    # Inject the escaped content into the template
    final_html = html_template.format(user_content=safe_content)

    return final_html