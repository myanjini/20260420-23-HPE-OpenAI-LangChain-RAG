import asyncio

from agents import Agent, Runner, function_tool
from dotenv import load_dotenv


load_dotenv()


@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."


@function_tool
def get_current_time(city: str, tz: str = "Asia/Seoul") -> str:
    """
    지정된 타임존과 도시의 현재 시간을 반환합니다.
    """
    from datetime import datetime
    from pytz import timezone

    print(tz)

    local_now = datetime.now(timezone(tz))
    print(city, local_now)

    return f"{city}의 현재 시간은 {local_now}입니다."


agent = Agent(
    name="Hello world",
    instructions="You are a helpful agent.",
    tools=[get_weather, get_current_time],
)

print(agent.get_prompt)


async def main():
    result = await Runner.run(agent, input="도쿄 현재 시간과 날씨는?")
    print(result.raw_responses)
    print()
    print(result.final_output)
    # The weather in Tokyo is sunny.


if __name__ == "__main__":
    asyncio.run(main())
