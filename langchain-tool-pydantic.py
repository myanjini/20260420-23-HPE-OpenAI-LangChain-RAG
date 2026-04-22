import pytz
from datetime import datetime
from langchain_core.tools import tool
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


load_dotenv()
model = ChatOpenAI(model="gpt-4o")


# 함수 입력값 형식을 정의 
from pydantic import BaseModel, Field

class StockHistoryInput(BaseModel):
    ticker: str = Field(..., title="주식 코드", description="주식 코드 (예: AAPL)")
    period: str = Field(..., title="기간", description="주식 데이터 조회 기간 (예: 1d, 1mo, 1y)")


# get_yf_stock_history 함수를 정의 
import yfinance as yf 

@tool
def get_yf_stock_history(stock_history_input: StockHistoryInput) -> str:
    """ 주식 종목의 가격 데이터를 조회하는 함수 """

    stock = yf.Ticker(stock_history_input.ticker)
    history = stock.history(period=stock_history_input.period)
    history_md = history.to_markdown()
    
    return history_md


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


# get_current_time, get_yf_stock_history 함수를 랭체인으로 언어 모델에 연결
tools = [get_current_time, get_yf_stock_history]
tool_dict = {
    "get_current_time": get_current_time, 
    "get_yf_stock_history": get_yf_stock_history
}


# 도구를 모델에 바인딩
llm_with_tools = model.bind_tools(tools)



# 도구를 사용해 언어 모델 답변 생성
messages = [
    SystemMessage("당신은 사용자의 질문에 답변을 하기 위해 tools를 사용할 수 있다."),
        HumanMessage("부산은 지금 몇 시고, 테슬라의 최근 3일간 주가 정보는 어떻게 되지?")
]

response = llm_with_tools.invoke(messages)
messages.append(response)


for tool_call in response.tool_calls:
    selected_tool = tool_dict.get(tool_call["name"])
    tool_msg = selected_tool.invoke(tool_call)
    messages.append(tool_msg)

response = llm_with_tools.invoke(messages)
print(response.content)


print(messages)