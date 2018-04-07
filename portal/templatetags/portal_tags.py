from django import template
import urllib.request,base64
from io import StringIO,BytesIO


register = template.Library()

@register.filter
def get64(url):
    """
    Method returning base64 image data instead of URL
    """
    if url.startswith("http"):
        with urllib.request.urlopen(url) as url1:
            image = StringIO(url1.read().decode('utf-8'))
        return 'data:image/jpg;base64,' + base64.b64encode(image.read())

    return url