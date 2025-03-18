import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# הוספת נתיב לפרויקט כדי לוודא שהמודולים נמצאים
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from ollamamodel import AIAdvisorRAG, get_collection
import rag_loader


def test_no_duplicate_advice_prints():
    """ בדיקה לוודא שאין הדפסות כפולות של קריאה ל-AI """
    ai_advisor = AIAdvisorRAG()
    question = "What is 1+1?"
    
    with patch("builtins.print") as mock_print:
        ai_advisor.get_advice(question)
        
        # וודא שהודעת "Getting AI advice..." מופיעה רק פעם אחת
        messages = [call[0][0] for call in mock_print.call_args_list]
        assert messages.count("🔍 Getting AI advice with RAG and personalized portfolio context...") == 1


def test_chromadb_loads_only_once():
    """ בדיקה לוודא ש-ChromaDB נטען רק פעם אחת """
    ai_advisor = AIAdvisorRAG()
    
    with patch("ollamamodel.get_collection", wraps=rag_loader.get_collection) as mock_get_collection:
        ai_advisor.ensure_collection_loaded()
        ai_advisor.ensure_collection_loaded()
        
        # הפונקציה אמורה להיקרא רק פעם אחת
        mock_get_collection.assert_called_once()


def test_full_ai_response():
    """ בדיקה לוודא שהתשובה של ה-AI אינה נחתכת """
    ai_advisor = AIAdvisorRAG()
    
    full_response = "Invest in diversified assets."
    
    with patch("ollamamodel.ollama.generate", return_value={"response": full_response}):
        response = ai_advisor.get_advice("Should I invest in Apple or Google?")
        
        assert response == full_response, "AI response was cut off!"
