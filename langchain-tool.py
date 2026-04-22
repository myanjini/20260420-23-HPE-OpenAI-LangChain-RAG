import pytz
from datetime import datetime
from langchain_core.tools import tool
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


load_dotenv()
# model = ChatOpenAI(model="gpt-4o")

from langchain_anthropic import ChatAnthropic
model = ChatAnthropic(model="claude-haiku-4-5-20251001")


@tool
def get_current_time(timezone: str, location: str) -> str:
    """
        현재 시간을 YYYY-MM-DD HH:MI:SS 형식으로 반환하는 함수
       
        Args:
            timezone (str): 타임존(예: "Asia/Seoul"). 실제 존재해야 함.
            location (str): 지역명. 타임존은 모든 지역에 대응하지 않으며, 이후 llm 답변 생성에 사용됨.
    """
    tz = pytz.timezone(timezone)
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    return f"{timezone} ({location}) 현재시간 {now}"

@tool
def new_function():
    """
    새로운 함수입니다.
    """
    return "새로운 함수입니다."

# get_current_time 함수를 랭체인으로 언어 모델에 연결


tools = [get_current_time, new_function]
tool_dict = {
    "get_current_time": get_current_time, 
    "new_function": new_function
}


# 도구를 모델에 바인딩
llm_with_tools = model.bind_tools(tools)



# 도구를 사용해 언어 모델 답변 생성


messages = [
    SystemMessage("당신은 사용자의 질문에 답변을 하기 위해 tools를 사용할 수 있다."),
    HumanMessage("부산은 지금 몇 시야?")
]


response = llm_with_tools.invoke(messages)
messages.append(response)


# print(response)
# print("-" * 50)
# print(messages)


for tool_call in response.tool_calls:
    selected_tool = tool_dict.get(tool_call["name"])
    tool_msg = selected_tool.invoke(tool_call)
    messages.append(tool_msg)

# print(messages)

response = llm_with_tools.invoke(messages)
print(response.content)