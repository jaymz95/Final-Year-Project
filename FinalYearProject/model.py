from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from .views import chatbot

conv = open('/home/jaymz95/Desktop/Final-Year-Project/FinalYearProject/yes.txt', 'r').readlines()

trainer = ListTrainer(chatbot)

trainer.train(conv)
