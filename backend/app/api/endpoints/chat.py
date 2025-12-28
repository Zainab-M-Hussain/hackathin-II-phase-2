from fastapi import APIRouter, Depends
from pydantic import BaseModel
from openai import OpenAI
from app.tools.registry import tool_registry
from app.database import get_session # Import get_session
from sqlmodel import Session # Import Session
import os
import json

router = APIRouter()

def get_openai_client():
    """Create and return an OpenAI client, initializing it only when needed."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return OpenAI(api_key=api_key)

# Get tools from registry
add_task_tool = tool_registry.get_tool_instance("add_task")
list_tasks_tool = tool_registry.get_tool_instance("list_tasks")
update_task_tool = tool_registry.get_tool_instance("update_task")
delete_task_tool = tool_registry.get_tool_instance("delete_task")
toggle_completion_tool = tool_registry.get_tool_instance("toggle_task_completion")

# Define tools schema
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": add_task_tool.description,
            "parameters": add_task_tool.parameters,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": list_tasks_tool.description,
            "parameters": list_tasks_tool.parameters,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Marks a task as complete.",
            "parameters": toggle_completion_tool.parameters,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": delete_task_tool.description,
            "parameters": delete_task_tool.parameters,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": update_task_tool.description,
            "parameters": update_task_tool.parameters,
        },
    },
]

class ChatRequest(BaseModel):
    message: str
    locale: str = "en"

@router.post("/")
def chat(request: ChatRequest, session: Session = Depends(get_session)):
    client = get_openai_client()

    # Create the assistant inside the function
    # Use the locale from the request, defaulting to English
    language_instruction = "Please respond in English." if request.locale == "en" else f"Please respond in {request.locale}."
    assistant = client.beta.assistants.create(
        name="Task Manager",
        instructions=f"You are a helpful assistant for managing tasks. {language_instruction} When creating tasks, always use the default user ID '00000000-0000-0000-0000-000000000001' unless the user explicitly specifies another valid user ID. Do not ask the user for their UUID, instead use the default ID automatically.",
        tools=tools,
        model="gpt-4o",
    )

    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=request.message,
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run.status == "requires_action":
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # For all operations that require a user_id, ensure it's set to default if missing
                if function_name in ["add_task", "list_tasks", "update_task", "delete_task", "complete_task", "toggle_task_completion"]:
                    if "user_id" not in function_args or not function_args["user_id"]:
                        function_args["user_id"] = "00000000-0000-0000-0000-000000000001"

                if function_name == "add_task":
                    # Execute the tool using the synchronous method
                    output = tool_registry.execute_tool("add_task", **function_args)
                    tool_outputs.append(
                        {
                            "tool_call_id": tool_call.id,
                            "output": json.dumps(output),
                        }
                    )
                elif function_name == "list_tasks":
                    output = tool_registry.execute_tool("list_tasks", **function_args)
                    tool_outputs.append(
                        {
                            "tool_call_id": tool_call.id,
                            "output": json.dumps(output),
                        }
                    )
                elif function_name == "complete_task":
                    # For complete_task, we need to toggle the completion status
                    output = tool_registry.execute_tool("toggle_task_completion", **function_args)
                    tool_outputs.append(
                        {
                            "tool_call_id": tool_call.id,
                            "output": json.dumps(output),
                        }
                    )
                elif function_name == "delete_task":
                    output = tool_registry.execute_tool("delete_task", **function_args)
                    tool_outputs.append(
                        {
                            "tool_call_id": tool_call.id,
                            "output": json.dumps(output),
                        }
                    )
                elif function_name == "update_task":
                    output = tool_registry.execute_tool("update_task", **function_args)
                    tool_outputs.append(
                        {
                            "tool_call_id": tool_call.id,
                            "output": json.dumps(output),
                        }
                    )
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
            )

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    return {"response": messages.data[0].content[0].text.value}
