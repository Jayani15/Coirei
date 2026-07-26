def build_context(
        status,
        local_context,
        web_context
):

    if status=="Correct":

        return local_context

    elif status=="Incorrect":

        return web_context

    elif status=="Ambiguous":

        return f"""

LOCAL KNOWLEDGE

{local_context}

WEB KNOWLEDGE

{web_context}

"""