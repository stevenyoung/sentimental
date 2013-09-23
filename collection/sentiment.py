from os import path
from nltk.corpus import stopwords


def get_positive_words():
  f = open(path.join(path.expanduser('~'),
           'lexicons/positive-words.txt'))
  words = []
  for line in f:
    if not line.startswith(';'):
      words.append(line.strip())
  f.close()
  return words


def get_negative_words():
  f = open(path.join(path.expanduser('~'),
           'lexicons/negative-words.txt'))
  words = []
  for line in f:
    if not line.startswith(';'):
      words.append(line.strip())
  f.close()
  return words


def score_sentiment(sentence):
  score = {}
  positive_words = get_positive_words()
  negative_words = get_negative_words()
  # split into words
  words = sentence.lower().split()
  # remove punctuation and split into seperate words
  # words = re.findall(r'\w+', sentence,flags = re.UNICODE | re.LOCALE)
  important_words = filter(lambda x: x not in stopwords.words('english'),
                           words)
  positive_matches = 0
  negative_matches = 0
  # print sentence
  # print important_words
  for word in important_words:
    word = word.encode('ascii', 'ignore')
    # print word
    if word in positive_words:
      # print 'pos match'
      positive_matches += 1
    if word in negative_words:
      # print 'neg match'
      negative_matches += 1
  score['positive matches'] = positive_matches
  score['negative matches'] = negative_matches
  score['word count'] = len(words)
  score['meaning word count'] = len(important_words)
  return score


def main():
  sentence = 'i turned into a stump'
  score = score_sentiment(sentence)
  print sentence, score


if __name__ == '__main__':
  main()
