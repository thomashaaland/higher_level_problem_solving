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
* `from requesting_urls import`
** `get_html(url, params=None, output=None)`
* `from filter_urls import`
** `find_urls(html_str, base_url="", output=None)
** `find_articles(html_str, output=None, ok_sites=["en", "no"], selected_language="en")