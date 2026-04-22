from agents import Agent, Runner
import asyncio
from dotenv import load_dotenv

load_dotenv()

korean_agent = Agent(
    name="Korean agent",
    instructions="You only speak Korean.",
)

spanish_agent = Agent(
    name="Spanish agent",
    instructions="You only speak Spanish.",
)

english_agent = Agent(
    name="English agent",
    instructions="You only speak English",
)

triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[korean_agent, spanish_agent, english_agent],
)


async def main():
    result = await Runner.run(
        triage_agent,
        input="안녕하세요. 어떻게 지내세요?",
        # input="Hola, ¿cómo estás?"
    )
    print(type(result))
    print("-" * 50)
    print(result)
    print("-" * 50)
    print(result.new_items)
    print("-" * 50)
    print(result.raw_responses)
    print("-" * 50)
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
