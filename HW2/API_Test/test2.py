import unittest
import api
import os


class Test2(unittest.TestCase):
	def test_username(self):
		m = 0
		os.system('python api.py')
		txt = open('bad_result.txt', 'r')
		a = txt.read()
		if a == ('Sorry, the user is not exist.'):
			m = m + 1
		try:
			self.assertEqual(m, 1)
			print('Your program pass the recognization test.')
		except:
			print('Your program fail the recognization test.')
		txt.close()

if __name__ == '__main__':
	unittest.main()
