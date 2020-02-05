from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


conv = open('yes', 'r').readlines()


# Create a new chat bot named Charlie
chatbot = ChatBot('Charlie')

trainer = ListTrainer(chatbot)

trainer.train(conv)

