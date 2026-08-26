from backend.chat import chat_with_ai


def test_chat():

    response = chat_with_ai(
        "What is Python?",
        user_id=1
    )

    assert response is not None