import functools
import requests
import threading
import time

from collections import deque

from filter_urls import find_articles
from requesting_urls import get_html


def time_dec(func):
    """Decorator for measuring time. Decorated 
    function will display its runtime.
    Args:
       func :function: The function to be timed
    Returns:
       :function: returns the function to be used
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        value = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Time elapsed for function {func.__name__}: {end - start}")
        return value
    return wrapper

@time_dec
def bfs(candidates, visited, end_url):
    """Search trying to find the end_url. 
    Breadth First Search for searching graphs. Searches the links
    avoiding going deep. Searches all links on first page, then all links
    on all second pages and so on. If nothing is found returns None, 
    otherwise returns a list of the shortest path found.
    Args:
        candidates :deque: A double ended queue. Here functions as a 
           queue to enable the breadth first algorithm. Doubles as a 
           container for the quickest route and possible candidate sites.
           Contains tuples to save memory.
        visited :set: A set containing all visited paths.
        end_url :str: The goal url. Returns a tuple of the quickest
           route from the start url to the end url.
    """

    def run_get_html(current, current_sites, process_number):
        """Run function for parallelising requesting urls. 
        Need to be able to catch and handle some exceptions due
        to connection problems.
        Args:
            current :str: An url to be processed.
            current_sites :list [str]: A list where the extracted 
                html is to be returned to the rest of the program
                as a side-effect.
            process_number :int: This process's id.
        Returns:
            None
        """
        try:
            current_site = get_html(current)
            current_sites[process_number] = current_site
        except requests.exceptions.RequestException as e:
            print(f"Could not load website {current}. {e}.")
        
            
    @time_dec
    def threaded_get_html(candidates, visited, num_processes = 256):
        """Helper function for running parallelised html request. This
        function sets up and controls the parallelising. 
        Args:
            candidates :deque: A deque with tuples. The candidates are 
                sites which has been seen but not yet filtered for urls. 
            visited :set: A set of visited websites.
            num_processes :int: The maximum number of processes which 
                will be started during parallelisation.
        Returns:
            current_sites :list (str): A list of all the extracted html.
                Element is None if something went wrong. We want to go 
                around a broken site.
            current_paths :list (tuple): A list of the paths taken by
                the sites extracted. Element is None if something went 
                wrong with that particular site.
        """
        # Number of processes
        # Should not be greater than the number of candidates
        num_processes = min(len(candidates), num_processes)
        
        #Introduce mutable container
        threads = [None]*num_processes
        current_sites = [None]*num_processes
        current_paths = [None]*num_processes

        # This part is the slowest
        # This has been threaded for speed
        for i in range(len(threads)):
            # Unpack the current site. Pop from candidates since this site no
            # longer is a candidate
            current_paths[i] = candidates.popleft()
            current = current_paths[i][0]

            # Check if we have been here before
            if current not in visited:
                
                # Visited register that we have visited this site
                visited.add(current)

                # Thread_get_html modifies current sites only
                threads[i] = threading.Thread(target=run_get_html,
                                              args=(current, current_sites, i))
                threads[i].start()

        # Join the threads before continuing
        for i in range(len(threads)):
            if threads[i]:
                threads[i].join()
                
        # Done, return
        return current_sites, current_paths
        
        
    # popleft: removes and returns left
    # append: appends to the right
    # Start BFS using a deque as a queue to generate the breadth first search
    # Run for as long as there are possible candidates to look at.
    while candidates:
        # Time the loop for convenience.
        start_while = time.perf_counter()
        # Perform threaded site fetching
        current_sites, current_paths = threaded_get_html(candidates, visited)

        # Now run through all the fetched html and extract links
        # This is also a great candidate for paralellising
        for current_site, current_path in zip(current_sites, current_paths):
            # Make a quick check if the html was successfully extracted
            if not current_site:
                continue
            # Give some status updates to show progress
            print("Length of path:", len(current_path))
            [print(path) for path in current_path]
            # Find the links from the html. Call these links new candidates
            new_candidates = find_articles(current_site, ok_sites=["en"])
            # Append new paths
            for new in new_candidates:
                # Check if we have been here before
                if new in visited:
                    continue
                # Create new tuple to expand path
                new_path = (new, *current_path)
                # Check if we found the end url
                if new == end_url:
                    return new_path
                # Append the new candidates
                candidates.append(new_path)
            # Summary with the time for reference
            end_while = time.perf_counter()
            print(f"Time elapsed for whole loop: {end_while - start_while}")
    print("Target site not found.")
    return ("Target site not found.")
    
def init_search(start_url, end_url):
    """Starter function for search. Calls Breadth First Search algorithm since 
    websites are not weighted graphs and all vertices has the same cost.
    Args:
        start_url :str: The starting website to find the path to the end website
        end_url :str: The target url. 
    Returns:
        :tuple: Returns a tuple with the traversed sites, including destination 
            and starting site.
    """
    candidate_paths = deque([])
    visited = set()
    candidate_paths.append((start_url,))
    return bfs(candidate_paths, visited, end_url)
    

def main():
    # Some possible starting and target sites.
    start_url = "https://en.wikipedia.org/wiki/Parque_18_de_marzo_de_1938"
    end_url = "https://en.wikipedia.org/wiki/Bill_Mundell"
    easy_end_url = "https://en.wikipedia.org/wiki/Stadium"
    medium_end_url = "https://en.wikipedia.org/wiki/Pausanias_of_Athens"

    panzerpappa = "https://en.wikipedia.org/wiki/Panzerpappa"
    pompeii = "https://en.wikipedia.org/wiki/Pompeii"

    covid19 = "https://en.wikipedia.org/wiki/COVID-19"
    peter_singer = "https://en.wikipedia.org/wiki/Peter_Singer"

    stovner = "https://en.wikipedia.org/wiki/Stovner"
    hackingtosh = "https://en.wikipedia.org/wiki/Hackintosh"

    # Start the search
    result = init_search(start_url, end_url)
    outfile = "./wiki_race_challenge/shortest_way.txt"
    
    with open(outfile, 'w') as f:
        f.write("The shortest path was found to be:\n")
        for r in result:
            f.write(r)
            f.write('\n')
    
    print("-"*50)
    print(f"The shortest path was found to be: ")
    [print(r) for r in result]
    
if __name__ == "__main__":
    main()
