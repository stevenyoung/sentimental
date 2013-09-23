#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
from collections import Counter

from sklearn.cross_validation import cross_val_score
from sklearn.ensemble.forest import RandomForestClassifier
from sklearn.ensemble.forest import ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier

import located_tweets

# X, y = located_tweets.load_data_from_csv()
# test_X, test_y = located_tweets.load_test_data()

X, y = located_tweets.training_data_from_db()

cv = 10
features = itertools.cycle(['word count', 'meaning words', 'latitude',
                            'longitude', 'followers', 'user listed',
                            'user statuses', 'user favorites', 'user friends'])
for i in range(3, cv + 1):
  decision_tree = DecisionTreeClassifier()
  dt_score = cross_val_score(decision_tree, X, y, cv=i)
  print '\n\ndecision tree {}-fold cross validation accuracy: {}'.format(i, sum(dt_score)/dt_score.shape[0])

  dt_fit = decision_tree.fit(X, y)
  print 'Feature Importances %s' % (dt_fit.feature_importances_)
  for f in dt_fit.feature_importances_:
    print '{}: {}'.format(next(features), f)

  # setting threshold to make sure not to discard all features
  X_for_preds = dt_fit.transform(X, threshold=min(dt_fit.feature_importances_))
  preds = dt_fit.predict(X_for_preds)
  print 'predictions counter %s' % (Counter(dt_fit.predict(X_for_preds)))
  fp = 0
  tp = 0
  fn = 0
  tn = 0
  for a in range(len(y)):
    if y[a] == preds[a]:
      if preds[a] == 0:
        tn += 1
      elif preds[a] == 1:
        tp += 1
    elif preds[a] == 1:
      fp += 1
    elif preds[a] == 0:
      fn += 1

  print 'correct positives:', tp
  print 'correct negatives:', tn
  print 'false positives:', fp
  print 'false negatives:', fn

  #to visualize decision tree

  random_forest = RandomForestClassifier()
  random_score = cross_val_score(random_forest, X, y, cv=i)
  print '\nrandom forest %s-fold cross validation accuracy: %s' % (i, sum(random_score)/random_score.shape[0])

  random_fit = random_forest.fit(X, y)
  print 'Feature Importances %s' % (random_fit.feature_importances_)
  for f in random_fit.feature_importances_:
    print '{}: {}'.format(next(features), f)

  X_for_preds = random_fit.transform(X, threshold=min(random_fit.feature_importances_))
  preds = random_fit.predict(X_for_preds)
  print 'predictions counter %s' % (Counter(random_fit.predict(X_for_preds)))
  fp = 0
  tp = 0
  fn = 0
  tn = 0
  for a in range(len(y)):
    if y[a] == preds[a]:
      if preds[a] == 0:
        tn += 1
      elif preds[a] == 1:
        tp += 1
    elif preds[a] == 1:
      fp += 1
    elif preds[a] == 0:
      fn += 1

  print 'correct positives:', tp
  print 'correct negatives:', tn
  print 'false positives:', fp
  print 'false negatives:', fn

  extra_trees = ExtraTreesClassifier()
  extra_score = cross_val_score(extra_trees, X, y, cv=i)
  print '\nextra trees %s-fold cross validation accuracy: %s' % (i, sum(extra_score)/extra_score.shape[0])

  extra_fit = extra_trees.fit(X, y)
  print 'Feature Importances %s' % (extra_fit.feature_importances_)
  for f in extra_fit.feature_importances_:
    print '{}: {}'.format(next(features), f)

  X_for_preds = extra_fit.transform(X, threshold=min(extra_fit.feature_importances_))
  preds = extra_fit.predict(X_for_preds)
  print 'predictions counter %s' % (Counter(extra_fit.predict(X_for_preds)))
  fp = 0
  tp = 0
  fn = 0
  tn = 0
  for a in range(len(y)):
    if y[a] == preds[a]:
      if preds[a] == 0:
        tn += 1
      elif preds[a] == 1:
        tp += 1
    elif preds[a] == 1:
      fp += 1
    elif preds[a] == 0:
      fn += 1

  print 'correct positives:', tp
  print 'correct negatives:', tn
  print 'false positives:', fp
  print 'false negatives:', fn


from sklearn.linear_model import LogisticRegression
clf = LogisticRegression()
clf.fit(X, y)

# Add confusion matrices
