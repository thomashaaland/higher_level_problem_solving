# README.md Assignment5

## Task 5

### Prerequisites

version = python 3.9.7

List of required packages is found in [requirements.txt](./requirements.txt).

#### Tested on the following platforms
* Operating system: Ubuntu 20.04.3 LTS
  	    Kernel: Linux 5.11.0-37-generic

### Functionality

#### 5.1 `requesting_url.py`

The script if run as main downloads the threee websites [Studio Ghibli](https://en.wikipedia.org/wiki/Studio_Ghibli), [Star Wars](https://en.wikipedia.org/wiki/Star_Wars) and [Wikipedia main info page](https://en.wikipedia.org/w/index.php?title=Main_Page&action=info) and saves them as [Studio_Ghribli.txt](./requesting_urls/Studio_Ghribli.txt), [Star_Wars.txt](./requesting_urls/Studio_Ghribli.txt) and [index.txt](./requesting_urls/index.txt).


The function `requesting_url.get_html` accepts an url to a website an option to include parameters and an option to include an output path. It accepts the url and downloads the webpage. It can save the page as a `*.txt` file.

#### 5.2 `filter_urls.py`

The script if run as main runs doctests. It also downloads and finds links from the three urls
[Studio Ghibli](https://en.wikipedia.org/wiki/Studio_Ghibli), [Star Wars](https://en.wikipedia.org/wiki/Star_Wars) and [Wikipedia main info page](https://en.wikipedia.org/w/index.php?title=Main_Page&action=info) and saves the files [html_Studio_Ghribli.txt](./requesting_urls/html_Studio_Ghribli.txt), [html_Star_Wars.txt](./requesting_urls/html_Studio_Ghribli.txt), [html_index.txt](./requesting_urls/html_index.txt), [wiki_article_Studio_Ghribli.txt](./requesting_urls/wiki_article_Studio_Ghribli.txt), [wiki_article_Star_Wars.txt](./requesting_urls/wiki_article_Studio_Ghribli.txt), [wiki_article_index.txt](./requesting_urls/wiki_article_index.txt). It includes two functions.

The function `filter_urls.find_urls` accepts a html string and finds all urls, with the caveat the link is in a tag (and not in other contexts). It handles partial urls if it is given the base url.

The function `filter_urls.find_articles` find links from a website which links to wikipedia articles. Only works properly for english wikipedia articles.

#### 5.2 `collect_dates.py`

This script if run as main downloads the three sites [J. K. Rowling](https://en.wikipedia.org/wiki/J._K._Rowling), [Richard Feynman](https://en.wikipedia.org/wiki/Richard_Feynman) and [Hans Rosling](https://en.wikipedia.org/wiki/Hans_Rosling) and writes three files [dates_rowling.txt](./requesting_urls/dates_rowling.txt), [dates_feynman.txt](./requesting_urls/dates_feynman.txt) and [dates_rosling.txt](./requesting_urls/dates_rosling.txt).

There is one function `collect_dates.find_dates` which accepts either a url or a html string. It finds all dates in the page and returns it as a list of dates in the yyyy/mm/dd format.

#### 5.3 ``

### Missing Functionality

### Usage


