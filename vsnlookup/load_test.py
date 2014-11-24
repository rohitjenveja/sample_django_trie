#!/usr/bin/python

"""Load test whether the trie could handle large number of VSNs."""

import logging
import itertools
import search

def GenerateFakeVSNs(amount):
  i = 0
  fake_vsns = []
  for index, item in enumerate(itertools.permutations('ABCDEF123456', 12)):
    if index > amount:
      break
    else:
      # Note: many of the VSNs generated will be invalid. Simply doing this
      # to test how fast a trie lookup would be with hundreds of thousands
      # of combinations
      fake_vsns.append(item)
  return fake_vsns

if __name__ == '__main__':
  fake_vsns = GenerateFakeVSNs(200000)
  trie = search.create_trie(fake_vsns)
  del(fake_vsns)
  print search.lookup_from_trie(trie, 'ABCDEF123456')

  # Testing 10 million results. It will take about 1 minute to create the trie.
  # Lookups are quick after the trie has been built.
  fake_vsns = GenerateFakeVSNs(10000000)
  print len(fake_vsns)
  trie = search.create_trie(fake_vsns)
  del(fake_vsns)
  print search.lookup_from_trie(trie, 'ABCDEF123456')
