import os
from pathlib import Path
from dotenv import load_dotenv

from azure.ai.agents import AgentsClient
from azure.ai.agents.models import ListSortOrder
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential

# Load .env from project root
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
AGENT_ID = os.getenv("AZURE_AI_AGENT_ID")

def get_credential():
    scope = "https://ai.azure.com/.default"

    try:
        cred = DefaultAzureCredential()
        cred.get_token(scope)
        print("Authenticated with DefaultAzureCredential.")
        return cred
    except Exception as ex:
        print(f"DefaultAzureCredential failed: {ex}")
        print("Falling back to InteractiveBrowserCredential...")

        cred = InteractiveBrowserCredential()
        cred.get_token(scope)
        print("Authenticated with InteractiveBrowserCredential.")
        return cred


def main():
    if not PROJECT_ENDPOINT:
        raise ValueError("AZURE_AI_PROJECT_ENDPOINT is missing from .env")

    credential = get_credential()

    agents_client = AgentsClient(
        endpoint=PROJECT_ENDPOINT,
        credential=credential,
    )

    # Optional sanity check
    agent = agents_client.get_agent(AGENT_ID)
    print(f"Using agent: {agent.name} / {agent.id}")

    # 1) Create a thread
    thread = agents_client.threads.create()
    print(f"Created thread: {thread.id}")

    # 2) Add one user message
    user_message = "Hello please respond with a short description of yourself."
    agents_client.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message,
    )
    print("User message sent.")

    # 3) Run the agent and wait for completion
    run = agents_client.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id,
    )

    print(f"Run status: {run.status}")

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")
        return

    # 4) Read back the messages
    print("\nConversation output:")
    messages = agents_client.messages.list(
        thread_id=thread.id,
        order=ListSortOrder.ASCENDING,
    )

    for msg in messages:
        if msg.text_messages:
            last_text = msg.text_messages[-1]
            print(f"{msg.role}: {last_text.text.value}")


if __name__ == "__main__":
    main()