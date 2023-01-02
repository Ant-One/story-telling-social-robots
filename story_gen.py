from transformers import pipeline

def main():
    (genre, main_character, occupation, topic) = artAndPrompt()

    story = generateStory(genre, main_character, occupation, topic)

def generateStory(genre, main_character, occupation, topic):
    generator = pipeline('text-generation', model ='EleutherAI/gpt-neo-125M')

    context = [
        f"The following is a story. The genre of the story is {genre} and it is a story about {topic}.\
            The main character of this story is {main_character}. {main_character} is a {occupation}.\
            The story begins: """
    ]
    story = generator(context, max_new_tokens = 200)
    print(story)


def artAndPrompt():
    print("""
   _____ __                      ______                           __            
  / ___// /_____  _______  __   / ____/__  ____  ___  _________ _/ /_____  _____
  \__ \/ __/ __ \/ ___/ / / /  / / __/ _ \/ __ \/ _ \/ ___/ __ `/ __/ __ \/ ___/
 ___/ / /_/ /_/ / /  / /_/ /  / /_/ /  __/ / / /  __/ /  / /_/ / /_/ /_/ / /    
/____/\__/\____/_/   \__, /   \____/\___/_/ /_/\___/_/   \__,_/\__/\____/_/     
                    /____/                                                      

This story generator uses GPT-NEO to produce text.\n\
Please tell me a little bit about what kind of story you'll want me to create""")

    print("What is the genre of the story? (Historical, Sci-Fi, Fantasy, Thriller, Western, ...")
    genre = input()
    print("Fine, who is the main character of the story? How do others call him?")
    main_character = input()
    print("And what is the occupation of " + main_character + "?")
    occupation = input()
    print("Last question, what will be this story about? (Love, death, robots, friendship, money, coming-of-age, ...")
    topic = input()

    print(f"Now generating a {genre} story about {topic} with {main_character}, a brave {occupation}...")

    return (genre, main_character, occupation, topic)

if __name__ == "__main__":
    main()
