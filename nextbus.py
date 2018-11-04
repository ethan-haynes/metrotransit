import http.client, json, sys

class BusHandler:
    __metro_host__ = 'svc.metrotransit.org'
    __dirs__ = {
            'SOUTH' : '1',
            'EAST'  : '2',
            'WEST'  : '3',
            'NORTH' : '4'
    }

    def __init__(self, route, stop, direction):
        try:
            self.route = route
            self.stop = stop
            self.direction = self.__dirs__[direction.upper()]
            self.run()
        except KeyError:
            print(f'{direction} is not a valid direction. Please choose between [North, South, East, West]')

    def __http_conn__(self, url):
        conn = http.client.HTTPConnection(self.__metro_host__)
        conn.request("GET", url)
        res = conn.getresponse()
        return json.loads(res.read())

    def __get_route__(self):
        data, route = self.__http_conn__('/NexTrip/Routes?format=json'), None
        for item in data:
            if self.route == item['Description']:
                route = item['Route']
        if not route:
            raise ValueError(f'{self.route} is not a valid Route')
        
        return route

    def __get_stop__(self, route):
        data, stop = self.__http_conn__(f'/NexTrip/Stops/{route}/{self.direction}?format=json'), None
        for item in data:
            if self.stop == item['Text']:
                stop = item['Value']
        if not stop:
            raise ValueError(f'{self.stop} is not a valid Stop')

        return stop

    def __get_time__(self, route, stop):
        data, time = self.__http_conn__(f'/NexTrip/{route}/{self.direction}/{stop}?format=json'), None

        if data and len(data):
            return data.pop(0)['DepartureText']

    def run(self):
        route = self.__get_route__()
        stop = self.__get_stop__(route)
        time = self.__get_time__(route, stop)
        if time:
            print(time)

if __name__ == '__main__':
    try:
        if len(sys.argv) != 4: 
            raise ValueError('Input did not include {Route} {Stop} and {Direction}') 
        _, route, stop, direction = sys.argv
        BusHandler(route, stop, direction)
    except ValueError as error:
        print(error)
