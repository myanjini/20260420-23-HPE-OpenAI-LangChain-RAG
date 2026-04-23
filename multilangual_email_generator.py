# 패키지 임포트
import logging
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_community.llms.ctransformers import CTransformers
from langchain_ollama.llms import OllamaLLM

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# LLM 응답을 생성하는 함수
def getLLMResponse(email_subject, email_sender, email_recipient, email_language):
    # 언어별 템플릿 정의
    if email_language == "한국어":
        template = """
{subject} 주제를 포함한 이메일을 작성해 주세요. 

보낸 사람: {sender}
받는 사람: {recipient}

전부 {language}로 번역해서 작성해 주세요. 

이메일 내용: """
    else:
        template = """
Write an email including the topic {subject}.

Sender: {sender}
Recipient: {recipient}

Please write the entire email in {language}.

Email content: """

    # 프롬프트 생성
    prompt = PromptTemplate(
        input_variables=["subject", "sender", "recipient", "language"],
        template=template,
    )

    # 언어별 LLM 모델 설정
    if email_language == "한국어":
        llm = OllamaLLM(model="llama3.1:8b", temperature=0.7)
    else:
        llm = CTransformers(
            model="./llama-2-7b-chat.ggmlv3.q8_0.bin",
            # model="./llama-2-7b-chat.Q8_0.gguf",
            model_type="llama",
            # config={"max_new_tokens": 1024, "temperature": 0.7},
            config={"max_new_tokens": 512, "temperature": 0.01},
        )

    # LLM을 사용해 응답 생성
    response = llm.invoke(
        prompt.format(
            subject=email_subject,
            sender=email_sender,
            recipient=email_recipient,
            language=email_language,
        )
    )

    logger.info(f"LLM: {llm}")
    logger.debug(f"Response: {response}")

    return response


# Streamlit 앱 구성
st.set_page_config(
    page_title="이메일 생성기",
    page_icon="📧",
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.header("이메일 생성기 📧")

email_language = st.selectbox(
    "이메일 작성에 사용할 언어를 선택하세요.", ["한국어", "English"]
)

email_subject = st.text_area("이메일 주제를 입력하세요.", height=100)

col1, col2 = st.columns([10, 10])
with col1:
    email_sender = st.text_input("보내는 사람 이름")
with col2:
    email_recipient = st.text_input("받는 사람 이름")

submit = st.button("이메일 생성")
if submit:
    with st.spinner("이메일을 생성하고 있습니다..."):
        try:
            response = getLLMResponse(
                email_subject, email_sender, email_recipient, email_language
            )
            st.write(response)
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
