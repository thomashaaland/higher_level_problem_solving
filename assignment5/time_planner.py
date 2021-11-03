from bs4 import BeautifulSoup
import requests as req
import re
import os
from requesting_urls import get_html
from collect_dates import find_dates

def extract_events(url):
    """Extract date, venue and discipline for competitions.
    Docs
    Args:
        url (str): The url to extract the events from.
    Returns:
        table_info (list of lists): A nested list where the rows
     represent each race date, and the columns are [date, venue,
    discipline].
    """

    # Dictionary of the disciplines and their abbreviations
    discipline_dict = {
        "DH": "Downhill",
        "SL": "Slalom",
        "GS": "Giant Slalom",
        "SG": "Super Giant Slalom",
        "AC": "Alpine Combined",
        "PG": "Parallel Giant Slalom",
        }

    # Get the html
    html = get_html(url)

    # make soup
    soup = BeautifulSoup(html, "html.parser")

    # Find the tag that contains the Calendar header span
    calendar_header = soup.find(id="Calendar")

    # Find the following table
    calendar_tables = calendar_header.find_all_next("table")
    calendar_table = calendar_tables[0]

    #print(calendar_table)
    dates = find_dates(str(calendar_table), link=False)
    
    # Find the rows of the first table
    rows = calendar_table.find_all("tr")
    cols = rows[0].find_all("th")
    # Use dictionary comprehension to assign index to column name
    # use col_2_index["Event"] --> index for Event column
    # The regext uses an unbound group to skip table header and capture
    # group every word and '#' characters, stopping if meeting special
    # characters such as 'newline' or '<' characters
    col_2_index = {re.findall(r"(?:<th.*>)([#\w]+)", str(col))[0]:i
                   for i, col in enumerate(cols)}
    
    # try parsing the row of 'th' cells to identify the indices
    # for Event, Venue, and Type (discipline)

    found_event = None
    found_date = None
    found_venue = None
    found_discipline = None
    # Saving all necessary values in the list under
    events = []

    # How many columns does a full row have?
    full_row_length = len(cols)
    # some rows have fewer because the 'venue'
    # spans multiple rows,
    # short_row_length means a repeated venue, which
    # should be reused from the previous iteration
    short_row_length = full_row_length - 2
    venue_span_rows = 0

    for row in rows:        
        cells = row.find_all("td")

        
        # some rows have one number of columns,
        # if it's a different number (usually 0 or 1),
        # ignore it
        if len(cells) not in range(short_row_length, full_row_length + 1):
            # skip rows that don't have most columns
            continue
        
        event = cells[col_2_index["Event"]]
        # An event seems to always be a 1-3 digit number,
        # so we can check that we have an event with a sumple regex
        if re.match(r"\d{1,3}", event.text.strip()):
            found_event = event.text.strip()
        else:
            found_event = None

        if len(cells) == full_row_length:
            # If event is cancelled, the index below might need to
            # be shifted
            venue_cell = cells[col_2_index["Venue"]]
            found_venue = venue_cell.text.strip()
            discipline_index = col_2_index["Type"]
        else:
            # repeated venue, discipline is in a different column
            # where is the discipline column?
            discipline_index = col_2_index["Type"] - (full_row_length - len(cells))

        discipline = cells[discipline_index]
        # find the discipline id
        # can you make a regex to find only the keys of the
        # disciplines dictionary?
        # (DH|...)
        discipline_regex = r"(DH|SL|GS|SG|PG)"
        # this can also be done with just HTML parsing
        discipline_match = re.search(discipline_regex, discipline.text.strip())
        if discipline_match:
            # look up the full discipline name
            disc = re.findall(discipline_regex, discipline.text.strip())[0]
            found_discipline = discipline_dict[disc]
        else:
            found_discipline = None
        if all([found_venue, found_event, found_discipline]):
            # if we found something
            events.append((found_event, dates[int(found_event) - 1], found_venue, found_discipline))
        
    return events

def create_betting_slip(events, save_as):
    """Saves a markdown format betting slip to the location 
    './datetime_filter/<save_as>.md'.
    Args:
        events (list): takes a list of 3-tuples containing
            date, venue and type for each event.
        save_as (string): filename to save the markdown 
            betting slip.
    """

    # Ensure directory exists
    os.makedirs("datetime_filter", exist_ok=True)

    with open(f"./datetime_filter/{save_as}.md", "w") as out_file:
        out_file.write(f"# BETTING SLIP ({save_as})\n\nName:\n\n")
        out_file.write("Date | Venue | Discipline | Who wins?\n")
        out_file.write(" --- | --- | --- | --- \n")
        for e in events:
            event, date, venue, type = e
            out_file.write(f"{date} | {venue} | {type} | \n")

def main():
    adress = "https://en.wikipedia.org/wiki/2021%E2%80%9322_FIS_Alpine_Ski_World_Cup"
    events = extract_events(adress)
    for event in events:
        print(event)
    create_betting_slip(events, "betting_slip_empty")

if __name__ == "__main__":
    main()
