import requests
import json
from IPython.display import Image
from IPython.display import display
from IPython.core.display import HTML
"""
demo_key = "DEMO_KEY"

url = "https://api.nasa.gov/planetary/apod?api_key=" + demo_key

response = requests.get(url)

data = response.json()

print(response.json()["explanation"])
Image(url=data["url"], width=600)
"""

"""
url = "https://api.kanye.rest/"

r = requests.get(url)
data = r.json()

print(data)
"""

stop_id = 5926

__version__ = "0.5.1"

ENTUR_CLIENT_ID = __version__

ENTUR_GRAPHQL_ENDPOINT = "https://api.entur.io/journey-planner/v2/graphql"

ENTUR_GRAPHQL_QUERY = """
{
  stopPlace(id: "NSR:StopPlace:5926") {
    name
    estimatedCalls(timeRange: 72100, numberOfDepartures: 20) {
      expectedArrivalTime
      realtime
      destinationDisplay {
        frontText
      }
      serviceJourney {
        directionType
        line {
          publicCode
        }
      }
    }
  }
}
"""

headers = {
    "Accept": "application/json",
    "ET-Client-Name": "UIO:IN3110 - ingeborggjerde",
    "ET-Client-Id": ENTUR_CLIENT_ID,
    }

qry = ENTUR_GRAPHQL_QUERY % dict(stop_id=stop_id)
res = requests.post(
    ENTUR_GRAPHQL_ENDPOINT,
    headers=headers,
    timeout=5,
    json=dict(query=qry, variables={}),
    )

print(res.json()["data"]["stopPlace"]["estimatedCalls"])
