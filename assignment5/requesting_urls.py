import requests as req


def get_html(url, params=None, output=None):
    """
    Reads a web adresss and returns its content as text.
    If you supply parameters, filters based on those.
    If output is supplied writes file to disk.

    Args:
        url :str: The url to the website to be read.
        params :dict: parameters to filter with.
        output :str: Need *.txt suffix. A file to write to.

    Retuns:
        :str: the website as a string.
    """

    # Check that the input is correct
    if not params is None:
        assert type(params) is dict, "The optional parameters needs to be a dictionary."
    if not output is None:
        assert all(
            [type(output) is str, output.endswith(".txt")]
        ), "The outputfile needs to be a *.txt file."

    # get the response, passing in the optional arguments
    response = req.get(url, params=params)
    html_str = response.text

    # If the optional argument is something, write the website as *.txt file
    if output:
        with open(output, "w") as f:
            print(f"Writing {output}")
            f.write(html_str)
            print(f"File {output} successfully written to disk")
    return html_str


# If this is run as a script it will produce and fetch from three websites.
if __name__ == "__main__":
    urls = [
        "https://en.wikipedia.org/wiki/Studio_Ghibli",
        "https://en.wikipedia.org/wiki/Star_Wars",
        "https://en.wikipedia.org/w/index.php",
    ]
    params = [None, None, {"title": "Main", "action": "info"}]
    outputs = ["Studio_Ghribli.txt", "Star_Wars.txt", "index.txt"]
    for url, param, output in zip(urls, params, outputs):
        get_html(url, params=param, output="./requesting_urls/" + output)
