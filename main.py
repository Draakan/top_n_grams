import json
import csv
from collections import Counter
import re
from enum import Enum


class EventType(str, Enum):
  PUSH = 'PushEvent'


def extract_3grams(message):
  words = re.findall(r'\b\w+\b', message.lower())
  ngrams = zip(words, words[1:], words[2:])

  return [' '.join(ngram) for ngram in ngrams]


def process_jsonl(jsonl_file):
  author_3grams = {}

  with open(jsonl_file, 'r') as items:
    for item in items:
      data = json.loads(item)

      if data['type'] == EventType.PUSH:
        author = data['actor']['login']
        commits = data['payload']['commits']

        for commit in commits:
          message = commit['message']
          author_3grams.setdefault(author, extract_3grams(message))

  return author_3grams


def write_to_csv(author_3grams, file_path):
  with open(file_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['author', 'first 3-gram', 'second 3-gram', 'third 3-gram', 'fourth 3-gram', 'fifth 3-gram'])

    for author, ngrams in author_3grams.items():
      if len(ngrams) >= 5:
        top_ngrams = Counter(ngrams).most_common(5)
        writer.writerow([author] + [ngram[0] for ngram in top_ngrams])


def main():
  author_3grams = process_jsonl('./10K.github.jsonl')

  write_to_csv(author_3grams, './top_3grams.csv')

  print('done')


if __name__ == '__main__':
  main()
