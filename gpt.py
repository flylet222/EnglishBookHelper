import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)

def translate_by_box(text_list):
    #return text_list
    result_list = []
    prompt = """
            You are a translator. You will be given a paragraph in English and asked to translate it into Korean. 
            Keep the keyword in English. 
            The paragraph is from a book about computer system.
    """
    for text in text_list:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "translate from English to Korean: " + text}
            ]
        )
        result = " " + completion.choices[0].message.content
        print(result)
        if result == " ":
            result = "번역 실패"
        result_list.append(result)
    """ with open("result.txt", "w") as f:
        for t, item in zip(text_list, result_list):
            f.write(t + "\n")
            f.write(item + "\n" + "\n")
    with open("result.txt", "r") as f:
        result_list = f.readlines() """
    return result_list
