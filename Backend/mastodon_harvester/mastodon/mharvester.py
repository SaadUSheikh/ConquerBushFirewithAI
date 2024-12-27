from elasticsearch8 import Elasticsearch
from flask import current_app
from mastodon import Mastodon
from bs4 import BeautifulSoup
from datetime import datetime
import time, json, re, jsonify

def parse_datetime_utc(created_at):
    ''' Returns the created datetime of one status in UTC+0 format
        ---
        Parameter
            created_at: a string fetched from a key 
                named 'created_at' of a status dictionary, it is the initial format of created datetime
        ---
    '''
    date_str = re.sub(r'\.\d*', r'', created_at)
    date_format = '%Y-%m-%d %H:%M:%S%z'
    date_obj = datetime.strptime(date_str, date_format)
    utc_time = date_obj.strftime('%Y-%m-%dT%H:%M')

    return utc_time

def parse_username(username):
    ''' Returns the username of status
        --- 
        Parameter
            username: a string fetched from a key 
                named ['account']['username'] of a status dictionary
        ---
    '''
    return username

def parse_content(content):
    ''' Returns the content of status
        ---
        Parameter
            content: a string fetched from a key 
                named 'content' of a status dictionary, it contains the content and hashtags of the status
        ---
    '''
    soup = BeautifulSoup(content, 'html.parser')
    text = re.sub(r'http[s]?:[^\s]*', r'', soup.get_text())
    content = re.sub(r'#[^\s]*', r'', text)
    content = content.strip()

    return content

def parse_hashtags(content):
    ''' Returns the hashtags of status
        ---
        Parameter
            content: a string fetched from a key 
                named 'content' of a status dictionary, it contains the content and hashtags of the status
        ---
    '''
    soup = BeautifulSoup(content, 'html.parser')
    text = re.sub(r'http[s]?:[^\s]*', r'', soup.get_text())
    hashtags = re.findall(r'#[^\s]*', text)

    return hashtags

def main():
    ## pushing statuses into ElasticSearch

    ## creating an Elasticsearch client instance
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=('elastic', '7f5HcK>2$(5E')
    )
    current_app.logger.info(f"Attempting to fetch mastodon data")

    try:
        ## initializing a Mastodon instance with the given token and API base URL
        m = Mastodon(
            access_token="a2QMTeXV3F9rywD0yhswNynpQmhuOhSBjsrXElGOqD8", 
            api_base_url="https://mastodon.au")

        ## fetching the latest status by sleep 5 seconds from the last one
        lastid = m.timeline(timeline='public', since_id=None, limit=1, remote=True)[0]['id']
        time.sleep(5)
        statuses =  json.dumps(m.timeline(timeline='public', since_id=lastid, remote=True), default=str)
        statuses = json.loads(statuses)

        ## iterating through all the statuses fetched,
        ## and extracting 4 desired keys (created datetime, username, content and hashtags)
        ## then serializing them into json formatted string.
        ## finally, pushing them into ElasticSearch
        data = []
        for post in statuses:
            ## filtering non-english statuses
            if post['language'] != 'en':
                continue

            row_data = {
                "created_at": parse_datetime_utc(post['created_at']),
                "username": parse_username(post['account']['username']),
                "content" : parse_content(post['content']),
                "hashtags": parse_hashtags(post['content'])
            }
            data.append(row_data)
            res = client.index(index="mastodon", id = post['id'], body=row_data)
            current_app.logger.info(f"Indexed data: {res}")
            pretty_json = json.dumps(data, indent=4)
            return current_app.response_class(pretty_json, content_type="application/json"), 200
    
    except Exception as err:
        # Generic error handling for any other exception
        return jsonify({"error": "An error occurred", "details": str(err)}), 500

