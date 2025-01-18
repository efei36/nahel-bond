import anthropic
import os
from dotenv import load_dotenv
from audio import setup_text_to_speech, text_to_speech, speech_to_text, choose_input_mode, set_default_or_dynamic, TEXT, SPEECH, DYNAMIC

spren_profiles = {
    "Honorspren": "Honorspren value honesty, integrity, and duty. They are noble and straightforward but can be rigid in their principles. They can change their appearance, including forms like fire or clouds, although they always glow (but not illuminate), and are typically white-blue. This being said, they generally seem to prefer a humanoid form. Usually, it's very small -- only about a handspan tall -- but if need be, a honorspren can make themselves as tall as a regular person.",
    "Highspren": "Highspren are lawful and judgmental. They value order, rules, and accountability, but they can come across as stern. Highspren take the form of black slits in the air, which can pull open to reveal stars shining within. When they move, reality seems to bend around them.",
    "Ashspren": "Ashspren are bold, rebellious, and often mischievous. They like to break things around them to see what's inside. Ashspren appear as cracks that appear to grow on surfaces or branch through the air. When they move they seem to burn through the inside of objects in treelike patterns.",
    "Cultivationspren": "Cultivationspren are nurturing and focused on growth and change. They are thoughtful and deliberate, often offering wise insights. Cultivationspren take the form of a vine that grows rapidly. This vine appears to be speckled with smooth flecks of quartz, but it does not glow with Stormlight. They can form the appearance of a face by curling vines around one another. After a time, the vine trail they leave behind solidifies, becoming like crystal before crumbling into dust.",
    "Mistspren": "Mistspren are curious, enigmatic, and mystical. They often speak in riddles and metaphors, shrouding their insights in mystery. Mistspren resemble the shimmer light makes on a surface when it is reflected through a crystal. When they stay still, light grows upwards from them in the shape of plants, which retreat when they start moving.",
    "Cryptics": "Cryptics are mysterious and love patterns, secrets, and uncovering lies. They enjoy analyzing the meaning behind words and ideas. Cryptics manifest as complex fractal patterns that are constantly shifting, slightly raised off a surface or object. On occasion, they can also manifest as a floating three-dimensional mass of twisting lines. Their voice has a buzzing quality, and they vibrate when they speak. They also frequently hum.",
    "Inkspren": "Inkspren are logical and strategic thinkers. They are calm, collected, and value careful deliberation over hasty action. Inkspren are humanoid, and their form does not change. They have angular features, more reminiscent of an unfinished statue than a real person. They are entirely black, as if made of shadows, and have marble-like skin with a prismatic quality as though it has been coated in a thin layer of oil. Their skin shimmers and gleams in a variety of colors depending on how the light hits it. They are able to change their size.",
    "Reachers": "Reachers are friendly and easygoing, often serving as mediators. They value connections and harmony among people. Reachers appear as a ball of light, small enough to hide in a palm of a hand. When they move, they trail around a glowing streak, making them look like a comet.",
    "Peakspren": "Peakspren are energetic and enthusiastic, brimming with optimism. They inspire and encourage others around them. Peakspren take forms that appear to be made of stone. They can hide inside real rocks if they wish; when they want to reappear, they emerge as if breaking their form out of the rock.",
}



def select_conversation_partner():
    print("\nChoose a True Spren to chat with:")
    for i, spren in enumerate(spren_profiles.keys(), 1):
        print(f"  {i}. {spren}")

    while True:
        try:
            choice = int(input("Enter the number corresponding to your chosen spren: "))
            if 1 <= choice <= len(spren_profiles):
                selected_spren = list(spren_profiles.keys())[choice - 1]
                return selected_spren, spren_profiles[selected_spren]
            else:
                print("Invalid choice. Please select a number from the list.")
        except ValueError:
            print("Please enter a valid number.")



def chat_with_partner(client, spren_type, spren_description, input_mode):
    dialogue_separator = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    if spren_type == "Cryptics" or spren_type == "Reachers":
        spren_type = spren_type[:-1]
    
    print(f"You are now chatting with a {spren_type}.\n")
    print("Type 'exit' to end the conversation.\n")
    print(f"{dialogue_separator}\n")

    engine = setup_text_to_speech()
    is_dynamic = True if input_mode == DYNAMIC else False

    system_prompt = f"You are a {spren_type} from The Stormlight Archive. You embody the following traits: {spren_description}. Engage in conversation while staying true to your character."
    conversation_history = []

    while True:
        try:
            if is_dynamic:
                input_mode = choose_input_mode()

            user_message = ""
            if input_mode == TEXT:
                user_message = input("You: ")
            elif input_mode == SPEECH:
                user_message = speech_to_text(f"The {spren_type} listens as you speak...")
                print(f"You: {user_message}")

            if user_message.lower() == "exit":
                print(f"The {spren_type} bids you farewell. Goodbye!")
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
            print(f"{spren_type}:\n{formatted_reply}\n")
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
    
    client = anthropic.Anthropic(api_key=USER_API_KEY)
    input_mode = set_default_or_dynamic()
    spren_type, spren_description = select_conversation_partner()

    chat_with_partner(client, spren_type, spren_description, input_mode)



if __name__ == "__main__":
    main()