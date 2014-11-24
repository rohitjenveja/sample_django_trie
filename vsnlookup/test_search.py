__author__ = ('rjenveja@gmail.com Rohit Jenveja')

"""Validate building and searching a trie."""

import unittest
import search

class TestSearch(unittest.TestCase):
  
  def tearDown(self):
    self.trie = None

  def CreateSearchTrie(self, vsns):
    self.trie = search.create_trie(vsns)

  def testSearchTrieWithMultipleVSNs(self):
    self.CreateSearchTrie(['A**DEF123456', 'ABCDEF12345*'])
    lookup = search.lookup_from_trie(self.trie, 'ABCDEF123456')
    # assert that we find ABCDEF12345* as the result
    self.assertEquals((1, 'ABCDEF12345*'), lookup)

  def testSearchTrieWithExactVSN(self):
    self.CreateSearchTrie(['ABCDEF123456'])   
    self.assertEquals(search.lookup_from_trie(self.trie, 'ABCDEF123456'),
                     (0, 'ABCDEF123456'))

  def testSearchTrieWithEqualWildCardResults(self):
    self.CreateSearchTrie(['ABCDEF12345*', ['ABCDEF1234*6']])
    self.assertEquals(search.lookup_from_trie(self.trie, 'ABCDEF123456'),
                     (1, 'ABCDEF12345*'))

  def testCreateSearchTrie(self):
    self.CreateSearchTrie(['123'])
    expected_trie = {'1': {'2': {'3': {'complete': 'complete'}}}} 
    self.assertEquals(self.trie, expected_trie)

  def testLoadCSVAndTestExample(self):
    trie = search.load_csv()
    self.assertEquals(search.lookup_from_trie(search.TRIE, 'XXRCAV012345'),
                      (5, 'XXRC*V*12***'))


if __name__ == '__main__':
  unittest.main()
