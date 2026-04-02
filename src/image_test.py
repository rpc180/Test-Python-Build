import os
from pathlib import Path
from dotenv import load_dotenv

from azure.ai.agents import AgentsClient
from azure.ai.agents.models import (
    ListSortOrder,
    MessageImageFileParam,
    MessageInputImageFileBlock,
    MessageInputTextBlock,
)
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential

# Load .env from project root
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
AGENT_ID = os.getenv("AZURE_AI_AGENT_ID")

# Change this to your test image path
IMAGE_PATH = Path(__file__).resolve().parent / "test_image1.jpg"


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


def prompt_mode():
    """
    Ask the user whether to send text only or an image.
    """
    while True:
        print("\nChoose input mode:")
        print("1 - Text message only")
        print("2 - Image file (with optional text prompt)")
        choice = input("Enter 1 or 2: ").strip()

        if choice == "1":
            return "text"
        if choice == "2":
            return "image"

        print("Invalid selection. Please enter 1 or 2.")


def prompt_text_message():
    """
    Get a text prompt from the user.
    """
    default_text = "Describe your purpose and capabilities."
    user_text = input(
        f"\nEnter the text message to send "
        f"(press Enter for default: '{default_text}'): "
    ).strip()

    return user_text if user_text else default_text


def prompt_image_path():
    """
    Ask for an image path and validate it exists.
    """
    while True:
        raw_path = input("\nEnter the path to the image file: ").strip().strip('"')
        image_path = Path(raw_path)

        if image_path.exists() and image_path.is_file():
            return image_path.resolve()

        print("File not found. Please enter a valid image file path.")


def prompt_optional_image_text():
    """
    Optional text that accompanies the image.
    """
    default_text = (
        "Evaluate this image for classified objects using your knowledge set. "
        "Return only matched classified objects and their approximate location."
    )
    user_text = input(
        f"\nEnter an optional text prompt for the image "
        f"(press Enter for default): "
    ).strip()

    return user_text if user_text else default_text


def print_message_contents(msg):
    """
    Print message text content. Also note when image content exists.
    """
    printed_anything = False

    if getattr(msg, "text_messages", None):
        for text_block in msg.text_messages:
            print(f"{msg.role}: {text_block.text.value}")
            printed_anything = True

    if getattr(msg, "image_contents", None):
        for _ in msg.image_contents:
            print(f"{msg.role}: [image content attached]")
            printed_anything = True

    if not printed_anything:
        print(f"{msg.role}: [no displayable content]")


def send_text_message(agents_client, thread_id, user_message):
    """
    Send a plain text message.
    """
    agents_client.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_message,
    )
    print("Text message sent.")


def send_image_message(agents_client, thread_id, image_path, user_prompt):
    """
    Upload an image and send it along with a text prompt as multimodal content.
    """
    uploaded_image = agents_client.files.upload_and_poll(
        file_path=str(image_path),
        purpose="assistants",
    )
    print(f"Uploaded image: {uploaded_image.id}")

    image_file = MessageImageFileParam(
        file_id=uploaded_image.id,
        detail="high",
    )

    content_blocks = [
        MessageInputTextBlock(text=user_prompt),
        MessageInputImageFileBlock(image_file=image_file),
    ]

    agents_client.messages.create(
        thread_id=thread_id,
        role="user",
        content=content_blocks,
    )
    print("Image + prompt message sent.")


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

    # Create a new thread
    thread = agents_client.threads.create()
    print(f"Created thread: {thread.id}")

    # Ask user what to send
    mode = prompt_mode()

    if mode == "text":
        user_message = prompt_text_message()
        send_text_message(agents_client, thread.id, user_message)

    elif mode == "image":
        image_path = prompt_image_path()
        user_prompt = prompt_optional_image_text()
        send_image_message(agents_client, thread.id, image_path, user_prompt)

    # Run the agent
    run = agents_client.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id,
    )

    print(f"\nRun status: {run.status}")

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")
        return

    # Read conversation output
    print("\nConversation output:")
    messages = agents_client.messages.list(
        thread_id=thread.id,
        order=ListSortOrder.ASCENDING,
    )

    for msg in messages:
        print_message_contents(msg)


if __name__ == "__main__":
    main()