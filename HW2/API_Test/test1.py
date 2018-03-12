import unittest
import api
import time
import os


class Test1(unittest.TestCase):
	def test_time(self):
		t1 = time.time()
		os.system('python api.py')
		t2 = time.time()
		t = t2 - t1
		try:
			self.assertLess(t, 15)
			print('Your program meet the time specification.')
		except:
			print('You fail the time test.')

	
if __name__ == '__main__': 
	unittest.main() 