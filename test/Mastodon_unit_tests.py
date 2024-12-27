import sys
sys.path.append('../backend/mastodon_harvester/mastodon/')
from mharvester import parse_datetime_utc, parse_username, parse_content, parse_hashtags

## Unit tests
def test_parse_datetime_utc():
    ## testing if the output format of created datetime is in UTC+0 date_hour_minute format
    assert parse_datetime_utc('2024-05-03 04:03:59+00:00') == '2024-05-03T04:03'
    assert parse_datetime_utc('2024-05-03 06:10:41+00:00') == '2024-05-03T06:10'

def test_parse_username():
    assert parse_username('alexkidman') == 'alexkidman'
    assert parse_username('thebiologistisn') == 'thebiologistisn'

def test_parse_content():
    ## testing if the output format of the status' content is in pure text format,
    ## it means the content without http symbols and hashtags
    assert parse_content("<p>What's the exchange rate for Retoots vs. Retweets?</p>") == "What's the exchange rate for Retoots vs. Retweets?"

    assert parse_content('<p>There\'s a new artwork under the bridge near work <a href="https://mas.to/tags/palestine" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>palestine</span></a> <a href="https://mas.to/tags/streetart" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>streetart</span></a></p>') == "There's a new artwork under the bridge near work"

def test_parse_hashtags():
    ## testing if the output format of the status' hashtags is in a list string format
    assert parse_hashtags('<p><a href="https://mstdn.social/tags/GoodMorning" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>GoodMorning</span></a></p>') == ['#GoodMorning']

    assert parse_hashtags('<p>It\'s kinda shocking how fast self checkout at Coles and Woolworths went from annoying but arguably the fastest way out of the store to a major time sink and source of aggravation as whatever junk they\'ve bought to monitor the checkouts thinks you\'ve stolen or mis-scanned something. <a href="https://aus.social/tags/coles" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>coles</span></a> <a href="https://aus.social/tags/woolworths" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>woolworths</span></a></p>') == ['#coles', '#woolworths']
    
    ## test empty hashtags
    assert parse_hashtags('<p>The election story above (or below?) is from last night. </p><p>The tories swamped voters who care about issues beyond their own living rooms like so many bugs we learn this morning.</p>') == []


if __name__ == "__main__":
    test_parse_datetime_utc()
    test_parse_username()
    test_parse_content()
    test_parse_hashtags()



