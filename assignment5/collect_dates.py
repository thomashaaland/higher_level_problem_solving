import re
from requesting_urls import get_html


def find_dates(html_str, link=True):
    """
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
    """

    # Fetch the webpage
    if link:
        html = get_html(html_str)
    else:
        html = html_str
    
    def replace_month(matchobj):
        """
        Helper function to be used in regex sub. Replaces month with number and 
        formats the output into yyyy/mm/dd format
        Args:
            matchobj :Obj (re): Accepts one argument, which is the regex engine.
        Return:
            :str: Returns the date in yyyy/mm/dd format as a string
        """
        if re.findall(Jan, matchobj.group('month')):
            return matchobj.group('year').zfill(4) + "/01/" + matchobj.group('day').zfill(2)
        if re.findall(Feb, matchobj.group('month')):
            return matchobj.group('year').zfill(4) + "/02/" + matchobj.group('day').zfill(2)
        if re.findall(Mar, matchobj.group('month')):
            return matchobj.group('year').zfill(4) + "/03/" + matchobj.group('day').zfill(2)
        if re.findall(Apr, matchobj.group('month')):
            return matchobj.group('year').zfill(4) + "/04/" + matchobj.group('day').zfill(2)
        if re.findall(May, matchobj.group('month')):
            return matchobj.group('year').zfill(4) + "/05/" + matchobj.group('day').zfill(2)
        if re.findall(June, matchobj.group('month')):
            return matchobj.group('year').zfill(4) + "/06/" + matchobj.group('day').zfill(2)
        if re.findall(July, matchobj.group('month')):
            return matchobj.group('year').zfill(4) + "/07/" + matchobj.group('day').zfill(2)
        if re.findall(Aug, matchobj.group('month')):
            return matchobj.group('year').zfill(4) + "/08/" + matchobj.group('day').zfill(2)
        if re.findall(Sep, matchobj.group('month')):
            return matchobj.group('year').zfill(4) + "/09/" + matchobj.group('day').zfill(2)
        if re.findall(Oct, matchobj.group('month')):
            return matchobj.group('year').zfill(4) + "/10/" + matchobj.group('day').zfill(2)
        if re.findall(Nov, matchobj.group('month')):
            return matchobj.group('year').zfill(4) + "/11/" + matchobj.group('day').zfill(2)
        if re.findall(Dec, matchobj.group('month')):
            return matchobj.group('year').zfill(4) + "/12/" + matchobj.group('day').zfill(2)
        else:
            return "Error: Couldn't find the month"

    
    # Retrieve the base url
    # Require beginning of string 'https://' and match any character except '/'
    # 0 or more times.
    base_url_pattern = r"^https://[^/]*"
    base_url = re.findall(base_url_pattern, html_str)
    if base_url:
        basre_url = base_url[0]
    else:
        base_url = ""
    
    # Make regex for months. Check that it is bounded by nothing
    Jan  = r"\b[jJ]an(?:uary)?\b"
    Feb  = r"\b[fF]eb(?:ruary)?\b"
    Mar  = r"\b[mM]ar(?:ch)?\b"
    Apr  = r"\b[aA]pr(?:il)?\b"
    May  = r"\b[mM]ay\b"
    June = r"\b[jJ]une\b"
    July = r"\b[jJ]uly\b"
    Aug  = r"\b[aA]ug(?:ust)?\b"
    Sep  = r"\b[sS]ep(?:tember)?\b"
    Oct  = r"\b[oO]ct(?:ober)?\b"
    Nov  = r"\b[nN]ov(?:ember)?\b"
    Dec  = r"\b[dD]ec(?:ember)?\b"

    # Compile the months with or
    month = rf"(?:{Jan}|{Feb}|{Mar}|{Apr}|{May}|{June}|{July}|{Aug}|{Oct}|{Nov}|{Dec})"

    # Special case for months ISO
    iso_month_format = r"\b(?:0\d|1[0-2])\b"

    # The day has one digit between 1 and 9, starts with 2 followed by any digit
    # or starts with 3 and has 0 or 1 trailing.
    day = r"(?:\b[1-9]\b|[1-2]\d\b|\b3[0-1]\b)"
    year = r"(?:\b[1-9]\d*\b)"
    
    # Compile for the four different cases
    dmy = rf"{day}\s{month}\s{year}"
    mdy = rf"{month}\s{day},\s{year}"
    ymd = rf"{year}\s{month}\s{day}"
    iso = rf"{year}-{iso_month_format}-{day}"

    
    dates = []
    dmy_dates = re.findall(dmy, html)
    mdy_dates = re.findall(mdy, html)
    ymd_dates = re.findall(ymd, html)
    iso_dates = re.findall(iso, html)

    # regex pattern for grabbing day, month and year from dmy
    # Ensure beginning of line, grab digits until space and group as day
    # then grab a word until space and name month
    # finally grab digits until end of line and name year
    dmy_group_pattern = r"\b(?P<day>\d+)\s(?P<month>\w+)\s(?P<year>\d+)\b"
    # Works as before, but first month, then day separated by comma space and year
    mdy_group_pattern = r"\b(?P<month>\w+)\s(?P<day>\d+),\s(?P<year>\d+)\b"
    # Similar to dmy but first year, month then day
    ymd_group_pattern = r"\b(?P<year>\d+)\s(?P<month>\w+)\s(?P<day>\d+)\b"
    # ISO looks for 4 digits - 2 digits - 2 digits in yyyy-mm-dd format.
    # Need only find and replace '-'
    iso_group_pattern = r"-"

    # Substitute dates to fit yyyy/mm/dd
    dmy_dates = [re.sub(dmy_group_pattern,
                        replace_month,
                        dmy_date) for dmy_date in dmy_dates]
    mdy_dates = [re.sub(mdy_group_pattern,
                        replace_month,
                        mdy_date) for mdy_date in mdy_dates]
    ymd_dates = [re.sub(ymd_group_pattern,
                        replace_month,
                        ymd_date) for ymd_date in ymd_dates]
    iso_dates = [re.sub(iso_group_pattern,
                        '/',
                        iso_date) for iso_date in iso_dates]
    dates = dmy_dates + mdy_dates + ymd_dates + iso_dates

    return dates

if __name__ == "__main__":
    # Test websites
    websites = [r"https://en.wikipedia.org/wiki/J._K._Rowling",
                r"https://en.wikipedia.org/wiki/Richard_Feynman",
                r"https://en.wikipedia.org/wiki/Hans_Rosling"]
    # Output files for the test sites
    outputs = ["dates_rowling.txt", "dates_feynman.txt", "dates_rosling.txt"]

    
    for site, output in zip(websites, outputs):
        print(f"Writing file {output} for site {site}")
        with open("./requesting_urls/" + output, 'w') as f:
            for date in sorted(find_dates(site)):
                f.write(date + '\n')
        print(f"Finished write {output}")
    print("Done")
