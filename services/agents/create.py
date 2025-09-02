import os

import pydantic_ai
import pydantic_ai.models.anthropic
import pydantic_ai.models.google
import pydantic_ai.providers.anthropic
import pydantic_ai.providers.google

import services.anthropic

SYSTEM_PROMPT_OUTPUTS = "You are a helpful agent. Use one of the following tools to help compose your answer."

SYSTEM_PROMPT_TOOLS = (
    "You are a helpful agent. Be concise, reply with one sentence if possible. "
    "Never mention tools if you can't use them in the query."
)


def create_agent_anthropic(output_types: list = [str], tools: list = [], toolsets: list = []) -> pydantic_ai.Agent:
    agent = pydantic_ai.Agent(
        deps_type=dict,
        model=model_anthropic(),
        output_type=output_types,
        system_prompt=SYSTEM_PROMPT_TOOLS,
        tools=tools,
        toolsets=toolsets,
    )

    return agent


def create_agent_google(output_types: list = [str], tools: list = [], toolsets: list = []) -> pydantic_ai.Agent:
    agent = pydantic_ai.Agent(
        deps_type=dict,
        model=model_gemini(),  # "google-gla:gemini-1.5-flash"
        output_type=output_types,
        system_prompt=SYSTEM_PROMPT_TOOLS,
        tools=tools,
        toolsets=toolsets,
    )

    return agent


def create_agent_places(model: pydantic_ai.models, output_types: list) -> pydantic_ai.Agent:
    agent = pydantic_ai.Agent(
        deps_type=dict,
        model=model,
        output_type=output_types,
        system_prompt=SYSTEM_PROMPT_OUTPUTS,
        tools=[],
    )

    return agent


def model_anthropic() -> pydantic_ai.models:
    return pydantic_ai.models.anthropic.AnthropicModel(
        model_name=services.anthropic.query.MODEL_DEFAULT,
        provider=pydantic_ai.providers.anthropic.AnthropicProvider(api_key=os.getenv("ANTHROPIC_API_KEY")),
    )


def model_gemini() -> pydantic_ai.models:
    return pydantic_ai.models.google.GoogleModel(
        model_name="gemini-1.5-flash",
        provider=pydantic_ai.providers.google.GoogleProvider(api_key=os.getenv("GOOGLE_GEMINI_KEY"), vertexai=False),
    )
