from gtts import gTTS
import os

# Mock data extracted from https://gojaneducation.com/
gojan_school_info = {
    "name": "Gojan School of Business and Technology",
    "location": "Chennai, Tamil Nadu",
    "courses": {
        "English": "Gojan School of Business and Technology offers a wide range of courses including MBA, BBA, B.Com, BCA, and M.Com. The programs are designed to provide students with practical knowledge and industry exposure.",
        "Tamil": "கோஜன் பிசினஸ் அண்ட் டெக்னாலஜி பள்ளி எம்பிஏ, பிபிஏ, பி.காம், பிசிஏ மற்றும் எம்.காம் போன்ற பல்வேறு படிப்புகளை வழங்குகிறது. இந்த திட்டங்கள் மாணவர்களுக்கு நடைமுறை அறிவு மற்றும் தொழில் அனுபவத்தை வழங்க வடிவமைக்கப்பட்டுள்ளன."
    },
    "facilities": {
        "English": "The school boasts state-of-the-art facilities including modern classrooms, a well-equipped library, computer labs, and sports facilities. The campus provides a conducive environment for learning and personal growth.",
        "Tamil": "இந்த பள்ளியில் நவீன வகுப்பறைகள், நன்கு அமைக்கப்பட்ட நூலகம், கணினி ஆய்வகங்கள் மற்றும் விளையாட்டு வசதிகள் உள்ளன. வளாகம் கற்றல் மற்றும் தனிப்பட்ட வளர்ச்சிக்கு ஏற்ற சூழலை வழங்குகிறது."
    },
    "achievements": {
        "English": "Gojan School of Business and Technology has been recognized for its excellence in education and has produced many successful alumni who are leaders in their respective fields.",
        "Tamil": "கோஜன் பிசினஸ் அண்ட் டெக்னாலஜி பள்ளி கல்வித் துறையில் சிறந்து விளங்குவதற்காக அங்கீகரிக்கப்பட்டுள்ளது மற்றும் பல வெற்றிகரமான முன்னாள் மாணவர்களை உருவாக்கியுள்ளது, அவர்கள் தங்கள் துறைகளில் தலைவர்களாக உள்ளனர்."
    }
}

# Function to convert text to speech using gTTS
def text_to_speech(text, language="en"):
    try:
        # Map languages to gTTS language codes
        lang_codes = {
            "English": "en",
            "Tamil": "ta"
        }
        lang_code = lang_codes.get(language, "en")  # Default to English if language not found

        # Use gTTS for text-to-speech
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save("gojan_info.mp3")
        os.system("start gojan_info.mp3")  # For Windows
        # os.system("afplay gojan_info.mp3")  # For macOS
        # os.system("mpg321 gojan_info.mp3")  # For Linux
    except Exception as e:
        print(f"An error occurred while converting text to speech: {e}")

# Function to provide information about Gojan School
def provide_gojan_info(category, language="English"):
    if category not in gojan_school_info:
        print("Category not found.")
        return

    info = gojan_school_info[category][language]
    print(f"{category} ({language}): {info}")
    text_to_speech(info, language)

# Main function for user interaction
def main():
    print("Welcome to the Gojan School of Business and Technology Voice Assistant!")
    print("Choose a category to learn more:")
    print("1. Courses")
    print("2. Facilities")
    print("3. Achievements")

    category_choice = input("Enter the number of your choice: ").strip()
    categories = {
        "1": "courses",
        "2": "facilities",
        "3": "achievements"
    }
    category = categories.get(category_choice)

    if not category:
        print("Invalid choice. Please try again.")
        return

    language_choice = input("Choose language (0 for English, 1 for Tamil): ").strip()
    languages = {
        "0": "English",
        "1": "Tamil"
    }
    language = languages.get(language_choice)

    if not language:
        print("Invalid language choice. Defaulting to English.")
        language = "English"

    provide_gojan_info(category, language)

# Run the program
if __name__ == "__main__":
    main()