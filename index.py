from gtts import gTTS
import os
import openai

# Initialize OpenAI API
openai.api_key = 'your-openai-api-key'  # Replace with your actual OpenAI API key

# Heritage site database (updated with new places and languages)
heritage_sites = {
    "Airavatesvara Temple": {
        "location": "Darasuram, Tamil Nadu",
        "languages": {
            "English": "The Airavatesvara Temple in Darasuram, Tamil Nadu, is a UNESCO World Heritage Site and a masterpiece of Chola architecture. Built by King Rajaraja Chola II in the 12th century, the temple is dedicated to Lord Shiva. It is renowned for its intricate stone carvings, musical pillars, and the legend of Airavata, the white elephant of Indra, who worshipped here. The temple's architecture reflects the zenith of Chola art and culture.",
            "Tamil": "தாராசுரத்தில் உள்ள ஐராவதேஸ்வரர் கோயில் ஒரு யுனெஸ்கோ உலக பாரம்பரிய தளம் மற்றும் சோழர்களின் கட்டிடக்கலையின் ஒரு மாஸ்டர்பீஸ். 12 ஆம் நூற்றாண்டில் ராஜராஜ சோழன் II ஆல் கட்டப்பட்ட இந்த கோயில் சிவபெருமானுக்கு அர்ப்பணிக்கப்பட்டது. இது அதன் சிக்கலான கல் செதுக்குதல்கள், இசைத்தூண்கள் மற்றும் இந்திரனின் வெள்ளை யானை ஐராவதத்தின் புராணக்கதைக்கு பெயர் பெற்றது. இந்த கோயிலின் கட்டிடக்கலை சோழர்களின் கலை மற்றும் கலாச்சாரத்தின் உச்சத்தை பிரதிபலிக்கிறது.",
            "Hindi": "तमिलनाडु के दारासुरम में स्थित ऐरावतेश्वर मंदिर एक यूनेस्को विश्व धरोहर स्थल है और चोल वास्तुकला का एक उत्कृष्ट नमूना है। 12वीं शताब्दी में राजराज चोल द्वितीय द्वारा निर्मित, यह मंदिर भगवान शिव को समर्पित है। यह अपनी जटिल पत्थर की नक्काशी, संगीतमय स्तंभों और इंद्र के सफेद हाथी ऐरावत की कथा के लिए प्रसिद्ध है। मंदिर की वास्तुकला चोल कला और संस्कृति के शिखर को दर्शाती है।",
            "French": "Le temple Airavatesvara à Darasuram, Tamil Nadu, est un site du patrimoine mondial de l'UNESCO et un chef-d'œuvre de l'architecture Chola. Construit par le roi Rajaraja Chola II au XIIe siècle, le temple est dédié à Lord Shiva. Il est renommé pour ses sculptures en pierre complexes, ses piliers musicaux et la légende d'Airavata, l'éléphant blanc d'Indra, qui y a adoré. L'architecture du temple reflète l'apogée de l'art et de la culture Chola.",
            "Spanish": "El templo Airavatesvara en Darasuram, Tamil Nadu, es un sitio del Patrimonio Mundial de la UNESCO y una obra maestra de la arquitectura Chola. Construido por el rey Rajaraja Chola II en el siglo XII, el templo está dedicado al Señor Shiva. Es famoso por sus intrincadas tallas en piedra, sus pilares musicales y la leyenda de Airavata, el elefante blanco de Indra, que adoró aquí. La arquitectura del templo refleja la cúspide del arte y la cultura Chola.",
            "German": "Der Airavatesvara-Tempel in Darasuram, Tamil Nadu, ist ein UNESCO-Weltkulturerbe und ein Meisterwerk der Chola-Architektur. Der im 12. Jahrhundert von König Rajaraja Chola II. erbaute Tempel ist Lord Shiva gewidmet. Er ist berühmt für seine kunstvollen Steinschnitzereien, musikalischen Säulen und die Legende von Airavata, dem weißen Elefanten von Indra, der hier verehrt wurde. Die Architektur des Tempels spiegelt den Höhepunkt der Chola-Kunst und -Kultur wider."
        },
        "spoken_languages": ["Tamil", "English", "Hindi"]
    },
    "Brihadeeswara Temple": {
        "location": "Thanjavur, Tamil Nadu",
        "languages": {
            "English": "The Brihadeeswara Temple in Thanjavur, Tamil Nadu, is a UNESCO World Heritage Site and one of the greatest architectural achievements of the Chola dynasty. Built by King Rajaraja Chola I in the 11th century, the temple is dedicated to Lord Shiva. It is famous for its towering vimana (temple tower), which stands at 66 meters, and its massive Nandi (bull) statue. The temple's intricate carvings and frescoes depict scenes from Hindu mythology and showcase the grandeur of Chola art.",
            "Tamil": "தஞ்சாவூரில் உள்ள பிரகதீஸ்வரர் கோயில் ஒரு யுனெஸ்கோ உலக பாரம்பரிய தளம் மற்றும் சோழர்களின் மிகப்பெரிய கட்டிடக்கலை சாதனைகளில் ஒன்று. 11 ஆம் நூற்றாண்டில் ராஜராஜ சோழன் I ஆல் கட்டப்பட்ட இந்த கோயில் சிவபெருமானுக்கு அர்ப்பணிக்கப்பட்டது. இது அதன் 66 மீட்டர் உயரமுள்ள விமானம் (கோபுரம்) மற்றும் பிரம்மாண்டமான நந்தி (காளை) சிலைக்கு பெயர் பெற்றது. கோயிலின் சிக்கலான செதுக்குதல்கள் மற்றும் சுவரோவியங்கள் இந்து புராணக்கதைகளின் காட்சிகளை சித்தரிக்கின்றன மற்றும் சோழர்களின் கலையின் பிரம்மாண்டத்தை காட்டுகின்றன.",
            "Hindi": "तमिलनाडु के तंजावुर में स्थित बृहदीश्वर मंदिर एक यूनेस्को विश्व धरोहर स्थल है और चोल वंश की सबसे बड़ी वास्तुकला उपलब्धियों में से एक है। 11वीं शताब्दी में राजराज चोल प्रथम द्वारा निर्मित, यह मंदिर भगवान शिव को समर्पित है। यह अपने 66 मीटर ऊंचे विमान (मंदिर टॉवर) और विशाल नंदी (बैल) मूर्ति के लिए प्रसिद्ध है। मंदिर की जटिल नक्काशी और भित्तिचित्र हिंदू पौराणिक कथाओं के दृश्यों को दर्शाते हैं और चोल कला की भव्यता को प्रदर्शित करते हैं।",
            "French": "Le temple Brihadeeswara à Thanjavur, Tamil Nadu, est un site du patrimoine mondial de l'UNESCO et l'une des plus grandes réalisations architecturales de la dynastie Chola. Construit par le roi Rajaraja Chola Ier au XIe siècle, le temple est dédié à Lord Shiva. Il est célèbre pour son vimana (tour du temple) imposant de 66 mètres de haut et sa statue massive de Nandi (taureau). Les sculptures complexes et les fresques du temple dépeignent des scènes de la mythologie hindoue et illustrent la grandeur de l'art Chola.",
            "Spanish": "El templo Brihadeeswara en Thanjavur, Tamil Nadu, es un sitio del Patrimonio Mundial de la UNESCO y uno de los mayores logros arquitectónicos de la dinastía Chola. Construido por el rey Rajaraja Chola I en el siglo XI, el templo está dedicado al Señor Shiva. Es famoso por su imponente vimana (torre del templo) de 66 metros de altura y su enorme estatua de Nandi (toro). Las intrincadas tallas y frescos del templo representan escenas de la mitología hindú y muestran la grandeza del arte Chola.",
            "German": "Der Brihadeeswara-Tempel in Thanjavur, Tamil Nadu, ist ein UNESCO-Weltkulturerbe und eine der größten architektonischen Errungenschaften der Chola-Dynastie. Der im 11. Jahrhundert von König Rajaraja Chola I. erbaute Tempel ist Lord Shiva gewidmet. Er ist berühmt für seinen 66 Meter hohen Vimana (Tempelturm) und seine massive Nandi (Stier)-Statue. Die kunstvollen Schnitzereien und Fresken des Tempels zeigen Szenen aus der hinduistischen Mythologie und demonstrieren die Pracht der Chola-Kunst."
        },
        "spoken_languages": ["Tamil", "English", "Hindi"]
    },
    "Gangaikonda Cholapuram": {
        "location": "Tamil Nadu",
        "languages": {
            "English": "Gangaikonda Cholapuram, located in Tamil Nadu, was the capital of the Chola dynasty under King Rajendra Chola I. The city is home to the Brihadeeswara Temple, a UNESCO World Heritage Site, which is a smaller yet equally magnificent version of the Thanjavur temple. The temple is renowned for its intricate carvings, massive lingam, and the grandeur of Chola architecture. It stands as a testament to the power and cultural achievements of the Chola Empire.",
            "Tamil": "தமிழ்நாட்டில் அமைந்துள்ள கங்கைகொண்ட சோழபுரம், ராஜேந்திர சோழன் I இன் கீழ் சோழ வம்சத்தின் தலைநகராக இருந்தது. இந்த நகரம் ஒரு யுனெஸ்கோ உலக பாரம்பரிய தளமான பிரகதீஸ்வரர் கோயிலுக்கு பெயர் பெற்றது, இது தஞ்சாவூர் கோயிலின் சிறிய ஆனால் சமமான பிரம்மாண்டமான பதிப்பாகும். இந்த கோயில் அதன் சிக்கலான செதுக்குதல்கள், பிரம்மாண்டமான லிங்கம் மற்றும் சோழர்களின் கட்டிடக்கலையின் பிரம்மாண்டத்திற்கு பெயர் பெற்றது. இது சோழப் பேரரசின் சக்தி மற்றும் கலாச்சார சாதனைகளுக்கு ஒரு சான்றாக நிற்கிறது.",
            "Hindi": "तमिलनाडु में स्थित गंगैकोण्ड चोलपुरम, राजेंद्र चोल प्रथम के शासनकाल में चोल वंश की राजधानी थी। यह शहर बृहदीश्वर मंदिर का घर है, जो एक यूनेस्को विश्व धरोहर स्थल है और तंजावुर मंदिर का एक छोटा लेकिन समान रूप से शानदार संस्करण है। यह मंदिर अपनी जटिल नक्काशी, विशाल लिंगम और चोल वास्तुकला की भव्यता के लिए प्रसिद्ध है। यह चोल साम्राज्य की शक्ति और सांस्कृतिक उपलब्धियों का प्रमाण है।",
            "French": "Gangaikonda Cholapuram, situé dans le Tamil Nadu, était la capitale de la dynastie Chola sous le règne du roi Rajendra Chola I. La ville abrite le temple Brihadeeswara, un site du patrimoine mondial de l'UNESCO, qui est une version plus petite mais tout aussi magnifique du temple de Thanjavur. Le temple est renommé pour ses sculptures complexes, son lingam massif et la grandeur de l'architecture Chola. Il témoigne de la puissance et des réalisations culturelles de l'Empire Chola.",
            "Spanish": "Gangaikonda Cholapuram, ubicado en Tamil Nadu, fue la capital de la dinastía Chola bajo el rey Rajendra Chola I. La ciudad alberga el templo Brihadeeswara, un sitio del Patrimonio Mundial de la UNESCO, que es una versión más pequeña pero igualmente magnífica del templo de Thanjavur. El templo es famoso por sus intrincados tallados, su enorme lingam y la grandeza de la arquitectura Chola. Es un testimonio del poder y los logros culturales del Imperio Chola.",
            "German": "Gangaikonda Cholapuram, im Bundesstaat Tamil Nadu gelegen, war die Hauptstadt der Chola-Dynastie unter König Rajendra Chola I. Die Stadt beherbergt den Brihadeeswara-Tempel, ein UNESCO-Weltkulturerbe, das eine kleinere, aber ebenso prächtige Version des Thanjavur-Tempels ist. Der Tempel ist berühmt für seine kunstvollen Schnitzereien, seinen massiven Lingam und die Pracht der Chola-Architektur. Er steht als Zeugnis der Macht und kulturellen Errungenschaften des Chola-Reiches."
        },
        "spoken_languages": ["Tamil", "English", "Hindi"]
    },
    "Group of Monuments at Mahabalipuram": {
        "location": "Mahabalipuram, Tamil Nadu",
        "languages": {
            "English": "The Group of Monuments at Mahabalipuram, Tamil Nadu, is a UNESCO World Heritage Site and a testament to the architectural brilliance of the Pallava dynasty. These 7th and 8th-century monuments include rock-cut temples, cave sanctuaries, and the famous Shore Temple. The site is renowned for its intricate carvings, including the iconic 'Descent of the Ganges' relief. Mahabalipuram was a bustling port city during the Pallava era and remains a symbol of India's rich cultural heritage.",
            "Tamil": "மகாபலிபுரத்தில் உள்ள நினைவுச்சின்னங்களின் குழு ஒரு யுனெஸ்கோ உலக பாரம்பரிய தளம் மற்றும் பல்லவர்களின் கட்டிடக்கலை பிரகாசத்திற்கு ஒரு சான்று. இந்த 7 மற்றும் 8 ஆம் நூற்றாண்டு நினைவுச்சின்னங்களில் பாறை வெட்டு கோயில்கள், குகை சரணாலயங்கள் மற்றும் பிரபலமான கடற்கரை கோயில் ஆகியவை அடங்கும். இந்த தளம் அதன் சிக்கலான செதுக்குதல்களுக்கு பெயர் பெற்றது, இதில் 'கங்கையின் இறக்கம்' எனும் பிரபலமான சிற்பம் அடங்கும். பல்லவர்களின் காலத்தில் மகாபலிபுரம் ஒரு பரபரப்பான துறைமுக நகரமாக இருந்தது மற்றும் இந்தியாவின் பணக்கார கலாச்சார பாரம்பரியத்தின் அடையாளமாக உள்ளது.",
            "Hindi": "तमिलनाडु के महाबलीपुरम में स्थित स्मारकों का समूह एक यूनेस्को विश्व धरोहर स्थल है और पल्लव वंश की वास्तुकला की प्रतिभा का प्रमाण है। ये 7वीं और 8वीं शताब्दी के स्मारकों में चट्टानों को काटकर बनाए गए मंदिर, गुफा मंदिर और प्रसिद्ध शोर टेम्पल शामिल हैं। यह स्थल अपनी जटिल नक्काशी के लिए प्रसिद्ध है, जिसमें प्रतिष्ठित 'गंगा अवतरण' राहत भी शामिल है। पल्लव युग में महाबलीपुरम एक व्यस्त बंदरगाह शहर था और यह भारत की समृद्ध सांस्कृतिक विरासत का प्रतीक है।",
            "French": "Le groupe de monuments de Mahabalipuram, Tamil Nadu, est un site du patrimoine mondial de l'UNESCO et un témoignage de la brillance architecturale de la dynastie Pallava. Ces monuments des VIIe et VIIIe siècles comprennent des temples taillés dans la roche, des sanctuaires troglodytes et le célèbre temple du Rivage. Le site est renommé pour ses sculptures complexes, y compris le célèbre relief 'Descente du Gange'. Mahabalipuram était une ville portuaire animée à l'époque Pallava et reste un symbole du riche patrimoine culturel de l'Inde.",
            "Spanish": "El grupo de monumentos de Mahabalipuram, Tamil Nadu, es un sitio del Patrimonio Mundial de la UNESCO y un testimonio del brillo arquitectónico de la dinastía Pallava. Estos monumentos de los siglos VII y VIII incluyen templos tallados en roca, santuarios en cuevas y el famoso Templo de la Orilla. El sitio es famoso por sus intrincados tallados, incluido el icónico relieve 'Descenso del Ganges'. Mahabalipuram fue una bulliciosa ciudad portuaria durante la era Pallava y sigue siendo un símbolo del rico patrimonio cultural de la India.",
            "German": "Die Gruppe von Denkmälern in Mahabalipuram, Tamil Nadu, ist ein UNESCO-Weltkulturerbe und ein Zeugnis der architektonischen Brillanz der Pallava-Dynastie. Diese Denkmäler aus dem 7. und 8. Jahrhundert umfassen in den Fels gehauene Tempel, Höhlenheiligtümer und den berühmten Ufertempel. Die Stätte ist berühmt für ihre kunstvollen Schnitzereien, darunter das ikonische Relief 'Gangestau'. Mahabalipuram war während der Pallava-Ära eine geschäftige Hafenstadt und bleibt ein Symbol für das reiche kulturelle Erbe Indiens."
        },
        "spoken_languages": ["Tamil", "English", "Hindi"]
    },
    "Meenakshi Amman Temple": {
        "location": "Madurai, Tamil Nadu",
        "languages": {
            "English": "The Meenakshi Amman Temple in Madurai, Tamil Nadu, is one of the most iconic temples in India and a masterpiece of Dravidian architecture. Dedicated to Goddess Meenakshi (an incarnation of Parvati) and Lord Sundareswarar (Shiva), the temple is renowned for its towering gopurams (gateway towers), intricate carvings, and vibrant festivals. The temple complex spans 14 acres and features 14 gopurams, the tallest of which is 52 meters high. It is a symbol of Tamil culture and spirituality.",
            "Tamil": "மதுரையில் உள்ள மீனாட்சி அம்மன் கோயில் இந்தியாவின் மிகவும் அடையாளமான கோயில்களில் ஒன்றாகும் மற்றும் திராவிட கட்டிடக்கலையின் ஒரு மாஸ்டர்பீஸ். தெய்வீக மீனாட்சி (பார்வதியின் அவதாரம்) மற்றும் சுந்தரேஸ்வரர் (சிவன்) ஆகியோருக்கு அர்ப்பணிக்கப்பட்ட இந்த கோயில் அதன் உயரமான கோபுரங்கள் (நுழைவாயில் கோபுரங்கள்), சிக்கலான செதுக்குதல்கள் மற்றும் உற்சாகமான திருவிழாக்களுக்கு பெயர் பெற்றது. கோயில் வளாகம் 14 ஏக்கர் பரப்பளவில் உள்ளது மற்றும் 14 கோபுரங்களைக் கொண்டுள்ளது, இதில் மிக உயரமானது 52 மீட்டர் உயரமானது. இது தமிழ் கலாச்சாரம் மற்றும் ஆன்மீகத்தின் அடையாளமாகும்.",
            "Hindi": "तमिलना�ाडु के मदुरै में स्थित मीनाक्षी अम्मन मंदिर भारत के सबसे प्रतिष्ठित मंदिरों में से एक है और द्रविड़ वास्तुकला का एक उत्कृष्ट नमूना है। देवी मीनाक्षी (पार्वती का अवतार) और भगवान सुंदरेश्वर (शिव) को समर्पित, यह मंदिर अपने ऊंचे गोपुरम (प्रवेश द्वार टावर), जटिल नक्काशी और जीवंत त्योहारों के लिए प्रसिद्ध है। मंदिर परिसर 14 एकड़ में फैला है और इसमें 14 गोपुरम हैं, जिनमें सबसे ऊंचा 52 मीटर ऊंचा है। यह तमिल संस्कृति और आध्यात्मिकता का प्रतीक है।",
            "French": "Le temple de Meenakshi Amman à Madurai, Tamil Nadu, est l'un des temples les plus emblématiques de l'Inde et un chef-d'œuvre de l'architecture dravidienne. Dédié à la déesse Meenakshi (une incarnation de Parvati) et au seigneur Sundareswarar (Shiva), le temple est renommé pour ses gopurams (tours d'entrée) imposants, ses sculptures complexes et ses festivals vibrants. Le complexe du temple s'étend sur 14 acres et compte 14 gopurams, dont le plus haut mesure 52 mètres. C'est un symbole de la culture et de la spiritualité tamoules.",
            "Spanish": "El templo de Meenakshi Amman en Madurai, Tamil Nadu, es uno de los templos más icónicos de la India y una obra maestra de la arquitectura dravidiana. Dedicado a la diosa Meenakshi (una encarnación de Parvati) y al señor Sundareswarar (Shiva), el templo es famoso por sus imponentes gopurams (torres de entrada), intrincados tallados y vibrantes festivales. El complejo del templo abarca 14 acres y cuenta con 14 gopurams, el más alto de los cuales mide 52 metros. Es un símbolo de la cultura y espiritualidad tamil.",
            "German": "Der Meenakshi Amman-Tempel in Madurai, Tamil Nadu, ist einer der ikonischsten Tempel Indiens und ein Meisterwerk der dravidischen Architektur. Der Tempel, der der Göttin Meenakshi (einer Inkarnation von Parvati) und Lord Sundareswarar (Shiva) gewidmet ist, ist berühmt für seine imposanten Gopurams (Eingangstürme), kunstvollen Schnitzereien und lebendigen Feste. Der Tempelkomplex erstreckt sich über 14 Hektar und verfügt über 14 Gopurams, von denen der höchste 52 Meter hoch ist. Er ist ein Symbol der tamilischen Kultur und Spiritualität."
        },
        "spoken_languages": ["Tamil", "English", "Hindi"]
    },
    "Nilgiri Mountain Railway Line": {
        "location": "Tamil Nadu",
        "languages": {
            "English": "The Nilgiri Mountain Railway Line, a UNESCO World Heritage Site, is a historic railway in Tamil Nadu that connects Mettupalayam to Ooty. Built in the early 20th century, this scenic railway is known for its steam locomotives and breathtaking views of the Nilgiri Hills. The railway features a unique rack-and-pinion system to navigate steep gradients and is one of the few mountain railways in the world still in operation. It offers a nostalgic journey through lush forests, tea plantations, and misty mountains.",
            "Tamil": "நீலகிரி மலை ரயில் பாதை ஒரு யுனெஸ்கோ உலக பாரம்பரிய தளம் மற்றும் தமிழ்நாட்டில் மேட்டுப்பாளையத்தை உதகமண்டலத்துடன் இணைக்கும் ஒரு வரலாற்று ரயில் பாதை. 20 ஆம் நூற்றாண்டின் ஆரம்பத்தில் கட்டப்பட்ட இந்த அழகிய ரயில் அதன் நீராவி எஞ்சின்கள் மற்றும் நீலகிரி மலைகளின் அற்புதமான காட்சிகளுக்கு பெயர் பெற்றது. இந்த ரயில் பாதை செங்குத்தான சரிவுகளை சமாளிக்க ஒரு தனித்துவமான ரேக்-மற்றும்-பினியன் அமைப்பை கொண்டுள்ளது மற்றும் உலகில் இன்னும் செயல்பாட்டில் உள்ள சில மலை ரயில் பாதைகளில் ஒன்றாகும். இது பசுமையான காடுகள், தேயிலை தோட்டங்கள் மற்றும் மூடுபனி மலைகள் வழியாக ஒரு நாஸ்டால்ஜிக் பயணத்தை வழங்குகிறது.",
            "Hindi": "नीलगिरि माउंटेन रेलवे लाइन, एक यूनेस्को विश्व धरोहर स्थल, तमिलनाडु में एक ऐतिहासिक रेलवे है जो मेट्टुपालयम को ऊटी से जोड़ती है। 20वीं शताब्दी की शुरुआत में निर्मित, यह सुंदर रेलवे अपने स्टीम लोकोमोटिव और नीलगिरि पहाड़ियों के लुभावने दृश्यों के लिए प्रसिद्ध है। रेलवे में खड़ी ढलानों को नेविगेट करने के लिए एक अद्वितीय रैक-एंड-पिनियन प्रणाली है और यह दुनिया की कुछ परिचालन में लगी पर्वतीय रेलवे में से एक है। यह हरे-भरे जंगलों, चाय बागानों और धुंधली पहाड़ियों के बीच एक नॉस्टैल्जिक यात्रा प्रदान करता है।",
            "French": "La ligne de chemin de fer de montagne Nilgiri, un site du patrimoine mondial de l'UNESCO, est un chemin de fer historique du Tamil Nadu qui relie Mettupalayam à Ooty. Construite au début du XXe siècle, cette ligne pittoresque est connue pour ses locomotives à vapeur et ses vues imprenables sur les collines de Nilgiri. Le chemin de fer dispose d'un système unique de crémaillère pour naviguer sur des pentes raides et est l'un des rares chemins de fer de montagne encore en activité dans le monde. Il offre un voyage nostalgique à travers des forêts luxuriantes, des plantations de thé et des montagnes brumeuses.",
            "Spanish": "La línea ferroviaria de montaña Nilgiri, un sitio del Patrimonio Mundial de la UNESCO, es un ferrocarril histórico en Tamil Nadu que conecta Mettupalayam con Ooty. Construida a principios del siglo XX, esta pintoresca línea ferroviaria es conocida por sus locomotoras de vapor y sus impresionantes vistas de las colinas de Nilgiri. El ferrocarril cuenta con un sistema único de cremallera para navegar por pendientes pronunciadas y es uno de los pocos ferrocarriles de montaña que aún están en funcionamiento en el mundo. Ofrece un viaje nostálgico a través de frondosos bosques, plantaciones de té y montañas brumosas.",
            "German": "Die Nilgiri-Bergbahn, ein UNESCO-Weltkulturerbe, ist eine historische Eisenbahnlinie in Tamil Nadu, die Mettupalayam mit Ooty verbindet. Diese malerische Bahnstrecke, die Anfang des 20. Jahrhunderts erbaut wurde, ist bekannt für ihre Dampflokomotiven und den atemberaubenden Blick auf die Nilgiri-Berge. Die Bahn verfügt über ein einzigartiges Zahnradsystem, um steile Steigungen zu bewältigen, und ist eine der wenigen noch in Betrieb befindlichen Bergbahnen der Welt. Sie bietet eine nostalgische Reise durch üppige Wälder, Teeplantagen und nebelverhangene Berge."
        },
        "spoken_languages": ["Tamil", "English", "Hindi"]
    },
    "Shore Temple": {
        "location": "Mahabalipuram, Tamil Nadu",
        "languages": {
            "English": "The Shore Temple in Mahabalipuram, Tamil Nadu, is a UNESCO World Heritage Site and one of the oldest structural stone temples in South India. Built in the 8th century by the Pallava dynasty, the temple is dedicated to Lord Shiva and Lord Vishnu. It is renowned for its stunning location by the Bay of Bengal, intricate carvings, and Dravidian architectural style. The temple is a symbol of the Pallava dynasty's architectural prowess and maritime heritage.",
            "Tamil": "மகாபலிபுரத்தில் உள்ள கடற்கரை கோயில் ஒரு யுனெஸ்கோ உலக பாரம்பரிய தளம் மற்றும் தென்னிந்தியாவின் பழமையான கல் கட்டமைப்பு கோயில்களில் ஒன்றாகும். 8 ஆம் நூற்றாண்டில் பல்லவர்களால் கட்டப்பட்ட இந்த கோயில் சிவபெருமான் மற்றும் விஷ்ணுவுக்கு அர்ப்பணிக்கப்பட்டது. இது வங்காள விரிகுடாவின் அருகில் அதன் அற்புதமான இடம், சிக்கலான செதுக்குதல்கள் மற்றும் திராவிட கட்டிடக்கலை பாணிக்கு பெயர் பெற்றது. இந்த கோயில் பல்லவர்களின் கட்டிடக்கலை திறன் மற்றும் கடல் பாரம்பரியத்தின் அடையாளமாகும்.",
            "Hindi": "तमिलनाडु के महाबलीपुरम में स्थित शोर टेम्पल एक यूनेस्को विश्व धरोहर स्थल है और दक्षिण भारत के सबसे पुराने संरचनात्मक पत्थर मंदिरों में से एक है। 8वीं शताब्दी में पल्लव वंश द्वारा निर्मित, यह मंदिर भगवान शिव और भगवान विष्णु को समर्पित है। यह बंगाल की खाड़ी के पास अपने आश्चर्यजनक स्थान, जटिल नक्काशी और द्रविड़ वास्तुकला शैली के लिए प्रसिद्ध है। यह मंदिर पल्लव वंश की वास्तुकला कौशल और समुद्री विरासत का प्रतीक है।",
            "French": "Le temple du Rivage à Mahabalipuram, Tamil Nadu, est un site du patrimoine mondial de l'UNESCO et l'un des plus anciens temples en pierre structurels du sud de l'Inde. Construit au VIIIe siècle par la dynastie Pallava, le temple est dédié à Lord Shiva et Lord Vishnu. Il est renommé pour son emplacement magnifique près du golfe du Bengale, ses sculptures complexes et son style architectural dravidien. Le temple est un symbole de la prouesse architecturale et du patrimoine maritime de la dynastie Pallava.",
            "Spanish": "El Templo de la Orilla en Mahabalipuram, Tamil Nadu, es un sitio del Patrimonio Mundial de la UNESCO y uno de los templos de piedra estructurales más antiguos del sur de la India. Construido en el siglo VIII por la dinastía Pallava, el templo está dedicado al Señor Shiva y al Señor Vishnu. Es famoso por su impresionante ubicación junto a la Bahía de Bengala, sus intrincados tallados y su estilo arquitectónico dravidiano. El templo es un símbolo de la destreza arquitectónica y el patrimonio marítimo de la dinastía Pallava.",
            "German": "Der Ufertempel in Mahabalipuram, Tamil Nadu, ist ein UNESCO-Weltkulturerbe und einer der ältesten strukturellen Steintempel Südindiens. Der im 8. Jahrhundert von der Pallava-Dynastie erbaute Tempel ist Lord Shiva und Lord Vishnu gewidmet. Er ist berühmt für seine atemberaubende Lage am Golf von Bengalen, seine kunstvollen Schnitzereien und seinen dravidischen Architekturstil. Der Tempel ist ein Symbol für die architektonische Meisterschaft und das maritime Erbe der Pallava-Dynastie."
        },
        "spoken_languages": ["Tamil", "English", "Hindi"]
    },
    "Great Living Chola Temples": {
        "location": "Tamil Nadu",
        "languages": {
            "English": "The Great Living Chola Temples, a UNESCO World Heritage Site, comprise three magnificent temples built by the Chola dynasty: the Brihadeeswara Temple in Thanjavur, the Airavatesvara Temple in Darasuram, and the Gangaikonda Cholapuram Temple. These temples are renowned for their architectural grandeur, intricate carvings, and cultural significance. They represent the zenith of Chola art and architecture and are still active places of worship, showcasing the living traditions of Tamil culture.",
            "Tamil": "பெரிய சோழர் கோயில்கள் ஒரு யுனெஸ்கோ உலக பாரம்பரிய தளம் மற்றும் சோழர்களால் கட்டப்பட்ட மூன்று பிரம்மாண்டமான கோயில்களை உள்ளடக்கியது: தஞ்சாவூரில் உள்ள பிரகதீஸ்வரர் கோயில், தாராசுரத்தில் உள்ள ஐராவதேஸ்வரர் கோயில் மற்றும் கங்கைகொண்ட சோழபுரம் கோயில். இந்த கோயில்கள் அவற்றின் கட்டிடக்கலை பிரம்மாண்டம், சிக்கலான செதுக்குதல்கள் மற்றும் கலாச்சார முக்கியத்துவத்திற்கு பெயர் பெற்றவை. இவை சோழர்களின் கலை மற்றும் கட்டிடக்கலையின் உச்சத்தை பிரதிபலிக்கின்றன மற்றும் இன்னும் செயல்பாட்டில் உள்ள வழிபாட்டுத் தலங்களாக உள்ளன, தமிழ் கலாச்சாரத்தின் வாழும் பாரம்பரியங்களை காட்டுகின்றன.",
            "Hindi": "महान जीवित चोल मंदिर, एक यूनेस्को विश्व धरोहर स्थल, चोल वंश द्वारा निर्मित तीन शानदार मंदिरों से बना है: तंजावुर में बृहदीश्वर मंदिर, दारासुरम में ऐरावतेश्वर मंदिर और गंगैकोण्ड चोलपुरम मंदिर। ये मंदिर अपनी वास्तुकला की भव्यता, जटिल नक्काशी और सांस्कृतिक महत्व के लिए प्रसिद्ध हैं। ये चोल कला और वास्तुकला के शिखर का प्रतिनिधित्व करते हैं और अभी भी सक्रिय पूजा स्थल हैं, जो तमिल संस्कृति की जीवित परंपराओं को प्रदर्शित करते हैं।",
            "French": "Les grands temples vivants Chola, un site du patrimoine mondial de l'UNESCO, comprennent trois magnifiques temples construits par la dynastie Chola : le temple Brihadeeswara à Thanjavur, le temple Airavatesvara à Darasuram et le temple de Gangaikonda Cholapuram. Ces temples sont renommés pour leur grandeur architecturale, leurs sculptures complexes et leur importance culturelle. Ils représentent l'apogée de l'art et de l'architecture Chola et sont encore des lieux de culte actifs, montrant les traditions vivantes de la culture tamoule.",
            "Spanish": "Los Grandes Templos Vivientes de Chola, un sitio del Patrimonio Mundial de la UNESCO, comprenden tres magníficos templos construidos por la dinastía Chola: el Templo Brihadeeswara en Thanjavur, el Templo Airavatesvara en Darasuram y el Templo de Gangaikonda Cholapuram. Estos templos son famosos por su grandeza arquitectónica, sus intrincados tallados y su importancia cultural. Representan la cúspide del arte y la arquitectura Chola y siguen siendo lugares de culto activos, mostrando las tradiciones vivas de la cultura tamil.",
            "German": "Die Großen Lebenden Chola-Tempel, ein UNESCO-Weltkulturerbe, umfassen drei prächtige Tempel, die von der Chola-Dynastie erbaut wurden: der Brihadeeswara-Tempel in Thanjavur, der Airavatesvara-Tempel in Darasuram und der Gangaikonda Cholapuram-Tempel. Diese Tempel sind berühmt für ihre architektonische Pracht, kunstvollen Schnitzereien und kulturelle Bedeutung. Sie repräsentieren den Höhepunkt der Chola-Kunst und -Architektur und sind noch immer aktive Kultstätten, die die lebendigen Traditionen der tamilischen Kultur zeigen."
        },
        "spoken_languages": ["Tamil", "English", "Hindi"]
    }
}
# Function to generate dynamic insights using GPT API
def generate_gpt_insight(site_name, language="English"):
    try:
        prompt = f"Provide a detailed and engaging insight about the heritage site {site_name} in {language}."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=300  # Increase tokens for longer content
        )
        return response.choices[0].text.strip()
    except openai.error.AuthenticationError:
        print("Error: Invalid OpenAI API key. Please check your API key and try again.")
        return None
    except Exception as e:
        print(f"An error occurred while generating GPT insight: {e}")
        return None

# Function to convert text to speech using gTTS
def text_to_speech(text, language="en"):
    try:
        # Map languages to gTTS language codes
        lang_codes = {
            "English": "en",
            "Tamil": "ta",
            "Hindi": "hi",
            "French": "fr",
            "Spanish": "es",
            "German": "de"
        }
        lang_code = lang_codes.get(language, "en")  # Default to English if language not found

        # Use gTTS for text-to-speech
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save("heritage_insight.mp3")
        os.system("start heritage_insight.mp3")  # For Windows
        # os.system("afplay heritage_insight.mp3")  # For macOS
        # os.system("mpg321 heritage_insight.mp3")  # For Linux
    except Exception as e:
        print(f"An error occurred while converting text to speech: {e}")

# Main function to provide heritage site insights
def provide_heritage_insight(site_name, language="English"):
    if site_name not in heritage_sites:
        print("Heritage site not found in the database.")
        return

    site_info = heritage_sites[site_name]
    location = site_info["location"]

    # Get insight for the selected language
    if language in site_info["languages"]:
        insight = site_info["languages"][language]
    else:
        print(f"Language '{language}' not available. Defaulting to English.")
        insight = site_info["languages"]["English"]

    # Generate dynamic insight using GPT API
    gpt_insight = generate_gpt_insight(site_name, language)
    if gpt_insight:
        print(f"Insight: {gpt_insight}")
    else:
        print("Using pre-defined insight due to GPT API error.")
        gpt_insight = insight

    # Add spoken languages information
    spoken_languages = ", ".join(site_info["spoken_languages"])
    full_info = f"{gpt_insight}\n\nMost frequently spoken languages in {location}: {spoken_languages}"

    # Convert to speech
    text_to_speech(full_info, language)

# User interaction
if __name__ == "__main__":
    print("Welcome to the Indian Heritage Explorer!")
    print("Available heritage sites:")
    for site in heritage_sites:
        print(f"- {site}")

    site_name = input("Enter the name of the heritage site: ")
    language = input("Choose language (English, Tamil, Hindi, French, Spanish, German): ").strip().capitalize()

    provide_heritage_insight(site_name, language)