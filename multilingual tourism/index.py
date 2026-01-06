from gtts import gTTS
import os
import json
import time
import pygame
from datetime import datetime

# Initialize pygame mixer for better audio handling
pygame.mixer.init()

# Heritage spots data for Tamil Nadu
heritage_spots = {
    "Meenakshi Temple": {
        "location": "Madurai",
        "description": {
            "English": "The Meenakshi Amman Temple is a historic Hindu temple located on the southern bank of the Vaigai River. It is dedicated to Parvati (Meenakshi) and Shiva (Sundareswarar). The temple complex is famous for its 14 gopurams (gateway towers), with the tallest southern tower reaching 170 feet. It is one of the largest temple complexes in Tamil Nadu and a masterpiece of Dravidian architecture.",
            "Tamil": "மீனாட்சி அம்மன் கோவில் வைகை நதியின் தெற்குக் கரையில் அமைந்துள்ள ஒரு வரலாற்று இந்துக்கோயிலாகும். இது பார்வதி (மீனாட்சி) மற்றும் சிவன் (சுந்தரேஸ்வரர்) ஆகியோருக்கு அர்ப்பணிக்கப்பட்டுள்ளது. இக்கோவில் வளாகம் 14 கோபுரங்களுக்கு பெயர் பெற்றது, இதில் மிக உயரமான தெற்கு கோபுரம் 170 அடி உயரத்தை எட்டுகிறது. இது தமிழ்நாட்டின் மிகப்பெரிய கோவில் வளாகங்களில் ஒன்றாகும்."
        },
        "best_time_to_visit": "October to March",
        "significance": "UNESCO World Heritage Site",
        "architectural_style": "Dravidian architecture"
    },
    
    "Brihadeeswarar Temple": {
        "location": "Thanjavur",
        "description": {
            "English": "Also known as the Big Temple, it is a UNESCO World Heritage Site built by Rajaraja Chola I in 1010 CE. The temple features the world's first complete granite temple and has the tallest vimana (temple tower) in the world. The Nandi (bull) statue at the entrance is carved from a single stone and is one of the largest in India.",
            "Tamil": "பெரிய கோவில் என்றும் அழைக்கப்படும் இது, 1010 CE இல் ராஜராஜ சோழன் I ஆல் கட்டப்பட்ட ஒரு யுனெஸ்கோ உலக பாரம்பரிய தளமாகும். இக்கோவில் உலகின் முதல் முழு கிரானைட் கோவிலாகும் மற்றும் உலகின் மிக உயரமான விமானம் (கோவில் கோபுரம்) கொண்டது. நுழைவாயிலில் உள்ள நந்தி சிலை ஒரே கல்லில் செதுக்கப்பட்டது மற்றும் இந்தியாவின் மிகப்பெரிய சிலைகளில் ஒன்றாகும்."
        },
        "best_time_to_visit": "November to February",
        "significance": "UNESCO World Heritage Site, Great Living Chola Temple",
        "architectural_style": "Chola architecture"
    },
    
    "Mahabalipuram Shore Temple": {
        "location": "Mahabalipuram",
        "description": {
            "English": "Built during the reign of the Pallava dynasty in the 8th century CE, this structural temple overlooking the Bay of Bengal is one of the oldest structural stone temples in South India. It is a UNESCO World Heritage Site known for its intricate rock-cut architecture and beautiful sculptures.",
            "Tamil": "8ஆம் நூற்றாண்டில் பல்லவர் ஆட்சிக் காலத்தில் கட்டப்பட்ட இந்த கட்டமைப்புக் கோவில் வங்காள விரிகுடாவை எதிர்கொண்டுள்ளது மற்றும் தென்னிந்தியாவின் பழமையான கட்டமைப்பு கல் கோவில்களில் ஒன்றாகும். இது அதன் சிக்கலான பாறை வெட்டு கட்டிடக்கலை மற்றும் அழகிய சிற்பங்களுக்கு பெயர் பெற்ற யுனெஸ்கோ உலக பாரம்பரிய தளமாகும்."
        },
        "best_time_to_visit": "October to March",
        "significance": "UNESCO World Heritage Site, Group of Monuments at Mahabalipuram",
        "architectural_style": "Pallava architecture"
    },
    
    "Chettinadu Mansions": {
        "location": "Chettinad region (Karaikudi)",
        "description": {
            "English": "Chettinad mansions are known for their grand architecture, spacious courtyards, and use of exotic materials like Burmese teak, Italian marble, and Belgian glass. These palatial homes were built by the prosperous Chettiar community in the 19th century who were traders and bankers.",
            "Tamil": "செட்டிநாடு மாளிகைகள் அவற்றின் கம்பீரமான கட்டிடக்கலை, விசாலமான முற்றங்கள் மற்றும் பர்மிய தேக்கு, இத்தாலிய பளிங்கு மற்றும் பெல்ஜிய கண்ணாடி போன்ற வெளிநாட்டு பொருட்களின் பயன்பாட்டிற்கு பெயர் பெற்றவை. இந்த அரண்மனை போன்ற வீடுகள் 19ஆம் நூற்றாண்டில் வணிகர்களும் வங்கியாளர்களுமான செட்டியார் சமூகத்தால் கட்டப்பட்டன."
        },
        "best_time_to_visit": "November to February",
        "significance": "Cultural Heritage, Unique Architecture",
        "architectural_style": "Chettinad architecture"
    },
    
    "Gangaikonda Cholapuram": {
        "location": "Jayankondam",
        "description": {
            "English": "Built by Rajendra Chola I to commemorate his victory over the Gangetic plains, this temple is now a UNESCO World Heritage Site. The temple is notable for its massive size, intricate sculptures, and the magnificent 185-foot vimana.",
            "Tamil": "கங்கை சமவெளியில் தனது வெற்றியை நினைவுகூர ராஜேந்திர சோழன் I ஆல் கட்டப்பட்ட இக்கோவில் இப்போது ஒரு யுனெஸ்கோ உலக பாரம்பரிய தளமாகும். இக்கோவில் அதன் பாரிய அளவு, சிக்கலான சிற்பங்கள் மற்றும் அற்புதமான 185 அடி விமானத்திற்கு குறிப்பிடத்தக்கது."
        },
        "best_time_to_visit": "October to March",
        "significance": "UNESCO World Heritage Site",
        "architectural_style": "Chola architecture"
    }
}

# Tourism information
tourism_info = {
    "transportation": {
        "English": "Tamil Nadu has excellent connectivity via air, rail, and road. Major cities have airports, and the railway network connects all heritage sites. Local transport includes buses, taxis, and auto-rickshaws.",
        "Tamil": "தமிழ்நாடு விமானம், ரயில் மற்றும் சாலை வழியாக சிறந்த இணைப்பைக் கொண்டுள்ளது. பெருநகரங்களில் விமான நிலையங்கள் உள்ளன, மற்றும் ரயில் பிணையம் அனைத்து பாரம்பரிய தளங்களையும் இணைக்கிறது. உள்ளூர் போக்குவரத்தில் பேருந்துகள், வாடகை கார்கள் மற்றும் ஆட்டோ ரிக்ஷாக்கள் அடங்கும்."
    },
    "accommodation": {
        "English": "Tamil Nadu offers a range of accommodations from budget hotels to luxury heritage properties. Most heritage sites have good hotels and resorts nearby.",
        "Tamil": "தமிழ்நாடு பட்ஜெட் ஹோட்டல்கள் முதல் ஆடம்பர பாரம்பரிய பண்பாடுகள் வரை பல்வேறு வகையான தங்குமிடங்களை வழங்குகிறது. பெரும்பாலான பாரம்பரிய தளங்களுக்கு அருகிலேயே நல்ல ஹோட்டல்கள் மற்றும் ரிசார்ட்டுகள் உள்ளன."
    },
    "cuisine": {
        "English": "Don't miss Tamil Nadu's famous cuisine including dosa, idli, sambar, Chettinad chicken, filter coffee, and traditional vegetarian meals served on banana leaves.",
        "Tamil": "தோசை, இட்லி, சாம்பார், செட்டிநாடு சிக்கன், பில்டர் காபி மற்றும் வாழை இலைகளில் வழங்கப்படும் பாரம்பரிய சைவ உணவுகள் உட்பட தமிழ்நாட்டின் பிரபலமான உணவுகளை கண்டிப்பாக சுவையுங்கள்."
    }
}

class TamilNaduTouristBot:
    def __init__(self):
        self.current_language = "English"
        self.audio_enabled = True
        self.user_name = ""
        
    def text_to_speech(self, text, language="en"):
        """Convert text to speech and play it"""
        if not self.audio_enabled:
            return
            
        try:
            # Map languages to gTTS language codes
            lang_codes = {
                "English": "en",
                "Tamil": "ta"
            }
            lang_code = lang_codes.get(language, "en")
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"heritage_info_{timestamp}.mp3"
            
            # Create gTTS object and save
            tts = gTTS(text=text, lang=lang_code, slow=False)
            tts.save(filename)
            
            # Play the audio
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            
            # Wait for audio to finish playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            # Clean up
            pygame.mixer.music.unload()
            time.sleep(0.1)
            
            # Delete the file after playing (optional)
            # os.remove(filename)
            
        except Exception as e:
            print(f"Audio error: {e}. Continuing with text display...")
    
    def display_heritage_info(self, heritage_name, language="English"):
        """Display information about a heritage site"""
        if heritage_name not in heritage_spots:
            print(f"{language}: Heritage site not found.")
            return
        
        site = heritage_spots[heritage_name]
        print("\n" + "="*60)
        print(f"{heritage_name} - {site['location']}")
        print("="*60)
        
        # Display in chosen language
        description = site['description'][language]
        print(f"\n📜 {language} Description:")
        print(f"{description}\n")
        
        # Additional information
        print(f"📍 Location: {site['location']}")
        print(f"📅 Best time to visit: {site['best_time_to_visit']}")
        print(f"⭐ Significance: {site['significance']}")
        print(f"🏛️ Architectural Style: {site['architectural_style']}")
        
        # Play audio
        if self.audio_enabled:
            audio_text = f"{heritage_name}. {description}"
            self.text_to_speech(audio_text, language)
    
    def display_tourism_info(self, category, language="English"):
        """Display tourism information"""
        if category not in tourism_info:
            print(f"{language}: Category not found.")
            return
        
        info = tourism_info[category][language]
        print("\n" + "="*60)
        print(f"Tourism Information: {category} ({language})")
        print("="*60)
        print(f"\n{info}")
        
        if self.audio_enabled:
            self.text_to_speech(info, language)
    
    def list_heritage_sites(self, language="English"):
        """List all available heritage sites"""
        print("\n" + "="*60)
        print(f"🎯 Heritage Sites of Tamil Nadu ({language})")
        print("="*60)
        
        for i, site in enumerate(heritage_spots.keys(), 1):
            location = heritage_spots[site]['location']
            print(f"{i}. {site} - {location}")
    
    def welcome_message(self):
        """Display welcome message"""
        print("\n" + "="*60)
        print("🎉 WELCOME TO TAMIL NADU HERITAGE TOURIST BOT 🎉")
        print("="*60)
        print("\nDiscover the rich cultural heritage of Tamil Nadu!")
        print("Explore magnificent temples, palaces, and historical sites.")
        print("\nAvailable languages: English / தமிழ்")
        print("="*60)
    
    def get_language_choice(self):
        """Get language choice from user"""
        print("\n🌍 Choose your language:")
        print("1. English")
        print("2. தமிழ் (Tamil)")
        
        while True:
            choice = input("\nEnter choice (1 or 2): ").strip()
            if choice == "1":
                return "English"
            elif choice == "2":
                return "Tamil"
            else:
                print("Invalid choice. Please enter 1 or 2.")
    
    def get_user_name(self):
        """Get user's name"""
        name = input("\nWhat's your name? ").strip()
        return name if name else "Guest"
    
    def main_menu(self):
        """Display main menu"""
        print(f"\n👋 Welcome, {self.user_name}!")
        print("\n" + "="*60)
        print(f"MAIN MENU ({self.current_language})")
        print("="*60)
        print("\n1. 🏛️ Explore Heritage Sites")
        print("2. ℹ️ Tourism Information")
        print("3. 🌐 Change Language")
        print("4. 🔊 Toggle Audio (Currently: " + ("ON" if self.audio_enabled else "OFF") + ")")
        print("5. 📋 List All Heritage Sites")
        print("6. ❌ Exit")
        print("="*60)
    
    def heritage_sites_menu(self):
        """Display heritage sites menu"""
        print("\n" + "="*60)
        print("🏛️ HERITAGE SITES MENU")
        print("="*60)
        
        sites = list(heritage_spots.keys())
        for i, site in enumerate(sites, 1):
            print(f"{i}. {site}")
        
        print(f"{len(sites) + 1}. 🔙 Back to Main Menu")
        
        return sites
    
    def tourism_info_menu(self):
        """Display tourism information menu"""
        print("\n" + "="*60)
        print("ℹ️ TOURISM INFORMATION")
        print("="*60)
        print("\n1. 🚌 Transportation")
        print("2. 🏨 Accommodation")
        print("3. 🍽️ Cuisine")
        print("4. 🔙 Back to Main Menu")
    
    def run(self):
        """Main function to run the tourist bot"""
        self.welcome_message()
        self.user_name = self.get_user_name()
        self.current_language = self.get_language_choice()
        
        while True:
            self.main_menu()
            choice = input(f"\n{self.user_name}, enter your choice (1-6): ").strip()
            
            if choice == "1":  # Explore Heritage Sites
                sites = self.heritage_sites_menu()
                site_choice = input("\nSelect a heritage site (number): ").strip()
                
                if site_choice.isdigit():
                    site_index = int(site_choice) - 1
                    if 0 <= site_index < len(sites):
                        self.display_heritage_info(sites[site_index], self.current_language)
                    elif site_index == len(sites):
                        continue  # Back to main menu
                    else:
                        print("Invalid choice. Please try again.")
                else:
                    print("Please enter a valid number.")
            
            elif choice == "2":  # Tourism Information
                self.tourism_info_menu()
                info_choice = input("\nSelect category (1-4): ").strip()
                
                categories = ["transportation", "accommodation", "cuisine"]
                if info_choice.isdigit():
                    info_index = int(info_choice) - 1
                    if 0 <= info_index < len(categories):
                        self.display_tourism_info(categories[info_index], self.current_language)
                    elif info_index == 3:
                        continue  # Back to main menu
                    else:
                        print("Invalid choice. Please try again.")
                else:
                    print("Please enter a valid number.")
            
            elif choice == "3":  # Change Language
                print("\n🌍 Change Language:")
                print(f"Current language: {self.current_language}")
                self.current_language = self.get_language_choice()
                print(f"✅ Language changed to {self.current_language}")
            
            elif choice == "4":  # Toggle Audio
                self.audio_enabled = not self.audio_enabled
                status = "ON" if self.audio_enabled else "OFF"
                print(f"\n🔊 Audio is now {status}")
                
                # Announce in both languages
                if self.audio_enabled:
                    announcement = f"Audio is now enabled. Welcome to Tamil Nadu heritage tour."
                else:
                    announcement = f"Audio is now disabled."
                
                self.text_to_speech(announcement, self.current_language)
            
            elif choice == "5":  # List All Heritage Sites
                self.list_heritage_sites(self.current_language)
                
                # Ask if user wants details
                view_details = input("\nWould you like to view details of any site? (yes/no): ").strip().lower()
                if view_details == 'yes':
                    site_name = input("Enter the name of the heritage site: ").strip()
                    if site_name in heritage_spots:
                        self.display_heritage_info(site_name, self.current_language)
                    else:
                        print("Site not found. Please check the name and try again.")
            
            elif choice == "6":  # Exit
                farewell_message = f"Thank you for exploring Tamil Nadu's heritage with us, {self.user_name}! Have a wonderful journey! வணக்கம்!"
                print(f"\n{farewell_message}")
                
                if self.audio_enabled:
                    self.text_to_speech(farewell_message, self.current_language)
                
                # Wait for audio to finish before exiting
                time.sleep(2)
                break
            
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
            
            # Pause before showing menu again
            input("\nPress Enter to continue...")

# Run the bot
if __name__ == "__main__":
    try:
        bot = TamilNaduTouristBot()
        bot.run()
    except KeyboardInterrupt:
        print("\n\n👋 Thank you for using Tamil Nadu Heritage Tourist Bot!")
    except Exception as e:
        print(f"\n⚠️ An error occurred: {e}")
        print("Please try again later.")
