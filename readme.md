**/collection** contains python scripts used to retrieve and store status messages.

**/exploration** visualizers, estimators

**/html** contains D3 visualizations

**/lexicons** are the lexicons used in this version.

(lexicons courtesy of http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html)


Can a collective 'mood' be determined by the features available in the Twitter-verse?

Collect status messages from Twitter's firehose and see.

How to measure sentiment?
Started with a very simple hypothesis:
  Count 'nice' words and 'mean' words in a tweet and score the tweet.

### Data Extraction


Tweets are collected via Twitter's Stream API and stored to a database.
Tweets are filtered by geo-located tweets inside a box bounded by latitude, longitude to include much of Northern California
Collected about 400,000 status messages over the first ten days in September 2013.

### Data Exploration

Trial and error, various approaches to deal with things like unconventional text in status messages, languages, etc.
Other irregularities: Location reported in various ways.

### Features

Can features besides content (latitude, longitude, user status counts, user followers, user friends) be used to determine 'sentiment' score?

###Data Analysis

Used a combination of features.
Inputs of location (latitude, longitude, user status counts, user followers, user friends).
Tried these estimators DecisionTrees, RandomTrees, ExtraTrees to predict this 'sentiment'


