import html

# A minimal HTML template that contains a placeholder for user content.
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
    Injects user-supplied content into a predefined HTML template, ensuring that the
    content is properly escaped to prevent XSS and other injection attacks.

    Parameters:
        page_content (str): The raw user-provided content to be embedded in the page.

    Returns:
        str: A complete HTML document with the escaped user content inserted.
    """
    # Escape special HTML characters to neutralize any embedded markup or scripts.
    escaped_content = html.escape(page_content, quote=True)

    # Safely format the template. Using `format` instead of f-strings to avoid accidental
    # execution of unintended expressions and to keep the placeholder explicit.
    return html_template.format(user_content=escaped_content)