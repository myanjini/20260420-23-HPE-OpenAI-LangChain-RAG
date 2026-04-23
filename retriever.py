# 임베딩 모델 선언
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding = OpenAIEmbeddings(model="text-embedding-3-large")


# FAISS DB를 로딩
from langchain_community.vectorstores import FAISS

persistent_directory = "./faiss_store"
db = FAISS.load_local(persistent_directory, embedding, allow_dangerous_deserialization=True)


# 검색 
# question = "뉴욕의 환경 정책이 궁금해."
retriever = db.as_retriever(search_kwargs={"k": 3})
# docs = retriever.invoke(question)


# 청크를 기반으로 사용자의 질문에 답변을 생성하는 체인을 구성
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI

chat = ChatOpenAI(model="gpt-4o-mini")

question_answer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "사용자 질문에 대해 아래 context에 기반해 답변해 주세요.\n\n{context}",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# create_stuff_documents_chain를 대체하는 LCEL 체인 구현
from langchain_core.runnables import RunnableLambda


# 문서 목록을 받아 하나의 문자열로 결합하는 함수
def format_docs(docs: list[Document]) -> str:
    # 각 Document 객체의 page_content를 추출해 줄바꿈 두 개(\n\n)로 연결
    return "\n\n".join(doc.page_content for doc in docs)


# 입력 딕셔너리에서 "documents"와 "messages"를 추출해 처리
document_chain = (
    # 1. 입력 딕셔너리를 프롬프트가 요구하는 키(content, messages)에 맞게 변환
    {
        # 'context' 키: 입력 x에서 'documents' 리스트를 추출하고, RunnableLambda로 래핑된 format_docs 함수를 통해 결합
        "context": (lambda x: x["documents"]) | RunnableLambda(format_docs),
        # 'messages' 키: 입력 x에서 'messages' 리스트를 그대로 추출
        "messages": lambda x: x["messages"],
    }
    # 2. 구성된 딕셔너리를 프롬프트 템플릿에 전달해 최종 PromptValue를 생성
    | question_answer_prompt
    # 3. PromptValue를 Chat 모델에 전달해 답변을 생성
    | chat
)


def retrieve_and_answer(question: str) -> str:
    # question = "뉴욕의 환경 정책이 궁금해."
    docs = retriever.invoke(question)
    for i, doc in enumerate(docs):
        print(f"Document {i+1}:\n{doc.page_content}\n{'-'*50}")

    # 메시지를 생성하고 질의하고 답변을 출력
    from langchain_core.messages import HumanMessage
    from langchain_community.chat_message_histories import ChatMessageHistory

    chat_history = ChatMessageHistory()

    chat_history.add_message(HumanMessage(content=question))

    answer = document_chain.invoke(
        {
            "documents": docs, "messages": chat_history.messages
        }
    )

    chat_history.add_message(answer)

    return answer.content

if __name__ == "__main__":
    question = "뉴욕의 환경 정책이 궁금해."
    answer = retrieve_and_answer(question)
    print("Answer:", answer)