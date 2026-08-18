from groq import Groq


async def chatbot(question):
    client_groq = Groq(api_key="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")

    prompt = f"""    
        Question:
        {question}
    
        Answer:
        """
    
    response = client_groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content