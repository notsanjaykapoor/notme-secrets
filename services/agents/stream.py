import asyncio
import dataclasses

import pydantic_ai

import context
import log
import services.convs.msgs
import services.database

logger = log.init("agent")


@dataclasses.dataclass
class AgentChannel:
    agent: pydantic_ai.Agent
    conv_id: int
    iq: asyncio.Queue
    oq: asyncio.Queue
    user_id: int


async def stream_task(channel: AgentChannel):
    """
    Stream agent responses.


    """
    try:
        msgs_history = await _stream_history(channel=channel)

        await _stream_user(channel=channel, msgs_history=msgs_history)
    except Exception as e:
        breakpoint()  #
        logger.error(f"{context.rid_get()} stream_task exception - {e}")


async def _stream_history(channel: AgentChannel) -> list[pydantic_ai.messages.ModelMessage]:
    await channel.oq.put(["history-start", "", None])

    msgs_history: list[pydantic_ai.messages.ModelMessage] = []

    if channel.conv_id > 0:
        with services.database.session.get() as db_session:
            _code, model_msgs = services.convs.msgs.load_by_conv_id(db_session=db_session, conv_id=channel.conv_id)

            for model_msg in model_msgs:
                await channel.oq.put(["history-msg", "model-msg", model_msg])

            msgs_history.extend(model_msgs)

    await channel.oq.put(["history-end", "", None])

    return msgs_history


async def _stream_user(channel: AgentChannel, msgs_history: list[pydantic_ai.messages.ModelMessage]):
    kind: str
    msg: dict

    kind, msg = await channel.iq.get()

    if kind == "user-prompt":
        text = msg.get("text")
        request_id = msg.get("request_id")

        async with channel.agent.iter(user_prompt=text, message_history=msgs_history, deps={}) as agent_run:
            async for node in agent_run:
                # can be 1 of 4 different node types
                if pydantic_ai.Agent.is_model_request_node(node):
                    await channel.oq.put(["agent-node", "model-request-start", node])
                    # stream the model request node
                    async with node.stream(agent_run.ctx) as request_stream:
                        async for event in request_stream:
                            await channel.oq.put(["stream-event", "model-request", event])
                    await channel.oq.put(["agent-node", "model-request-end", None])
                elif pydantic_ai.Agent.is_call_tools_node(node):
                    await channel.oq.put(["agent-node", "tool-call-start", node])
                    # stream the tools node
                    async with node.stream(agent_run.ctx) as handle_stream:
                        async for event in handle_stream:
                            await channel.oq.put(["stream-event", "tool-call", event])
                    await channel.oq.put(["agent-node", "tool-call-end", None])
                elif pydantic_ai.Agent.is_user_prompt_node(node):
                    await channel.oq.put(["agent-node", "user-prompt", node])
                elif pydantic_ai.Agent.is_end_node(node):
                    await channel.oq.put(["agent-node", "turn-end", node])

            agent_result = agent_run.result
            model_msgs = agent_result.new_messages()

            msgs_history.extend(model_msgs)

            with services.database.session.get() as db_session:
                services.convs.msgs.persist(
                    db_session=db_session, conv_id=channel.conv_id, user_id=channel.user_id, model_msgs=model_msgs
                )
