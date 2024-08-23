import random
import re
import google.generativeai as genai # type: ignore

def settings():
    api_key_input = ""
    selected_topic = ""
    content = ""

    while True:
        try:
            api_key_input = input("Enter your Gemini API Key (You can get your API key from https://aistudio.google.com/app/u/1/apikey): ")
            genai.configure(api_key = api_key_input)
            model = genai.GenerativeModel('gemini-1.5-pro')
            response = model.generate_content('Say this is a test')
            if response:
                break

        except:
            print("An exception occurred! Try again!")

    while True:
        l = ['Technical Skills', 'Experience', 'Projects', 'Certifications']
        selected_topic = input(f"Select sub-section {l}: ")

        if selected_topic not in l:
            print("Choose from the above list only!")
        else:
            break

    while True:
        content = input("Enter details: ")
        if content == "":
            print("You haven't mentioned relevant details!")
        else:
            break

    return selected_topic, content


def check_answer(question, chat_message, incorrect):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(f"""Question - {question} Candidate answer - {chat_message}. As an interviewer evaluating 
    the candidate's response, just state whether the response is "correct" or "incorrect", followed by a rating on a scale of 
    1 to 5, where 1 indicates a poor answer and 5 signifies an excellent one.""")

    if "incorrect" in response.text.lower():
        incorrect.append(question)
        
    pattern = r'\d+'
    match = re.search(pattern, response.text)
    if match:
        number = match.group(0)
        return int(number)
    

def check_answer_qualitative(question, answer):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(f"""Question - {question} Candidate answer - {answer}. As an interviewer evaluating 
    the candidate's response, rate the response on a scale of 1 to 5, where 1 indicates a poor answer and 5 signifies an 
    excellent one based on the clarity, structure and depth of the response.""")

    pattern = r'\d+'
    match = re.search(pattern, response.text)
    if match:
        number = match.group(0)
        return int(number)


def main():
    print("TalentScan - AI-Powered Interactive Debate Partner")
    selected_topic, content  = settings()
    
    if selected_topic == "Technical Skills":
        no_questions = random.randint(8, 10)
        incorrect = []
        score_sum = 0.0
        model = genai.GenerativeModel('gemini-1.5-pro')
        chat = model.start_chat(history = [])
        for _ in range(no_questions):
            question = ""
            res = chat.send_message(f"""Given a list of programming languages or tools: {content}, randomly select one from 
            above list only and ask a technical question to assess a candidate's proficiency in that skill. The question should be 
            clear, concise, and challenging enough to differentiate between candidates with varying levels of expertise. Respond 
            as if you were a human interviewer assessing a candidate's technical proficiency and maintain a professional tone.""")

            if res is not None:
                for chunk in res:
                    if chunk.candidates:
                        question += chunk.text
                print("\n🤖:", question)

            answer = input("👤: ")
            if answer != "": 
                score = check_answer(question, answer, incorrect)
                score_sum += score
        
        print(f"\nAverage Score: {score_sum / no_questions}")
        print("List of incorrect responses:\n")
        for count, q in enumerate(incorrect):
            print(count + ". " + q)
    else:
        no_questions = random.randint(3, 5)
        score_sum = 0.0
        model = genai.GenerativeModel('gemini-1.5-pro')
        chat = model.start_chat(history = [])
        start = True
        follow_up = ""
        for _ in range(no_questions):
            question = ""

            if start == True:
                res = chat.send_message(f"""As an interviewer assessing a candidate's proficiency based on their {selected_topic}, 
                randomly select one from the following: '{content}' and ask for an overview. Ensure the question is clear, concise,
                and challenging enough to differentiate between varying levels of proficiency. Respond as if you were a human 
                interviewer, maintaining a professional tone and focusing on their level of knowledge and proficiency.""")
                start = False

            else:
                choice = random.randint(1, 2)
                if choice == 1:
                    res = chat.send_message(f""""Candidate response: '{follow_up}'. Based on this response, formulate a follow-up 
                    question that explores their answer in greater detail. Ensure the question is insightful and relevant, aimed at 
                    delving deeper into their level of knowledge and proficiency. Respond as if you were a human interviewer, 
                    maintaining a professional tone and focusing on the depth and clarity of their expertise.""")
                else:
                    res = chat.send_message(f"""As an interviewer assessing a candidate's proficiency based on their {selected_topic}, 
                    randomly select one from the following: '{content}' and ask for an overview. Ensure the question is clear, concise,
                    and challenging enough to differentiate between varying levels of proficiency. Respond as if you were a human 
                    interviewer, maintaining a professional tone and focusing on their level of knowledge and proficiency.""")


            if res is not None:
                for chunk in res:
                    if chunk.candidates:
                        question += chunk.text
                print("\n🤖:", question)
            
            answer = input("👤: ")
            follow_up = answer
            if answer != "": 
                score = check_answer_qualitative(question, answer)
                print(score)
                score_sum += score

        print(f"\nAverage Score: {score_sum / no_questions}")

if __name__ == "__main__":
    main()