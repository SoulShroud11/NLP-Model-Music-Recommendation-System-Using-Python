import unittest
from unittest.mock import MagicMock, patch
import pickle

# Import your script
from app import recommend

class TestMusicRecommendation(unittest.TestCase):
    @patch('app.sp.search')
    @patch('app.st')
    def test_recommend(self, mock_st, mock_search):
        # Mock the streamlit st functions
        mock_st.header.return_value = None
        mock_st.selectbox.return_value = "Shape of You"
        mock_st.button.return_value = True
        mock_st.columns.return_value = [MagicMock() for _ in range(5)]
        
        # Mock the Spotify search results
        mock_search_results = {
            "tracks": {
                "items": [
                    {"album": {"images": [{"url": "http://example.com/image1.jpg"}]}},
                    {"album": {"images": [{"url": "http://example.com/image2.jpg"}]}},
                    {"album": {"images": [{"url": "http://example.com/image3.jpg"}]}},
                    {"album": {"images": [{"url": "http://example.com/image4.jpg"}]}},
                    {"album": {"images": [{"url": "http://example.com/image5.jpg"}]}},
                ]
            }
        }
        mock_search.return_value = mock_search_results

        # Mock the data loading process for music DataFrame
        music_data = {'song': ['Shape of You', 'Song 2', 'Song 3'], 'artist': ['Ed Sheeran', 'Artist 2', 'Artist 3']}
        mock_music = MagicMock()
        mock_music.__getitem__.side_effect = music_data.__getitem__
        mock_music.__len__.return_value = len(music_data['song'])

        # Load mock data for similarity
        with open('similarity.pkl', 'rb') as f:
            similarity = pickle.load(f)

        # Mock the similarity data
        with patch('app.music', mock_music), patch('app.similarity', similarity):
            recommended_music_names, recommended_music_posters = recommend("Shape of You")

            # Assertions
            self.assertEqual(len(recommended_music_names), 5)
            self.assertEqual(len(recommended_music_posters), 5)
            self.assertTrue(all(url.startswith("http://example.com/") for url in recommended_music_posters))

if __name__ == '__main__':
    unittest.main()
