__author__ = 'rohitj'

"""Test the validation logic."""


import unittest
import validation

class TestValidation(unittest.TestCase):

  def testValidVSNList(self):
    input = ['ABC*EF*****6', 'ABCDEF******']
    results = validation.ValidVSNList(input)
    self.assertEquals(results, input)

  def testValidVSNListWithInvalidVSN(self):
    input = ['ABC*EF*****6', 'ABCDEF******', 'invalid']
    results = validation.ValidVSNList(input)
    self.assertEquals(results, input[:2])

  def testFewestWildcardsClearWinner(self):
    fewest_wildcards = ["ABCDEF******", "ABCDEF1*****"]
    self.assertEquals(
        validation.FewestWildcards(fewest_wildcards),
        [fewest_wildcards[1]])

  def testFewestWildcardsTwoEqualWildcards(self):
    fewest_wildcards = ["ABCDEFG*****", "ABCDEF1*****"]
    # Both values should be returned, since they have equal
    # number of wild cards.
    self.assertEquals(
        validation.FewestWildcards(fewest_wildcards),
        fewest_wildcards)

  def testLowerCaseIsInvalid(self):
    expression = "ABcDEF123456"
    self.assertFalse(validation.ValidateVSN(expression))

  def testValidateVSNOnSmallExpression(self):
    expression = "a"
    self.assertFalse(validation.ValidateVSN(expression))

  def testValidateVSNOnLargeExpression(self):
    expression = "abcdef123456789"
    self.assertFalse(validation.ValidateVSN(expression))

  def testValidateVSNOnLettersLast(self):
    expression = "123456abcdef"
    self.assertFalse(validation.ValidateVSN(expression))

  def testValidateVSNOnLettersNumbersMixed(self):
    expression = "1a2b3c4d5e6f"
    self.assertFalse(validation.ValidateVSN(expression))

if __name__ == '__main__':
  unittest.main()
