from transformers import pipeline
from transformers import GPTJForCausalLM
from transformers import AutoTokenizer
import torch

def main():
    art()
    mainNoArt()

def mainNoArt():
    print("There are two ways to generate a story :")
    print("1 - writing collaboratively with the model")
    print("2 - answering several questions to guide the model to generate the story. This works with GPT-J and requires > 12 GB of RAM available")
    choice = int(input())

    if (choice == 1):
        interactivePrompt()
    elif(choice == 2):
        (genre, world, main_character, occupation, topic) = questions()
        story = generateStory(genre, world, main_character, occupation, topic)
        print("Here the generated story: \n")
        print(story)
        print("###\n Would you like to save your story (s) or to quit (q)?")
        choice = input()

        while(True):
            if(choice == 's'):
                save(story)
                break
            elif(choice == 'q'):
                print("quitting")
                break
            else:
                print("invalid input")

    else:
        print("Invalid choice")

def save(text):
    print("How should the story be called?")
    name = input()
    with open("stories/" + name, 'w') as f:
        f.write(text)

def interactivePrompt():
    story = ""
    generator = pipeline('text-generation', model ='EleutherAI/gpt-neo-125M')
    print("Please enter one or two sentences to begin the story:")
    start = input()
    if start[-1] != '.' :
            start += "."
    prompt = start
    
    while(prompt != 'q. '):
        result = generateText(prompt, generator)
        result = result.rsplit(".", 1)[0]
        result += "."
        print(result)
        story += result
        print("\n###\nEnter the next words in the text or type 'q' to quit:")
        prompt = input()
        if prompt[-1] != '.' :
            prompt += "."
        prompt += " "
    
    print("\n###\nHere is the finished story:")
    print(story)

    print("\n###\nWould you like to save your story (y) or (n)?")
    choice = input()

    question = False
    
    while(question == False):
        if(choice == "y"):
            save(story)
            question = True
        elif(choice == "n"):
            question = True
        else:
            print("Invalid input")

def generateText(input, generator):
    generated = generator(input, max_new_tokens = 100, no_repeat_ngram_size=2, temperature=0.9)
    return(generated[0].get("generated_text").replace("\n", ""))

def questions():
    print("What is the genre of the story? (Historical, Sci-Fi, Fantasy, Thriller, Western, ...")
    genre = input()
    genre = genre.lower()
    print("What is the name of the world in the story?")
    world = input()
    print("Fine, who is the main character of the story? How do others call him or her?")
    main_character = input()
    print("And what is the occupation of " + main_character + "?")
    occupation = input()
    occupation = occupation.lower()
    print("Last question, what will be this story about? (Love, death, robots, friendship, money, coming-of-age, ...")
    topic = input()
    topic = topic.lower()

    print(f"Now generating a {genre} story about {topic} with {main_character}, a brave {occupation}...")

    return (genre, world, main_character, occupation, topic)

def generateStory(genre, world, main_character, occupation, topic):
    #generator = pipeline('text-generation', model ='EleutherAI/gpt-neo-125M') #change this to accomodate a larger/different model

    #only for the very brave
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = GPTJForCausalLM.from_pretrained("EleutherAI/gpt-j-6B", revision="float16", low_cpu_mem_usage=True)
    model.to(device)
    tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")

    context = f"""The following is a story. The genre of the story is {genre} and it is a story about {topic}.\
            The story is set in the world of {world}.\
            The main character of this story is {main_character}. {main_character} is a {occupation}.\
            \nThe story begins as follow: In the world of {world}, {main_character} is """
    

    #context = f"{main_character} is a {occupation} that "
    input_ids = tokenizer(context, return_tensors="pt").input_ids.to(device)
    generated_ids = model.generate(input_ids, do_sample=True, temperature=0.9, max_length=2000)
    story = tokenizer.decode(generated_ids[0])
    story2 = story.replace(context, "")
    return(story2)


def art():
    print("""
   _____ __                      ______                           __            
  / ___// /_____  _______  __   / ____/__  ____  ___  _________ _/ /_____  _____
  \__ \/ __/ __ \/ ___/ / / /  / / __/ _ \/ __ \/ _ \/ ___/ __ `/ __/ __ \/ ___/
 ___/ / /_/ /_/ / /  / /_/ /  / /_/ /  __/ / / /  __/ /  / /_/ / /_/ /_/ / /    
/____/\__/\____/_/   \__, /   \____/\___/_/ /_/\___/_/   \__,_/\__/\____/_/     
                    /____/                                                      

This story generator uses GPT-NEO (or GPT-J) to produce text.\n\
Please tell me a little bit about what kind of story you'll want me to create\n\
    WARNING: SOMETIMES THE MODEL GOES A LITTLE CRAZY AND PRODUCES NSFW CONTENT, BE AWARE OF THIS!""")

if __name__ == "__main__":
    main()
