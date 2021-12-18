from unittest import TestCase, main
from birdgame import update_score

class UpdateScoreTest(TestCase):
    def test_more(self):
        self.assertEqual(update_score(3,0),3)
    def test_less(self):
        self.assertEqual(update_score(0,3),3)
    def test_equal(self):
        self.assertEqual(update_score(3,3),3)




if __name__ == 'main':
    main()