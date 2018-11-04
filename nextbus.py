import http.client, json, sys
from difflib import SequenceMatcher

diff = lambda a, b: SequenceMatcher(None, a, b).ratio()

try:
    if len(sys.argv) != 4: raise ValueError
    
    _, route, stop, direction = sys.argv

    conn = http.client.HTTPConnection('svc.metrotransit.org')
    conn.request("GET", "/NexTrip/Routes?format=json")
    res = conn.getresponse()
    data = json.loads(res.read())
    
    for item in data:
        if route == item['Description']:
            route = item['Route']

    directions = {
            'SOUTH' : '1',
            'EAST'  : '2',
            'WEST'  : '3',
            'NORTH' : '4'
    }

    direction = directions[direction.upper()]

    conn = http.client.HTTPConnection('svc.metrotransit.org')
    conn.request('GET', f'/NexTrip/Stops/{route}/{direction}?format=json')
    res = conn.getresponse()
    data = json.loads(res.read())

    for item in data:
        if stop == item['Text']:
            stop = item['Value']
    
    conn = http.client.HTTPConnection('svc.metrotransit.org')
    conn.request('GET', f'/NexTrip/{route}/{direction}/{stop}?format=json')
    res = conn.getresponse()
    data = json.loads(res.read())

    print(data.pop(0)['DepartureText'])

except ValueError:
    print('Input did not include {Route} {Stop} and {Direction}')

