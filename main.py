import os
from openai import OpenAI
import json
import collections

os.environ["OPENAI_API_KEY"] = ""
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def read_prompt(file_path):
    prompt = ''
    with open(file_path,'r') as f:
        prompt = f.readlines()
    prompt = '\n'.join(prompt)
    return prompt


def LLM_response(target_folder,question):
    
    systemPrompt = read_prompt('./template/moral_system.txt')
    #6_concepts QFT_30 6_concepts_compare QFT_30_compare 
    userPrompt = read_prompt('./questions/{}/{}.txt'.format(target_folder,question))#6_concepts QFT_30
    print("The current the question is:\n",userPrompt)
    messages=[
            {"role": "system",
            "content":systemPrompt
            },
            {"role": "user",
            "content": userPrompt
            }
        ]
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4",#gpt-3.5-turbo,gpt-4
    )
    return chat_completion.choices[0].message.content


def print_fancy_header():
    # Define the header message
    header_message = "Welcome to the Large Language Model Moral Test"
    
    
    top_bottom_border = "=" * 80
    side_borders = "|" + " " * (len(top_bottom_border) - 2) + "|"
    message_length = len(header_message)
    left_padding = (len(top_bottom_border) - message_length) // 2 - 1
    right_padding = len(top_bottom_border) - left_padding - message_length - 2
    centered_message = f"|{' ' * left_padding}{header_message}{' ' * right_padding}|"
    
    
    print(top_bottom_border)
    print(side_borders)
    print(centered_message)
    print(side_borders)
    print(top_bottom_border)
    
def get_all_files(path):
    files = []
    entries = os.listdir(path)
    
    for entry in entries:
        if entry.endswith("txt"):
            files.append(entry)
            
    return files
    

def main():
    total_score = 0
    cur_score = 0
    concepts_score = collections.defaultdict(float)
    
    print_fancy_header()
    #MFQ_30, 6_concepts,MFQ_30_compare, 6_concepts_compare
    target_folder = "MFQ_30_compare"
    #get the question answers
    ans = {}
    with open("./answers/{}.json".format(target_folder), 'r') as json_file:
        ans = json.load(json_file)
        
    questions = get_all_files("./questions/{}/".format(target_folder))
    #questions = ["care_1.txt"]
    for question in questions:
        response = LLM_response(target_folder,question[:-4])
        print("The answer of the Large Language Model is:\n {} \n".format(response))
        
        score = ans[question[:-4]][response[0]]
        print("The current score is: ", score)
        cur_score += score
        total_score += 4
        concepts_score[question[:-6]] += score
        print("The total score is: {:.1f}/{:.1f}".format(cur_score,total_score))
    concepts = ["harm","fairness","ingroup","authority","purity","liberty"]
    for key in concepts:
        print("The concepts {} score is: {:.1f}".format(key,concepts_score[key]))

        
        
if __name__ == '__main__':
    main()