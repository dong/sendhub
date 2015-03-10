import unittest
import phonenumbers

class TestingPhonenumbers(unittest.TestCase):

    def test_phonenumber_is_valid_US_phonenumber(self):
        us_phonenumber = '+14156143400'
        z = phonenumbers.parse(us_phonenumber, None)
        result = phonenumbers.is_valid_number(z)
        self.assertTrue(result, 'invalid phonenumber: %s'%us_phonenumber)

    def test_phonenumber_is_not_valid_US_phonenumber(self):
        non_us_phonenumber = '+15555555552'
        z = phonenumbers.parse(non_us_phonenumber, None)
        result = phonenumbers.is_valid_number(z)
        self.assertFalse(result, 'should be invalid phonenumber: %s' % non_us_phonenumber)

    def test_phonenumber_is_not_valid_US_phonenumber2(self):
        non_us_phonenumber = '+1555555'
        z = phonenumbers.parse(non_us_phonenumber, None)
        result = phonenumbers.is_valid_number(z)
        self.assertFalse(result, 'should be invalid phonenumber: %s' % non_us_phonenumber)

    def test_phonenumber_is_not_valid_US_phonenumber3(self):
        non_us_phonenumber = '+15sdf'
        try:
            z = phonenumbers.parse(non_us_phonenumber, None)
            result = phonenumbers.is_valid_number(z)
        except Exception as err:
            result = 'The string supplied did not seem to be a phone number' in str(err)
        self.assertTrue(result, 'should be invalid phonenumber: %s'% non_us_phonenumber)

