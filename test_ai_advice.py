from ollamamodel import ollamamodel

def test_ai_advice():
    print("\n🧪 Starting AI Advice Test:\n")

    # יצירת מופע של המודל
    ai_model = ollamamodel()

    # שאלה לבדיקה
    test_question = "What is a good investment strategy for beginners?"

    print(f"🤖 Sending question to AI: {test_question}")

    # קבלת תשובה
    response = ai_model.get_advice(test_question)

    # הדפסת תשובה
    print(f"\n📥 AI Response:\n{response}")

    # בדיקת תקינות תשובה
    if response.startswith("❌"):
        print("\n❌ AI returned an error. Check connection or model availability.")
    elif response.strip() == "":
        print("\n❌ AI returned an empty response.")
    else:
        print("\n✅ AI advice received successfully!")

if __name__ == "__main__":
    test_ai_advice()
