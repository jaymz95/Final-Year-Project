from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


conv = open('/home/jaymz95/Desktop/Final-Year-Project/FinalYearProject/yes.txt', 'r').readlines()


# Create a new chat bot named Charlie
chatbot = ChatBot('Charlie')

trainer = ListTrainer(chatbot)

trainer.train(conv)

f= open("guru99.txt","w+")

for i in range(10):
    f.write("This is line %d\r\n" % (i+1))

    f.close() 

