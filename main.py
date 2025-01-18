import anthropic
import os
from dotenv import load_dotenv
from audio import setup_text_to_speech, text_to_speech, speech_to_text, choose_input_mode, set_default_or_dynamic, TEXT, SPEECH, DYNAMIC
from default_spren_characters import select_spren_partner

CUSTOM_PARTNER = 1
SPREN_PARTNER = 2



def choose_conversation_partner():
    print("\nChoose your conversation partner:")
    print("  1. Create your own partner")
    print("  2. Select a pre provided spren conversation partner")

    while True:
        try:
            choice = int(input("Enter the number corresponding to your choice: "))
            if choice == 1:
                return CUSTOM_PARTNER
            elif choice == 2:
                return SPREN_PARTNER
            else:
                print("Invalid choice. Please select 1 or 2.")
        except ValueError:
            print("Please enter a valid number.")



def create_conversation_partner():
    print("\nChoose a name for your conversation partner")
    name = input("  Name: ")
    print("\nNext, create a background for your character. You can include their history, characterization, quirks, appearance, etc.")
    background = input("  Background: ")
    return name, background



def chat_with_partner(client, partner_name, partner_description, input_mode, is_custom):
    dialogue_separator = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

    inital_text = (
        f"You are now chatting with {partner_name}.\n"
        if is_custom else
        f"You are now chatting with a {partner_name}.\n"
    )
    print(inital_text)
    print("Type 'exit' to end the conversation.\n")
    print(f"{dialogue_separator}\n")

    engine = setup_text_to_speech()
    is_dynamic = True if input_mode == DYNAMIC else False

    listen_text = f"{partner_name} listens as you speak..." if is_custom else f"The {partner_name} listens as you speak..."
    farewell_text = f"{partner_name} bids you farewell. Goodbye!" if is_custom else f"The {partner_name} bids you farewell. Goodbye!"

    system_prompt = (
        f"Your name is {partner_name}. You embody the following traits: {partner_description}. Engage in conversation while staying true to your character." 
        if is_custom else 
        f"You are a {partner_name} from The Stormlight Archive. You embody the following traits: {partner_description}. Engage in conversation while staying true to your character."
    )
    conversation_history = []

    while True:
        try:
            if is_dynamic:
                input_mode = choose_input_mode()

            user_message = ""
            if input_mode == TEXT:
                user_message = input("You: ")
            elif input_mode == SPEECH:
                user_message = speech_to_text(listen_text)
                print(f"You: {user_message}")

            if user_message.lower() == "exit":
                print(farewell_text)
                break

            conversation_history.append({"role": "user", "content": user_message})

            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=512,
                temperature=0,
                system=system_prompt,
                messages=conversation_history
            )
            
            formatted_reply = "".join(_.text for _ in response.content)
            print(f"\n{dialogue_separator}\n")
            print(f"{partner_name}:\n{formatted_reply}\n")
            print(f"{dialogue_separator}\n")

            if input_mode == SPEECH:
                text_to_speech(engine, formatted_reply)

            conversation_history.append({"role": "assistant", "content": formatted_reply})
        except Exception as e:
            print(f"An error occurred: {e}")
            break



def main():
    """Main function to run the chatbot program."""
    load_dotenv()
    USER_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    if not USER_API_KEY:
        print("Error: API key not found. Please set ANTHROPIC_API_KEY in your .env file.")
        return
    
    is_custom = False
    partner_name = ""
    partner_description = ""

    if choose_conversation_partner() == CUSTOM_PARTNER:
        partner_name, partner_description = create_conversation_partner()
        is_custom = True
    else:
        partner_name, partner_description = select_spren_partner()

    client = anthropic.Anthropic(api_key=USER_API_KEY)
    input_mode = set_default_or_dynamic()

    chat_with_partner(client, partner_name, partner_description, input_mode, is_custom)



if __name__ == "__main__":
    main()