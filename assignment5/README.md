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

#### 5.3 `collect_dates.py`

This script if run as main downloads the three sites [J. K. Rowling](https://en.wikipedia.org/wiki/J._K._Rowling), [Richard Feynman](https://en.wikipedia.org/wiki/Richard_Feynman) and [Hans Rosling](https://en.wikipedia.org/wiki/Hans_Rosling) and writes three files [dates_rowling.txt](./requesting_urls/dates_rowling.txt), [dates_feynman.txt](./requesting_urls/dates_feynman.txt) and [dates_rosling.txt](./requesting_urls/dates_rosling.txt).

There is one function `collect_dates.find_dates` which accepts either a url or a html string. It finds all dates in the page and returns it as a list of dates in the yyyy/mm/dd format.

#### 5.4 `time_planner.py`

This script if run as main downloads events from [FIS Alpine Ski World Cup](https://en.wikipedia.org/wiki/2021%E2%80%9322_FIS_Alpine_Ski_World_Cup) and creates an empty betting slip.

There are two functions. The first function `time_planner.extract_events` accepts an url and extracts the date, venue and discipline for skiing.

The second function `time_planner.create_betting_slip` accepts events in the above format and saves a betting slip.

#### 5.5 `fetch_player_statistics.py`

If this script is run as main performs doctests and then plots the statistics points per game, blocks per game and rebounds per game for the three best players (measured by the most points per game) in the teams which reached the conference semi-finals. These statistics are saved in [players_over_PPG.png](./NBA_player_statistics/players_over_PPG.png), [players_over_BPG.png](./NBA_player_statistics/players_over_BPG.png) and [players_over_RPG.png](./NBA_player_statistics/players_over_RPG.png).

There are four functions. The function `fetch_player_statistics.extract_teams` accepts no arguments and extracts the name and url of the teams which reached the conference semi-finals.

The function `fetch_player_statistics.extract_players` takes in a url to a team and extract the name and url of all the players on that team.

The function `fetch_player_statistics.extract_player_statistics` accepts a player url and extracts the PPG, BPG and RPG statistics for that player.

Finally, `fetch_player_statistics.plot_NBA_player_statistics` takes a nested dictionary with teams as first key, a player as second key and a statistic as third key and plots the stats for these teams and players.

#### 5.6 `wiki_race_callenge.py`

When run as main this script finds the shortest route between the wikipedia pages [Parque 18 de marzo de 1938](https://en.wikipedia.org/wiki/Parque_18_de_marzo_de_1938) and [Bill Mundell](https://en.wikipedia.org/wiki/Bill_Mundell).

This script has 4 functions. The function `wiki_race_challenge.time_dec` is a decorator which adds timing functionality to functions it decorates.

The function `wiki_race_challenge.bfs` is a function which uses Breadth First Search algorithm to find the shortest path between none-weighted links to webpages. The shortest path is returned as a tuple of the sites needed to navigate to the final target site.

The function `init_search` is the function called to start the search. It simply takes the start url and the end url and returns the shortest path as a tuple.

The function `wiki_race_challange.main` is called when the script is run as main.

### Missing Functionality

Lacks proper tests for `time_planner.py`.

### Usage

You need to install dependencies first. You can build a virtual environment using the [requirements.txt](requirements.txt) file.

Some tests can be run using `py.test`. Additionally there are tests in the docs for all scripts except `time_planner.py`. To use simply use `python scrip.py` from terminal. Doing this creates the example output found in the folders where applicable.

To run as imported functions you can for example use `from requesting_urls import get_html` to import a function which fetches a html page of your choice and returns it as a string.

The following functions can be imported and are ready to be used with simple user interfaces.

`>>> from requesting_urls import`
* `get_html(url, params=None, output=None)`

`>>> from filter_urls import`
* `find_urls(html_str, base_url="", output=None)`
* `find_articles(html_str, output=None, ok_sites=["en", "no"], selected_language="en")`

`>>> from collect_dates import`
* `find_dates(html_str, link=True)`

`>>> from fetch_player_statistics import`
* `extract_teams()`
* `extract_players(team_url)`
* `extract_player_statistics(player_url)`

`>>> from wiki_race_challenge import`
* `init_search(start_url, end_url)`

#### `get_html(url, params=None, output=None)`
```python
    Reads a web adresss and returns its content as text.
    If you supply parameters, filters based on those.
    If output is supplied writes file to disk.

    Args:
        url :str: The url to the website to be read.
        params :dict: parameters to filter with.
        output :str: Need *.txt suffix. A file to write to.

    Retuns:
        :str: the website as a string.
```

#### `find_urls(html_str, base_url="", output=None)`
```python
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
```

#### `find_articles(html_str, output=None, ok_sites=["en", "no"], selected_language="en")`
```python
    Given a link to a webpage this function returns links to 
    (english and norvegian) wikipedia articles from that page.
    Args:
        html_str :str: A link to a website as a string.
        output :str: Optional argument for writing results to file.
        ok_sites :list (str): A list of languages accepted when 
            finding wikipedia articles.
        selected_language :str: Optional argument to specify the language 
            of the base url (Assumes the base url is a wikipedia article).
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
```

#### `find_dates(html_str, link=True)`
```
    Finds dates on a webpage.

    The returned list is in the format yyyy/mm/dd

    The following formats are considered when searching :
    12 DMY: 13 Oct(ober) 2020
    13 MDY: Oct(ober) 13 , 2020
    14 YMD: 2020 Oct(ober) 13
    15 ISO: 2020-10-13
    
    Args:
        html_str :str: A link to a website as a string
        link :bool: If set to true html_str is a link. Otherwise it 
            is raw html as a string.
    Returns:
        :list (str): A list of all dates found on the website formatted as 
        yyyy/mm/dd
```

#### `extract_teams()`
    ```python
    Extract team names and urls from the NBA Playoff 'Bracket'
    section table.

    Returns:
       team_names (list): A list of team names that made it to the 
       conference semifinals.
       team_urls (list): A list of absolute Wikipedia urls
       corresponding to team_names.
    ```


#### `extract_players(team_url)`
```python
    Extract players that played for a specific team in the NBA
    playoffs.

    Args:
        team_url (str): URL to the wikipedia article of the season
            of a given team.

    Returns:
        player_names (list): A list of players names corresponding
            to the team whos URL was passed.
        player_urls (list): A list of Wikipedia URLs corresponding 
            to player_names of the team whos URL was passed.
    
Example:
    >>> example_team = 'https://en.wikipedia.org/wiki/Toronto_Raptors'
    >>> extract_players(example_team)
    (['Precious Achiuwa', 'Anunoby', 'Dalano Banton', 'Scottie Barnes', 'Khem Birch', 'Isaac Bonga', 'Chris Boucher', 'Justin Champagnie', 'Sam Dekker', 'Goran Dragi', 'Malachi Flynn', 'David Johnson', 'Sviatoslav Mykhailiuk', 'Pascal Siakam', 'Gary Trent Jr.', 'Fred Van Vleet', 'Yuta Watanabe'], ['https://en.wikipedia.org/wiki/Precious_Achiuwa', 'https://en.wikipedia.org/wiki/OG_Anunoby', 'https://en.wikipedia.org/wiki/Dalano_Banton', 'https://en.wikipedia.org/wiki/Scottie_Barnes', 'https://en.wikipedia.org/wiki/Khem_Birch', 'https://en.wikipedia.org/wiki/Isaac_Bonga', 'https://en.wikipedia.org/wiki/Chris_Boucher_(basketball)', 'https://en.wikipedia.org/wiki/Justin_Champagnie', 'https://en.wikipedia.org/wiki/Sam_Dekker', 'https://en.wikipedia.org/wiki/Goran_Dragi%C4%87', 'https://en.wikipedia.org/wiki/Malachi_Flynn', 'https://en.wikipedia.org/wiki/David_Johnson_(basketball)', 'https://en.wikipedia.org/wiki/Sviatoslav_Mykhailiuk', 'https://en.wikipedia.org/wiki/Pascal_Siakam', 'https://en.wikipedia.org/wiki/Gary_Trent_Jr.', 'https://en.wikipedia.org/wiki/Fred_VanVleet', 'https://en.wikipedia.org/wiki/Yuta_Watanabe'])
    ```

#### `extract_player_statistics(player_url)`
    ```python
    Extract player statistics for NBA player.

    Args:
        player_url (str): URL to the Wikipedia article of a player.

    Returns:
        A tuple with the elements
        ppg (float): Points per Game
        bpg (float): Blocks per Game
        rpg (float): Rebounds per Game

Example:
    >>> example_player = 'https://en.wikipedia.org/wiki/Kyrie_Irving'
    >>> extract_player_statistics(example_player)
    (22.8, 0.4, 3.8)
    ```

#### `init_search(start_url, end_url)`
    ```python
    Starter function for search. Calls Breadth First Search algorithm since 
    websites are not weighted graphs and all vertices has the same cost.
    Args:
        start_url :str: The starting website to find the path to the end website
        end_url :str: The target url. 
    Returns:
        :tuple: Returns a tuple with the traversed sites, including destination 
            and starting site.
    ```