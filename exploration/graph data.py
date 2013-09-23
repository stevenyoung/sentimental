# /usr/bin/env python
# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import itertools
import MySQLdb
import matplotlib.pyplot as plt
import pandas.io.sql as sql

con = MySQLdb.connect('localhost', 'root', '', 'ebs_tweets')
query = 'SELECT * from stream_sf_test'
data_frame = sql.read_frame(query, con)


df = data_frame[data_frame['sentiment'] < 7]
df = data_frame[data_frame['sentiment'] > -7]
df = df[df['lng'] < 0]
df = df[df['lat'] > 0]
print(len(df))
fig = plt.figure()
ax = fig.add_subplot(111)
points = df[['lat', 'lng', 'sentiment']]
points = points[points['sentiment'] != 0]
series = []
for i in range(points['sentiment'].min(), points['sentiment'].max()):
	series.append(points[points['sentiment'] == i])

#print series

colors = itertools.cycle(['r', 'b', 'g', 'c', 'm', 'y', 'k'])
markers = itertools.cycle(['.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', '8', 's', 'p', '*', 'h', 'H','+', 'x', 'D'])
c = 0


i = 0
plots = []
while i < len(series):
	plot = ax.scatter(series[i]['lat'], series[i]['lng'], color=next(colors), marker = next(markers))
	plots.append(plot)
#    #ax.scatter(series[i]['lat'], series[i]['lng'], color=next(colors), marker = next(markers))
	i += 1

#plt.legend(plots,
#           ('Low Outlier', 'LoLo', 'Lo', 'Average', 'Hi', 'HiHi', 'High Outlier'),
#           scatterpoints=1,
#           loc='lower left',
#           ncol=3,
#           fontsize=8)

plt.axis([32, 43, -125, -114])

plt.axis([37.0, 38.0, -123.0, -122.0])
plt.show()

# <codecell>

points[points['sentiment'] != 0]

# <codecell>

df = df[df['sentiment'] < 10]

# <codecell>

df['sentiment'].min()

# <codecell>

points = df[['lat', 'lng', 'sentiment']]
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(points['lat'], points['lng'], c=(points['sentiment'] + 8)/32)
plt.show()


range(points['sentiment'].min(), points['sentiment'].max())

len(range(points['sentiment'].min(), points['sentiment'].max()))


