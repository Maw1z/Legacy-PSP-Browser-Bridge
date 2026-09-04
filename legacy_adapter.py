from bs4 import BeautifulSoup
from urllib.parse import urljoin


def transform_html(html_bytes, base_url):
    """
    Transform modern HTML into a simplified format suitable
    for the legacy client.
    """

    soup = BeautifulSoup(html_bytes, "html.parser")

    # Remove elements the legacy client cannot handle
    for tag in soup.find_all([
        "script",
        "iframe",
        "video",
        "audio",
        "canvas",
        "svg",
        "noscript"
    ]):
        tag.decompose()

    # Remove external stylesheets.
    # Inline styles are kept.
    for tag in soup.find_all("link", rel="stylesheet"):
        tag.decompose()

    # Remove modern metadata that may cause compatibility issues
    for tag in soup.find_all("meta"):
        name = tag.get("name", "").lower()

        if name in ["viewport", "theme-color"]:
            tag.decompose()

    # Rewrite URLs
    for tag in soup.find_all(True):
        for attr in ["href", "src", "action"]:
            value = tag.get(attr)

            if not value:
                continue

            # Resolve relative URLs
            absolute_url = urljoin(base_url, value)

            # Force HTTPS resources through the HTTP proxy
            if absolute_url.startswith("https://"):
                tag[attr] = absolute_url.replace(
                    "https://",
                    "http://",
                    1
                )

            elif absolute_url.startswith("http://"):
                tag[attr] = absolute_url

            # Leave things such as:
            # #anchor
            # mailto:
            # javascript:
            # untouched

    # Add minimal legacy-compatible styling
    style = soup.new_tag("style")
    style.string = """
        body {
            font-family: sans-serif;
            font-size: 14px;
            margin: 4px;
        }

        img {
            max-width: 450px;
        }

        a {
            color: #00f;
        }
    """

    if soup.head:
        soup.head.append(style)

    return str(soup).encode("utf-8", errors="replace")