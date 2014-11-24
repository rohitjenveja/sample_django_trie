#!/usr/bin/python

"""Creates a trie in-memory to lookup VSN with fewest wildcards.

Example trie:
  vsns = ['1234']
  trie = create_trie(vsns)
  Result would be {'1': {'2': {'3': {'4': {'complete': 'complete'}}}}}


Module also Creates a hashmap to quickly access information about a VSN.
The hash map is only used after the VSN with fewest wildcards has been
determined. The map contains additional metadata about the vehicle.

Example map:
{'XXRC*V******': ['XXRC*V******', 253913, 2013, Volkswagen, GTI,
                  "2-Door Autobahn, DSG"]}
"""

__author__ = ("rjenveja@gmail.com (Rohit Jenveja)")

import collections
import csv
import fnmatch
import logging
import os

import validation

TRIE = None
MAP = {}


class Error(Exception):
  """Base Exception class that all other exceptions inherit from."""


class InvalidFormat(Error):
  """Raised when a user tries to lookup an invalid VSN."""


def load_csv():
  """Load the CSV and create a trie and a hashmap."""
  global TRIE, MAP
  csv_path = os.path.join(os.path.dirname(__file__), "vsn_data_noheader.csv")
  with open(csv_path, "rb") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    vsns = []
    for row in reader:
      # conduct validation logic on each CSV entry.
      if validation.ValidateVSN(row[0]):
        vsns.append(row[0])
        MAP[row[0]] = row
  TRIE = create_trie(vsns)


def create_trie(vsns):
  """Create a trie from a list of vsns that have been validated."""
  root = {}
  for vsn in vsns:
    level = root
    for char in vsn:
      level = level.setdefault(char, {})
    level = level.setdefault("complete", "complete")
  return root


def lookup_from_trie(trie, query, patterns="", wildcards=0):
  """Travel through the trie and determine the result with fewest wildcards.

  Args:
    trie: A nested-dict that we are traversing down. Gets smaller through
        recursion.
    query: The search query whose characters are being iterated through.
    pattern: A string that are being built recursively that contain an eligible
      pattern.
    wildcards: The total of number of wildcards found on any recursive path of
      the trie.
  """
  path_with_wildcard = None
  path_without_wildcard = None
  current_trie_query = trie
  keys = current_trie_query.keys()

  if "complete" in current_trie_query:
    # We hit the final node, return the eligible pattern and total number
    # of wildcards used.
    return wildcards, patterns

  # Take each charachter in the user's query and go down the tree.
  # Find the path (if any) that contains the fewest wildcards.
  for char in query:
    if "*" in keys:
      current_string = patterns + "*"
      path_with_wildcard = lookup_from_trie(current_trie_query["*"], query[1:],
                                            current_string, wildcards+1)
    if char in keys:
      # Visit the valid child element that matches the char.
      current_string = patterns + char
      path_without_wildcard  = lookup_from_trie(
          current_trie_query[char], query[1:],
          current_string, wildcards)
    if path_with_wildcard and path_without_wildcard:
      # There were multiple options returned. Determine which route had the
      # fewest wildcards.
      if path_with_wildcard[0] < path_without_wildcard[0]:
        return path_with_wildcard
      else:
        return path_without_wildcard
    elif path_without_wildcard and not path_with_wildcard:
      # The path without wildcards at this level wins.
      return path_without_wildcard
    else:
      # The path that had the wildcard at this level had fewer wildcards in
      # subsequent levels.
      return path_with_wildcard
  else:
   if query:  # last letter or wildcard to check.
     if query in keys:
       # The very last char on the trie matched the query. Return the pattern
       # and total number of wildcards used.
       return patterns + query, wildcards
     else:
       # The very last char on the trie is a wildcard. Increment the total
       # number of wildcards used to go down this path and the eligible pattern.
       return patterns + "*", wildcards + 1

def query(query):
  """Process a frontend query.

  Args:
    query: User-input that might not be a valid VSN.

  Returns:
    A result if any are found from the trie.

  Raises:
    InvalidFormat:
      If the format does not meet the server-side validation, this is raised.
  """
  if not TRIE:
    load_csv()
  if validation.ValidateVSN(query):
    result = lookup_from_trie(TRIE, query)
    if result:
      return MAP[result[1]]
  else:
    # Perhaps raise an exception and catch the exception in the view
    raise InvalidFormat("Invalid Format. Please try again.")

if __name__ == '__main__':
  load_csv()

  # This portion of code will normally not be executed unless this file
  # is executed directly, instead of imported as a module. Useful for
  # performing quick queries through the command line.
