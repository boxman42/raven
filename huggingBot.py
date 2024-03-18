"""
This is a general framework for the godel text generation model. 
Initalize the bot with a godel model from https://huggingface.co/.
By default, the bot uses facebook/blenderbot-400M-distill. alternative model: facebook/blenderbot-3B
Use readInUtterances() to add to the conversation. this is done to keep context in the chatbot.
Use generateresponse() to generater a resonse to the latest message.
"""

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class huggingBot:
    def __init__(self, modelName:str="microsoft/GODEL-v1_1-base-seq2seq", maxTokens:int=500) -> None:
        self.name = modelName
        self.tokenizer = AutoTokenizer.from_pretrained(modelName)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(modelName)
        self.chatHistory = [] #all utterances
        self.chatHistoryLength = 0 #this is the number of tokens curently in the chat history
        self.maxTokens = maxTokens #the maxamum number of tokens the model can hendel
        self.knowledgeBase = "" #background information for the lm to use
        self.instruction = "Instruction: given a dialog context, you need to response empathically." #you have to tell the lm to be nice
    
    def setKnowledgeBase(self, text:str):
        self.knowledgeBase = text
    
    def setInstruction(self, text:str):
        self.instruction = text
    
    def setModel(self, modelName:str):
        """
        Model should really be passed in on initalization but this is here just in case you want to chnage it post initialization for dome reason.
        """
        self.name = modelName
        self.tokenizer = AutoTokenizer.from_pretrained(modelName)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(modelName)

    def readInUtterance(self, utterance:str):
        """
        The language model uses a colection of utterances in sequance to determine/generate a response. by using a chat history, context is kept in the conversation.
        The lm struggles to process any more then 500 tokens at a time so we must keep track of the number. This is a rough count as tokenization chnages the number words to tokens.
        if the number of tokens (chatHistotyLength) exceeds 500, we remove the first utterance of the chat history as it is unlikely it is still relevent. 
        """
        self.chatHistoryLength += len(utterance.strip().split()) #numer of words (aprox num of tokens)
        if self.chatHistoryLength >= self.maxTokens:
            self.chatHistoryLength -= len(self.chatHistory[0].split()) #subtract the length of the first elemnt from the chat count
            self.chatHistory = self.chatHistory[1:] #remove the first utterance from the list
        self.chatHistory.append(utterance)
    
    def generateResponse(self) -> str:
        knowledge = '[KNOWLEDGE] ' + self.knowledgeBase
        dialog = ' EOS '.join(self.chatHistory) #convert dialog into a string where each element is seperated by EOS
        query = f"{self.instruction} [CONTEXT] {dialog}. {knowledge}"
        #print(f"Godel query:{query}")
        input_ids = self.tokenizer(f"{query}", return_tensors="pt").input_ids
        tokenResponse = self.model.generate(input_ids, max_length=128, min_length=10, top_p=0.9, do_sample=True) #(tokenized version of our information, max number of words in output text, min number of words in output text)
        response = self.tokenizer.decode(tokenResponse[0], skip_special_tokens=True)
        self.readInUtterance(response) #this is done so the model knows the last thing it said.
        return response