import os

import pydantic_ai
import pydantic_ai.models.anthropic
import pydantic_ai.models.google
import pydantic_ai.providers.anthropic
import pydantic_ai.providers.google

import services.anthropic

system_prompt_general = "You are a helpful agent."

system_prompt_outputs = (
    "You are a helpful agent. Use one of the following tools if possible to help compose your answer."
)


def create_agent_general(
    model: pydantic_ai.models, output_types: list = [str], tools: list = [], toolsets: list = []
) -> pydantic_ai.Agent:
    agent = pydantic_ai.Agent(
        builtin_tools=[pydantic_ai.WebSearchTool(max_uses=1, search_context_size="low")],
        deps_type=dict,
        model=model,
        output_type=output_types,
        system_prompt=system_prompt_general,
        tools=tools,
        toolsets=toolsets,
    )

    return agent


def create_agent_places(model: pydantic_ai.models, output_types: list) -> pydantic_ai.Agent:
    agent = pydantic_ai.Agent(
        deps_type=dict,
        model=model,
        output_type=output_types,
        system_prompt=system_prompt_outputs,
        tools=[],
    )

    return agent


def model_anthropic() -> pydantic_ai.models:
    settings = pydantic_ai.models.ModelSettings(parallel_tool_calls=True)

    return pydantic_ai.models.anthropic.AnthropicModel(
        model_name=services.anthropic.query.MODEL_DEFAULT,
        provider=pydantic_ai.providers.anthropic.AnthropicProvider(api_key=os.getenv("ANTHROPIC_API_KEY")),
        settings=settings,
    )


def model_gemini() -> pydantic_ai.models:
    return pydantic_ai.models.google.GoogleModel(
        model_name="gemini-1.5-flash",
        provider=pydantic_ai.providers.google.GoogleProvider(api_key=os.getenv("GOOGLE_GEMINI_KEY"), vertexai=False),
    )
