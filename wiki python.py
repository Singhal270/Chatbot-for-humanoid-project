import wikipedia

while(True):
    name=input("topic :>")
    if name!="quit":
        try:
            text=wikipedia.summary(name ,sentences=10000)
            file=open('C:/Users/MOHIT SINGHAL/Desktop/projects/topic for chatbot.txt','a')
            file.write("\n\n")
            file.write(text)
            file.write("\n\n")
            file.close()
            print("....done.....")
        except:
            fh=open('C:/Users/MOHIT SINGHAL/Desktop/projects/wiki_not_found.txt','a')
            fh.write("\n")
            fh.write(name)
            fh.close()
            print(".....web page not found.....")
    else:
        break


   
	  
