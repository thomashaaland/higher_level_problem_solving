from requesting_urls import get_html
import re

def find_urls(html_str, base_url="", output=None):
    """
    Finds urls in a website
    
    Args:
        html_str :str: A website as a string
        base_url :str: Optional argument for handling relative url's
        output :str: Optional argument for writing results to file
    Returns:
        :list (str):

Example:
    >>> example_site = '''
    ... <a href="#fragment-only">anchor link</a>
    ... <a id="some-id" href="/relative/path#fragment">relative link</a>
    ... <a href="//other.host/same-protocol">same-protocol link</a>
    ... <a href="https://example.com">absolute URL</a>
    ... '''
    >>> find_urls(example_site, base_url="https://base.path")
    ['https://base.path/relative/path', 'https://other.host/same-protocol', 'https://example.com']
    """

    # Pattern explanation: Match everything not greedily from '<a '
    # including 'href="', and group everything not greedily until the
    # characters [", ;, & or #] is encountered
    # This is designed to capture links not including optional parameters
    pattern = r'(?:<a\s.*?href=")(.*?)(?:["#])'
    search_results = re.findall(pattern, html_str)
    
    search_results = [result for result in search_results if result != '']
    
    # Check to find /, and only /, at the beginning of string.
    # If it is, it is a relative path
    relative_path = r"^\/[^\/].*"

    # Check to find // at the beginning of string. If it is, it is missing a html
    missing_html = r"^\/\/.*"

    # Optimisation opportunity
    results = []
    for result in search_results:
        if re.findall(relative_path, result):
            results.append(base_url + result)
        elif re.findall(missing_html, result):
            results.append("https:" + result)
        elif result != '':
            results.append(result)


    if output is not None:
        with open(output, 'w') as f:
            print(f"Writing file {output}")
            for result in results:
                f.write(result + '\n')
            
    return results

def find_articles(html_str, output=None, ok_sites=["en", "no"]):
    """
    Given a link to a webpage this function returns links to 
    (english and norvegian) wikipedia articles from that page.
    Args:
        html_str :str: A link to a website as a string
        output :str: Optional argument for writing results to file
    Returns:
        :list (str): The resulting list of links to wikipedia articles

Example
    >>> example_site = '''
    ... <a href="#fragment-only">anchor link</a>
    ... <a id="some-id" href="/relative/path#fragment">relative link</a>
    ... <a href="//other.host/same-protocol">same-protocol link</a>
    ... <a href="https://example.com">absolute URL</a>
    ... '''
    >>> find_articles(example_site)
    ['https://en.wikipedia.org/relative/path']
    """

    

    # Only works on english and norwegian pages for now
    # Find ulrs starting with https://en.wikipedia.org/
    regex_for_wikis = r"^https:\/\/(" + "|".join(ok_sites) + ")\.wikipedia\.org[\/]?[^:]+$"
    base_url = r"https://en.wikipedia.org"
    urls = find_urls(html_str, base_url = base_url)
    results = [url for url in urls if re.findall(regex_for_wikis, url)]
    
    if output is not None:
        with open(output, 'w') as f:
            for result in results:
                f.write(result + '\n')

    return results
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    urls = [
        "https://en.wikipedia.org/wiki/Studio_Ghibli",
        "https://en.wikipedia.org/wiki/Star_Wars",
        "https://en.wikipedia.org/w/index.php",
    ]
    params = [None, None, {"title": "Main", "action": "info"}]
    outputs = ["Studio_Ghribli.txt", "Star_Wars.txt", "index.txt"]
    for url, param, output in zip(urls, params, outputs):
        html = get_html(url, params=param)
        find_urls(html, base_url = r"https://en.wikipedia.org/",
                  output = "./requesting_urls/" + "html_" + output)
        find_articles(html, output = "./requesting_urls/" + "wiki_article_" + output)
        
