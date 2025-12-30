import random
from abc import ABC,abstractmethod

class Runnable(ABC):
    @abstractmethod
    def invoke(input_data):
        pass

class NakliLLM(Runnable):
    def __init__(self):
        print("LLM created")

    def invoke(self,prompt):
        response_list=[
            'Delhi is the capital of India',
            'IPL is cricket League',
            'Ai stands for Artificial Intelligence'
        ]
        return {
            'response':random.choice(response_list)
        }

    
    def predict(self,prompt):
        response_list=[
            'Delhi is the capital of India',
            'IPL is cricket League',
            'Ai stands for Artificial Intelligence'
        ]
        return {
            'response':random.choice(response_list)
        }

class NakliPromptTemplate(Runnable):
    def __init__(self,template,input_variables):
        self.template=template
        self.input_variables=input_variables

    def invoke(self,input_dict):
        return self.template.format(**input_dict)


class RunnableConnector(Runnable):
    def __init__(self,runnable_list:list):
        self.runnable_list=runnable_list

    def invoke(self,input_data):
        for runnable in self.runnable_list:
            input_data=runnable.invoke(input_data)      
        return input_data  

class NakliStrOutputParser(Runnable):
    def __init__(self):
        pass 
    def invoke(self,input_data):
        return input_data['response']


llm=NakliLLM()

template=NakliPromptTemplate(
    template='Write a poem about {topic}',
    input_variables=['topic']
)

template2=NakliPromptTemplate(
    template="Explain this joke : \n{joke} ",
    input_variables=['joke']
)
    
parser=NakliStrOutputParser()

chain=RunnableConnector([template,llm,parser])


chain2=RunnableConnector([template2,llm,parser])

chain3=RunnableConnector([chain,chain2])

result=chain3.invoke({
    'topic':'India',
})

print(result)