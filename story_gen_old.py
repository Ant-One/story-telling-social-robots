import random
from transformers import pipeline


generator = pipeline('text-generation', model ='EleutherAI/gpt-neo-125M')

max_iterations = 3
results = []

starts = ("Once upon a time in a beautiful country, there was a ", "Long ago in a far far country, some ", "Today is gonna be the day where I ", "What if I were to disguise fast food as my own invention? I could ")
beginning = random.choice(starts)
print("CHOOSEN START: " + beginning)
generated_text = generator(beginning, min_length=20, max_length=100, do_sample=True, temperature=0.9) #TODO use CUDA
new_generated_text = generated_text

print("ROUND 0" + " TEXT:\n" + new_generated_text[0].get("generated_text"))

#print(generated_text[0].get("generated_text")) #how to get text
results.append(new_generated_text[0].get("generated_text"))
#TODO remove repeated text
for i in range(0, max_iterations):
  new_start = getLastSentence(new_generated_text[0].get("generated_text"))
  print("FEEDING ROUND " + str(i + 1) + " :")
  print(new_start + "\n")
  new_generated_text = generator(new_start, min_length=20, max_length=100, do_sample=True, temperature=0.9)
  print("TEXT GENERATED ROUND " + str(i + 1) + " :\n" + new_generated_text[0].get("generated_text"))
  results.append(new_generated_text[0].get("generated_text"))

#Utils

def getLastSentence(text):
  sub_string = ""
  if "." in text:
    sub_string = text.split(".")[-2]#We want the last complete sentence
  else:
    print("no separation found. using now: " + sub_string)
    word_list = text.split()[-3:] #we arbitrarely take the last 3 words
    for element in word_list:
      sub_string += (element + " ")

  if sub_string[-1] != ".":
    sub_string += "."
      
  return sub_string

def flatten(l):
  output = ""
  for elem in l:
    output += elem
  return output