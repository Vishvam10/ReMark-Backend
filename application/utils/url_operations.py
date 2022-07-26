from urllib.parse import urlparse

def get_url(uri) :
    """
        URL is of the form : https://www.example.com/
        URI is of the form : https://www.example.com/something/#somethingelse ...
        This function returns the URL (with the trailing slash) 
        from an URI
    """
    if(uri == "127.0.0.1:5500/") :
        return uri
    res = urlparse(uri)
    if res.scheme == "" :
        return -1
    if res.netloc == "" :
        return -1    
    url = res.scheme + "://" + res.netloc + "/"
    return url
