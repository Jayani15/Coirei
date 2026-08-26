from backend.memory import (
    save_memory,
    get_memory
)


def test_memory():

    save_memory(
        user_id=1,
        user_message="I like Python",
        assistant_response="Great!"
    )

    memory = get_memory(1)

    assert len(memory["conversation"]) > 0