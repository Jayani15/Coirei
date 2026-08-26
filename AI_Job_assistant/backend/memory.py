from database import (
    save_message as db_save_message,
    get_chat_history,
    save_memory as db_save_memory,
    get_user_memory as db_get_user_memory
)


# -------------------------
# Conversation Memory
# -------------------------

def get_conversation(user_id):

    return get_chat_history(user_id)


def save_message(user_id, role, content):

    db_save_message(
        user_id,
        role,
        content
    )


# -------------------------
# Long-Term User Memory
# -------------------------

def save_user_memory(user_id, key, value):

    db_save_memory(
        user_id,
        key,
        value
    )


def get_user_memory(user_id):

    return db_get_user_memory(user_id)