#!/usr/bin/python

"""Server-side validation logic that can be used before creating, updating, or
   reading from a data source.

   In addition to server side validation logic, there is also client-side
   validation in the javascript.
"""

__author__ = "rjenveja@gmail.com (Rohit Jenveja)"

import re

VALIDATE_REGEX = "^[A-Z*]{6}[0-9*]{6}$"

def ValidateVSN(expression):
  """Validates a vsn passes the regex check to ensure its properly formatted.

  Args:
    expression: A string to check.

  Returns:
    A boolean value indicating whether its passed the regex expression.

  """
  compiled = re.compile(VALIDATE_REGEX)
  result = compiled.match(expression)
  if result:
    return True
  return False


def ValidVSNList(items):
  """Validates a list of VSNs in string format.

  Args:
    items: A list of strings of VSNs to be validated.

  Returns:
    A subset of the list containing only valid VSNs.
  """
  return [item for item in items if ValidateVSN(item)]


def FewestWildcards(matched_values):
  """Returns a list of the items that have the fewest wildcards.

  Args:
    match_values: All valid VSNs.

  Returns:
    A list of VSNs with the fewest wildcards. It can return multiple VSNs,
    if they have an equal number of wildcards.
  """
  min_key_value = []
  for value in matched_values:
    count = value.count('*')
    if not min_key_value:
      min_key_value = [[value], count]
    elif count < min_key_value[1]:  # compare count of previous min_key_value
      min_key_value = ([value], count)
    # Handle the case where same number of wildcards in two expressions.
    elif count == min_key_value[1]:
      min_key_value[0].append(value)
  return min_key_value[0]
