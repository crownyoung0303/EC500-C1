import unittest
import api
import os


class Test3(unittest.TestCase):
	def test_video(self):
		for i in os.listdir('.'):  # delete the exsit .mp4 file
			if i.endswith('.mp4'):
				os.remove(i)
		for u in os.listdir('.'): # delete the exsit .txt file
			if u.endswith('.txt'):
				os.remove(u)
		print('For this test, make sure the second argument you enter is not 1!')
		os.system('python api.py')
		m = 0
		n = 0
		for video in os.listdir('.'):
			if video.endswith('.mp4'):
				m = m + 1
		for txt in os.listdir('.'):
			if txt.endswith('_result.txt'):
				n = n + 1
		try:
			self.assertEqual(m, 1)
			print('Your program pass the .mp4 file generation test.')
		except:
			print('Your program fail .mp4 file generation test.')
		try:
			self.assertEqual(n, 1)
			print('Your program pass the .txt file generation test.')
		except:
			print('Your program fail .txt file generation test.')

	
if __name__ == '__main__':
	unittest.main() 