import new
import unittest
import ast

class Test_TestTrial(unittest.TestCase):
    def test_nothing(self):
        self.assertEqual(new.nothing(5), 5)

    def test_get_podcast_data_from_feed(self):
        shouldBe = "[{'title': 'Joe Being...Oh.', 'summary': 'Joe Biden causes a furor in Washington with tales of working with segregationists. ABCs Tom Llamas examines how Bidens son made millions when his father was in office. And amid a raft of climate headlines, the EPA makes a big change to emissions standards. \nLike the show? Leave a review: http://bit.ly/ReviewStartHere \nFollow @StartHereABC for exclusive content, show updates and more:\n- Twitter: https://www.twitter.com/starthereabc\n- Facebook: https://www.facebook.com/starthereabc\n- Instagram: https://www.instagram.com/starthereabc \nDiscover more ABC News podcasts: http://www.abcnewspodcasts.com \nStart Here is produced by ABC Radio. For more information: http://www.abcnewspodcasts.com', 'length': '21037556', 'href': 'https://serve.castfire.com/audio/3649889/3649889_2019-06-20-020429.256k.mp3', 'published': 'Thu, 20 Jun 2019 05:30:46 -0400', 'audio': 1}]"
        result = str(new.get_podcast_data_from_feed('tests/podcast_data'))
        self.assertEqual( 
            shouldBe[0:50],
            result[0:50]
         )



if __name__ == '__main__':
    unittest.main()