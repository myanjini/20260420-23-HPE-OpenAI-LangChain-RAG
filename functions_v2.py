from datetime import datetime
import pytz


# pytz을 사용해 문자열 형식으로 받은 타임존을 파이썬 타임존 인스턴스로 만들고,
# 이를 datetime.now()에 전달해 해당 타임존의 현재 시간을 반환
def get_current_time(timezone: str = "Asia/Seoul"):
    tz = pytz.timezone(timezone)
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    now_timezone = f"{now} {timezone}"
    return now_timezone


# 함수 호출을 위한 메타데이터
tools = [
    {
        "type": "function",
        "name": "get_current_time",
        "description": "타임존의 현재 날짜와 시간을 'YYYY-MM-DD HH:MM:SS' 형식으로 반환합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": "현재 날짜와 시간을 반환할 타임존을 입력하세요. (예: 'Asia/Seoul')",
                },
            },
            "required": ["timezone"],
        },
    }
]

if __name__ == "__main__":
    current_time = get_current_time("Asia/Seoul")
    print(current_time)
