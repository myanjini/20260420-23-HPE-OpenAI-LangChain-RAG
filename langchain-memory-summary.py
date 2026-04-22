from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.memory import ConversationSummaryMemory
from langchain_core.prompts  import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()
model = ChatOpenAI(model="gpt-4.1-nano")

memory = ConversationSummaryMemory(llm=model, return_messages=True)

prompt = ChatPromptTemplate.from_messages([
    ("system", "사용자의 질문에 친절하게 답해줘."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")     
])

chain = prompt | model

while True: 
    user_input = input("사용자: ")
    if user_input.lower() == "exit":
        break

    history = memory.load_memory_variables({})["history"]    
    ai_message = chain.invoke({"history": history, "input": user_input})

    print(f"상담사: {ai_message.content}")
    print()

    memory.save_context({"input": user_input}, {"output": ai_message.content})


#print(memory)
print("-" * 50)
#print(history)
for msg in history:
    print(f"{msg.__class__.__name__}\t{msg.content}")

print("-" * 50)
print(memory.buffer)   
