import unittest
from unittest.mock import patch
from ollamamodel import AIAdvisorRAG
from rag_loader import get_collection
from main import main

class TestGetCollectionUsage(unittest.TestCase):
    @patch("rag_loader.get_collection")
    def test_get_collection_call(self, mock_get_collection):
        """
        בודקת האם get_collection() נקרא במקומות לא נכונים, ומונעת טעינה מיותרת
        """
        mock_get_collection.return_value = "MOCK_COLLECTION"

        # מפעילים את המערכת
        main()

        # בודקים כמה פעמים קראו ל-get_collection()
        self.assertEqual(mock_get_collection.call_count, 1, "❌ ERROR: get_collection() נקרא יותר מפעם אחת!")

if __name__ == "__main__":
    unittest.main()
