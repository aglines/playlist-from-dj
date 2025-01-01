import apache_beam as beam
import requests
import json
from datetime import datetime
import os
import time
from config.private_data import API_SOURCE_URL_PLAYS

# Some data limits based on simple research
# max_offset = 295811
# earliest_date = '2001-04-09T08:00:00-07:00'
# earliest_show_id = 6911

class RequestData(beam.DoFn):
    def __init__(self, chunk_size=3000, delay=0.3):
        self.chunk_size = chunk_size
        self.data_chunk = []
        self.delay = delay


    def process(self, element):
        url = API_SOURCE_URL_PLAYS
        params = {
            'host_ids': 26,
            'exclude_airbreaks': True,
            'exclude_non_songs': True,
            'airdate_after': '2001-04-09T08:00:00-07:00',
            'airdate_before': '2025-01-01T00:00:00-08:00',
            'ordering': 'airdate'
        }
        next_url = url

        while next_url:
            response = requests.get(next_url, params=params)
            if response.status_code not in range(200, 201):
                print(f"Error in API request response: {response.status_code}")
            response = response.json()
            data = response['results']
            if not data:
                print('No more data')
                break

            self.data_chunk.extend(data)
            if len(self.data_chunk) >= self.chunk_size:
                yield self.data_chunk
                self.data_chunk = []

            next_url = response.get('next')
            params = {}
            print(f'Next URL: {next_url}')

            # Add delay between requests
            time.sleep(self.delay)

        if self.data_chunk:
            yield self.data_chunk
            self.data_chunk = []

def writedata_tojson(data):
    rn = datetime.now().strftime('%H%M%S')
    output_file = os.path.join('data', f'output_{rn}.json')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(data, f)
    return output_file

if __name__ == '__main__':
    with beam.Pipeline() as pipeline:
        (
            pipeline
            | 'Start' >> beam.Create([1])
            | 'Get Data' >> beam.ParDo(RequestData(chunk_size=3000, delay=0.3))
            | 'Write to JSON' >> beam.Map(writedata_tojson)
        )

