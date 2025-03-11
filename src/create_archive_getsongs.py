import apache_beam as beam
import requests
import json
from datetime import datetime
import os
import time
from dotenv import load_dotenv
from dateutil.relativedelta import relativedelta

load_dotenv()

# Some data limits based on simple research
# max_offset = 295811
# earliest_show_id = 6911

class RequestData(beam.DoFn):
    def __init__(self, chunk_size=1000, delay=0.5):
        self.chunk_size = chunk_size
        self.data_chunk = []
        self.delay = delay

    def process(self, element):
        url = os.getenv('API_SOURCE_URL_PLAYS')
        host_id = os.getenv('DJ_ID')
        current_date = datetime.now()
        end_date = datetime(2000, 1, 1)  # It's known the archive doesn't go beyond this date

        while current_date > end_date:
            airdate_before = current_date
            airdate_after = current_date - relativedelta(months=1)

            params = {
                'host_ids': host_id,
                'exclude_airbreaks': True,
                'exclude_non_songs': True,
                'airdate_after': airdate_after.strftime('%Y-%m-%dT%H:%M:%S%z'),
                'airdate_before': airdate_before.strftime('%Y-%m-%dT%H:%M:%S%z'),
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

            current_date = airdate_after  # Move to the previous month

def writedata_tojson(data):
    data_path = os.getenv('LOCAL_DATA_PATH')
    rn = datetime.now().strftime('%H%M%S')
    output_file = os.path.join(f'{data_path}/kexp', f'output_{rn}.json')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(data, f)
    return output_file

if __name__ == '__main__':
    with beam.Pipeline() as pipeline:
        (
            pipeline
            | 'Start' >> beam.Create([1])
            | 'Get Data' >> beam.ParDo(RequestData(chunk_size=1000, delay=0.5))
            | 'Write to JSON' >> beam.Map(writedata_tojson)
        )
