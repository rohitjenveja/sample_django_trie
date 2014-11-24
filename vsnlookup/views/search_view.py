#!/usr/bin/python

"""The controller for rendering the search form and result."""

__author__ = ("rjenveja@gmail.com (Rohit Jenveja)")


from django.shortcuts import render_to_response
from vsnlookup import search as search_logic


INVALID_FORMAT_TEXT = "Invalid format. Please try again"
CSV_HEADER = ["serial", "vehicle", "trim", "year", "make",
              "model", "trim"]


def index(request):
  """The main page of the application.

  Accepts 'q' as a GET variable, signifying the query. Populates
  the values dictionary with the items in CSV_HEADER.
  """
  if request.GET.has_key("q"):
    query = request.GET["q"]
    values = {"server_side_display_error": False}
    try:
      results = search_logic.query(query)
      if results:
        print results
        map(lambda key, value: values.update({key: value}),
            CSV_HEADER, results)
      else:
        values["no_results"] = True
    except search_logic.InvalidFormat:
      values["server_side_error"] = INVALID_FORMAT_TEXT
      values["server_side_display_error"] = True
  else:
    # The user has just loaded the page.
    values = {}

  return render_to_response("home.html", values)
