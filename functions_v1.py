from datetime import datetime

# 현재 날짜와 시간을 "YYYY-MM-DD HH:MI:SS" 형식으로 반환하는 함수
def get_current_time():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return now


# 함수 호출을 위한 메타데이터
tools = [
    {
        "type": "function",
        "name": "get_current_time",
        "description": "현재 날짜와 시간을 'YYYY-MM-DD HH:MM:SS' 형식으로 반환합니다.",
    }
]


if __name__ == "__main__":
    current_time = get_current_time()
    print(current_time)
