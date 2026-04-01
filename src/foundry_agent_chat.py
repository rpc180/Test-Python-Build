import os
import sys
from typing import Optional

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
from azure.core.exceptions import ClientAuthenticationError


PROJECT_ENDPOINT_ENV = "AZURE_AI_PROJECT_ENDPOINT"
AGENT_NAME_ENV = "AZURE_AI_AGENT_NAME"


def get_credential():
    """
    Try DefaultAzureCredential first for local dev.
    Fall back to InteractiveBrowserCredential if needed.
    """
    try:
        cred = DefaultAzureCredential()
        # Trigger token acquisition early so auth failures happen up front.
        cred.get_token("https://ai.azure.com/.default")
        print("Authenticated with DefaultAzureCredential.")
        return cred
    except Exception as ex:
        print("DefaultAzureCredential did not work.")
        print(f"Reason: {ex}")
        print("Falling back to InteractiveBrowserCredential...")
        cred = InteractiveBrowserCredential()
        cred.get_token("https://ai.azure.com/.default")
        print("Authenticated with InteractiveBrowserCredential.")
        return cred


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def create_project_client():
    endpoint = get_required_env(PROJECT_ENDPOINT_ENV)
    credential = get_credential()
    return AIProjectClient(endpoint=endpoint, credential=credential)


def main():
    try:
        endpoint = get_required_env(PROJECT_ENDPOINT_ENV)
        agent_name = get_required_env(AGENT_NAME_ENV)
    except ValueError as ex:
        print(ex)
        sys.exit(1)

    print("Starting Foundry agent chat test...")
    print(f"Project endpoint: {endpoint}")
    print(f"Agent name: {agent_name}")
    print("Type 'exit' to quit.\n")

    try:
        project = create_project_client()
        openai_client = project.get_openai_client()

        # One persistent conversation for multi-turn chat
        conversation = openai_client.conversations.create()
        print(f"Conversation created: {conversation.id}\n")

        while True:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in {"exit", "quit"}:
                print("Goodbye.")
                break

            try:
                response = openai_client.responses.create(
                    conversation=conversation.id,
                    input=user_input,
                    extra_body={
                        "agent_reference": {
                            "name": agent_name,
                            "type": "agent_reference"
                        }
                    },
                )

                print(f"\nAgent: {response.output_text}\n")

            except Exception as ex:
                print(f"\nRequest failed: {ex}\n")

    except ClientAuthenticationError as ex:
        print("Authentication failed.")
        print(ex)
        sys.exit(2)
    except Exception as ex:
        print("Application failed to start.")
        print(ex)
        sys.exit(3)


if __name__ == "__main__":
    main()