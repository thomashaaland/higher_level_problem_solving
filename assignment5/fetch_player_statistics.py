from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import requests as req
import re
from requesting_urls import get_html
from filter_urls import find_urls

def extract_teams():
    """Extract team names and urls from the NBA Playoff 'Bracket'
    section table.

    Returns:
       team_names (list): A list of team names that made it to the 
       conference semifinals.
       team_urls (list): A list of absolute Wikipedia urls
       corresponding to team_names.
    """

    # get html using for example get_html from requesting_urls
    url = "https://en.wikipedia.org/wiki/2021_NBA_playoffs"
    html = get_html(url)
    
    # keep base url
    base_url = "https://en.wikipedia.org"

    # create soup
    soup = BeautifulSoup(html, "html.parser")
    # find bracket we are interested in
    bracket_header = soup.find(id="Bracket")
    bracket_table = bracket_header.find_next("table")
    rows = bracket_table.find_all("tr")

    # create list of teams
    team_list = []

    # indices used in the teams table
    seed = 0
    name = 1
    won = 2
    
    for i in range(len(rows)):
        cells = rows[i].find_all("td")
        cells_text = [cell.get_text(strip=True) for cell in cells]

        # Filter out of the cells that are empty
        cells_text = [cell for cell in cells_text if cell]

        # Find the rows that contain seeding, team name and games won
        if len(cells_text) > 1 and len(cells_text)< 4:
            # Use regex to remove the star demarking the winner
            t_name = re.sub(r"\*", r"", cells_text[name])
            team_list.append(t_name)

    # Filter out the team that appear more than once, which means they made it
    # to the conference semifinals
    teams = {team:0 for team in team_list}
    for team in team_list:
        teams[team] += 1
    
    team_list_filtered = {team for team in team_list if teams[team] > 1}
    
    # Create lists of the team names and urls to the team website
    team_names = []
    team_urls = []

    # your code
    for row in rows:
        for team_name in team_list_filtered:
            # find the link paragraph
            link_paragraph = re.findall(rf"<a.*>{team_name}.*", str(row))
            # If link is found and the team hasn't already been added
            if link_paragraph and team_name not in team_names:
                # Find the link itself
                link = find_urls(str(link_paragraph), base_url = base_url)
                team_names.append(team_name)
                team_urls.append(*link)

    return team_names, team_urls

def extract_players(team_url):
    """Extract players that played for a specific team in the NBA
    playoffs.

    Args:
        team_url (str): URL to the wikipedia article of the season
            of a given team.

    Returns:
        player_names (list): A list of players names corresponding
            to the team whos URL was passed.
        player_urls (list): A list of Wikipedia URLs corresponding 
            to player_names of the team whos URL was passed.
    """

    # keep base url
    base_url = "https://en.wikipedia.org"

    # get html for each page using the team url you extracted before
    html = get_html(team_url)

    # make soup
    soup = BeautifulSoup(html, "html.parser")
    # get the header of the Roster
    roster_header = soup.find(id="Roster")
    # identify table
    roster_table = roster_header.find_next("table")
    rows = roster_table.find_all("tr")

    # prepare lists for player names and urls
    player_names = []
    player_urls = []

    # Run through the rows to grab url and name of each player
    for i in range(0, len(rows)):
        cells = rows[i].find_all("td")
        cells_text = [cell.get_text(strip=True) for cell in cells]
        if len(cells_text) == 7:
            rel_url = cells[2].find_next("a").attrs["href"]
            # Use regex to remove information in paranthesis
            # It create one group for everything at the beginning and
            # one non-capturing group for the rest starting with '_('
            # until the end OR everything. This creates a tuple which
            # needs to be joined with the empty string ''.
            # Fetch the name. Group words starting with a capital letter
            # followed by any number of one or more lowercase letter.
            reg_fetch_name = r"(?:[A-Z][a-z]+)"
            # Create urls and name to each player
            # Need to join inner tuple with the empty string ''
            # Need to join list with one space.
            name = ' '.join(re.findall(reg_fetch_name, rel_url))
            # need to create absolute urls combining the base and
            # the relative url
            player_urls.append(base_url + rel_url)
            player_names.append(name)

    return player_names, player_urls

def extract_player_statistics(player_url):
    """Extract player statistics for NBA player.

    Args:
        player_url (str): URL to the Wikipedia article of a player.

    Returns:
        ppg (float): Points per Game
        bpg (float): Blocks per Game
        rpg (float): Rebounds per Game
    """
    # As some players have incomplete statistics/information, let's
    # set a default score.

    ppg = 0.
    bpg = 0.
    rpg = 0.

    # get html
    html = get_html(player_url)

    # make soup
    soup = BeautifulSoup(html, "html.parser")

    # find header of NBA career statistics
    nba_header = soup.find(id="Career_statistics")

    # Check for a few alternative names of header
    if nba_header is None:
        nba_header = soup.find(id="NBA_career_statistics")
    
    # check for alternate name of header
    if nba_header is None:
        nba_header = soup.find(id="NBA")
        
    
    try:
        # find regular season header
        # You might want to check for different spellings, e.g. capitalization
        # You also want to take into account the different orders
        # of header and table
        # Also make sure the regular season table is found.
        try:
            regular_season_header = nba_header.find_next(id="Regular_season")
            assert regular_season_header is not None
        except:
            return ppg, bpg, rpg

        # next we should identify the table
        nba_table = regular_season_header.find_next("table")
                
    except:
        try:
            # Table might be right after NBA career statistics header
            nba_table = nba_header.find_next("table")
        except:
            return ppg, bpg, rpg

    
    # find nba table header and extract rows
    table_header = nba_table.find_all("th")
    table_rows = nba_table.find_all("tr")
    rows = [row.find_all("td") for row in table_rows if row.find_all("td")]

    # Extract the scores from the different categories
    # Be sure that some values were extracted or return just 0's
    try:
        scores = [row for row in rows if row[0].text.strip('\n') == "Career"]
        scores = scores[0]
    except:
        return ppg, bpg, rpg
        
    # The row name can span more than one column
    ind_diff = len(table_header) - len(scores)

    # find the columns for the different categories
    col_ind = {col.text.strip('\n'):(i - ind_diff) for i, col in enumerate(table_header)}
    ppg_column = col_ind["PPG"]
    bpg_column = col_ind["BPG"]
    rpg_column = col_ind["RPG"]

    # Convert the scores extracted to floats
    # Note: In some cases the scores are not defined but only
    # shown as '-'. In such cases let's set the score to 0 ot None
    for i in (ppg_column, bpg_column, rpg_column):
        try:
            scores[i] = float(scores[i].text.strip('\n'))
        except ValueError:
            scores[i] = 0.0
    ppg, bpg, rpg = scores[ppg_column], scores[bpg_column], scores[rpg_column]
    
    return ppg, bpg, rpg

# A matplotlib color for each team name
# (could be a name or a #rrggbb web color string)
color_table = {
    "Philadelphia": "#0328fc",
    "Atlanta": "#fc0303",
    "Milwaukee":"#005e3a",
    "Brooklyn":"#000000",
    "Phoenix":"#ff6f00",
    "Utah":"#00186e",
    "LA Clippers":"#ff4800",
    "Denver":"#001438"
    }

def plot_NBA_player_statistics(teams, stat = "PPG"):
    """Plot NBA player statistics. Makes a bar plot.
    Args: 
        teams (dict): 3 nested dictionaries has statistics for some teams. 
            The key is a team name and the value is a new dictionary. This 
            dictionary has player names as keys and a final dictionary as value. 
            This last dictionary has 'PPG', 'BPG' and 'RPG' keys for 'Points per
            game', 'Blocks per game' and 'Rebounds per game'
        stat (string): Determines which stat to plot.
    """
    # Change the width to make the plots easier to read
    plt.rcParams["figure.figsize"] = (15,6)
    count_so_far = 0
    all_names = []

    # iterate through each team and the
    for team in teams:
        players = teams[team]
        
        # pick the color for the team from the table above
        color = color_table[team]
        
        # Collect the ppg and name of each player on the team
        # you'll want to repeat with other stats as well
        data = []
        names = []
        for player in teams[team]:
            player_stats = players[player]
            names.append(player)
            data.append(player_stats[stat])
        # record all the names, for use later in x label
        all_names.extend(names)

        # the position of bars is shifted by the number of players
        # so far
        x = range(count_so_far, count_so_far + len(players))
        #count_so_far += len(players)
        count_so_far += len(players)
        # Make bars for this team's players ppg,
        # with the team name as the label
        bars = plt.bar(x, data, color=color, label=team)
        # add the value as text on the bars
        plt.bar_label(bars)

    # use the names, rotated 90 degrees as the labels for the bars
    plt.xticks(range(len(all_names)), all_names, rotation=90)
    # add the legend with the colors for each team
    plt.legend(loc=0)
    # turn off gridlines
    plt.grid(False)
    # set the title, xlabel and ylabel
    title_dict = {"PPG":"Points per game",
                  "BPG":"Blocks per game",
                  "RPG":"Rebounds per game"}
    plt.title(title_dict[stat])
    plt.xlabel("Player")
    plt.ylabel("Score")
    # Ensure the layout is tight and nothing spills out or overlaps
    plt.tight_layout()
    # Save the figure to a file
    plt.savefig("./NBA_player_statistics/players_over_" + stat.lower() + ".png")

if __name__ =="__main__":
    # Extract teams along their urls
    teams, team_urls = extract_teams()
    # Make a dictionary to hold all the teams
    league_dict = {}
    # Iterate through all teams
    for team, team_url in zip(teams, team_urls):
        # Produce something to indicate progress
        print(team)
        print("-"*40)
        # Extract player names along with their url for this team
        player_names, player_urls = extract_players(team_url)
        # Make a dictionary to hold each player for this team
        players_dict = {}
        player_scores = []
        # Iterate through each player to grab their stats
        for player_name, player_url in zip(player_names, player_urls):
            # Grab stats for this player
            ppg, bpg, rpg = extract_player_statistics(player_url)
            # Save the stats in a dictionary
            player_dict = {"PPG":ppg, "BPG":bpg, "RPG":rpg}
            player_scores.append((player_name, player_dict))
            #print(player_name)
            
        # Fill player dictionary with the 3 best players
        player_scores.sort(key = lambda x: x[1]["PPG"])
        for player_name, player_stats in player_scores[-3:]:
            players_dict[player_name] = player_stats

            
        # Fill the league dictionary with statted players
        league_dict[team] = players_dict
    # Plot each stat
    plot_NBA_player_statistics(league_dict, "PPG")
    plot_NBA_player_statistics(league_dict, "BPG")
    plot_NBA_player_statistics(league_dict, "RPG")


