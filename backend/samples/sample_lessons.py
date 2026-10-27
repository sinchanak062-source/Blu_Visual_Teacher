"""
Built-in reference lesson plans in multiple languages for offline resilience.
"""

SAMPLE_LESSONS = {
    # 1. Python Loops
    "python_loops": {
        "en": {
            "title": "How a Python loop works",
            "level": "beginner",
            "language": "en",
            "target_length": 45,
            "scenes": [
                {
                    "type": "title_card",
                    "heading": "How does a Python loop work?",
                    "narration": "A loop repeats an instruction for each value in a sequence, saving time and code."
                },
                {
                    "type": "code_walkthrough",
                    "heading": "Step 1: Read the code",
                    "code": "for i in range(3):\n    print(i)",
                    "highlight_lines": [1],
                    "narration": "The range of three generates three consecutive values: zero, one, and two."
                },
                {
                    "type": "diagram",
                    "heading": "Step 2: Watch each iteration",
                    "items": ["i = 0", "i = 1", "i = 2"],
                    "arrows": [["i = 0", "i = 1"], ["i = 1", "i = 2"]],
                    "narration": "In each pass, the variable i takes the next value, then executes the print statement."
                },
                {
                    "type": "timeline",
                    "heading": "Step 3: Loop Lifecycle",
                    "steps": ["Start Range", "Set i = 0", "Set i = 1", "Set i = 2", "Loop Done"],
                    "narration": "The loop automatically advances step by step until the sequence finishes."
                },
                {
                    "type": "quiz",
                    "heading": "Concept Check",
                    "question": "What is the final value printed by range(3)?",
                    "options": ["1", "2", "3", "0"],
                    "correct_index": 1,
                    "narration": "Remember: range in Python starts at zero and stops before three, so the final printed value is two."
                }
            ]
        },
        "hi": {
            "title": "पायथन लूप कैसे काम करता है",
            "level": "beginner",
            "language": "hi",
            "target_length": 45,
            "scenes": [
                {
                    "type": "title_card",
                    "heading": "पायथन लूप कैसे काम करता है?",
                    "narration": "लूप एक ही निर्देश को क्रम के हर मान के लिए बार-बार दोहराता है।"
                },
                {
                    "type": "code_walkthrough",
                    "heading": "चरण 1: कोड को समझें",
                    "code": "for i in range(3):\n    print(i)",
                    "highlight_lines": [1],
                    "narration": "range(3) हमें तीन लगातार मान देता है: शून्य, एक और दो।"
                },
                {
                    "type": "diagram",
                    "heading": "चरण 2: हर चक्र को देखें",
                    "items": ["i = 0", "i = 1", "i = 2"],
                    "arrows": [["i = 0", "i = 1"], ["i = 1", "i = 2"]],
                    "narration": "हर चक्र में i अगला मान लेता है और प्रिंट कमांड चलाता है।"
                },
                {
                    "type": "timeline",
                    "heading": "चरण 3: लूप का जीवन चक्र",
                    "steps": ["शुरुआत", "पहला मान i = 0", "दूसरा मान i = 1", "तीसरा मान i = 2", "लूप समाप्त"],
                    "narration": "लूप क्रमवार आगे बढ़ता है और क्रम पूरा होते ही समाप्त हो जाता है।"
                },
                {
                    "type": "quiz",
                    "heading": "अभ्यास प्रश्न",
                    "question": "range(3) का अंतिम प्रिंट मान क्या होगा?",
                    "options": ["1", "2", "3", "0"],
                    "correct_index": 1,
                    "narration": "पायथन में गिनती शून्य से शुरू होती है, इसलिए अंतिम प्रिंट मान दो होगा।"
                }
            ]
        },
        "ta": {
            "title": "பைதான் லூப் எவ்வாறு செயல்படுகிறது",
            "level": "beginner",
            "language": "ta",
            "target_length": 45,
            "scenes": [
                {
                    "type": "title_card",
                    "heading": "பைதான் லூப் எவ்வாறு செயல்படுகிறது?",
                    "narration": "ஒரு வரிசையில் உள்ள ஒவ்வொரு மதிப்புக்கும் லூப் மீண்டும் மீண்டும் இயங்குகிறது."
                },
                {
                    "type": "code_walkthrough",
                    "heading": "படி 1: குறியீட்டைப் படியுங்கள்",
                    "code": "for i in range(3):\n    print(i)",
                    "highlight_lines": [1],
                    "narration": "range(3) என்பது பூஜ்ஜியம், ஒன்று மற்றும் இரண்டு ஆகிய மூன்று மதிப்புகளைத் தருகிறது."
                },
                {
                    "type": "diagram",
                    "heading": "படி 2: ஒவ்வொரு சுழற்சியையும் கவனியுங்கள்",
                    "items": ["i = 0", "i = 1", "i = 2"],
                    "arrows": [["i = 0", "i = 1"], ["i = 1", "i = 2"]],
                    "narration": "ஒவ்வொரு சுழற்சியிலும் i அடுத்த மதிப்பை எடுத்து அச்சிடுகிறது."
                },
                {
                    "type": "timeline",
                    "heading": "படி 3: லூப் வரிசை",
                    "steps": ["தொடக்க நிலை", "i = 0", "i = 1", "i = 2", "முடிவு"],
                    "narration": "வரிசை முடியும் வரை லூப் தானாகவே இயங்கி முடிகிறது."
                },
                {
                    "type": "quiz",
                    "heading": "வினாடி வினா",
                    "question": "range(3) அச்சிடும் கடைசி மதிப்பு என்ன?",
                    "options": ["1", "2", "3", "0"],
                    "correct_index": 1,
                    "narration": "பைதானில் பூஜ்ஜியத்தில் தொடங்குவதால், அச்சிடப்படும் கடைசி மதிப்பு இரண்டு ஆகும்."
                }
            ]
        },
        "te": {
            "title": "పైథాన్ లూప్ ఎలా పనిచేస్తుంది",
            "level": "beginner",
            "language": "te",
            "target_length": 45,
            "scenes": [
                {
                    "type": "title_card",
                    "heading": "పైథాన్ లూప్ ఎలా పనిచేస్తుంది?",
                    "narration": "ఒక శ్రేణిలోని ప్రతి విలువకు ఒక సూచనను లూప్ మళ్లీ మళ్లీ అమలు చేస్తుంది."
                },
                {
                    "type": "code_walkthrough",
                    "heading": "దశ 1: కోడ్‌ను గమనించండి",
                    "code": "for i in range(3):\n    print(i)",
                    "highlight_lines": [1],
                    "narration": "range(3) అనేది సున్నా, ఒకటి మరియు రెండు అనే మూడు విలువలను ఇస్తుంది."
                },
                {
                    "type": "diagram",
                    "heading": "దశ 2: ప్రతి ఇటరేషన్ చూడండి",
                    "items": ["i = 0", "i = 1", "i = 2"],
                    "arrows": [["i = 0", "i = 1"], ["i = 1", "i = 2"]],
                    "narration": "ప్రతి లూప్‌లో i తదుపరి విలువను తీసుకుని ప్రింట్ చేస్తుంది."
                },
                {
                    "type": "timeline",
                    "heading": "దశ 3: లూప్ సైకిల్",
                    "steps": ["ప్రారంభం", "విలువ i = 0", "విలువ i = 1", "విలువ i = 2", "లూప్ ముగింపు"],
                    "narration": "శ్రేణి పూర్తయ్యే వరకు లూప్ సజావుగా సాగుతుంది."
                },
                {
                    "type": "quiz",
                    "heading": "క్విజ్ ప్రశ్న",
                    "question": "range(3) ప్రింట్ చేసే చివరి విలువ ఏమిటి?",
                    "options": ["1", "2", "3", "0"],
                    "correct_index": 1,
                    "narration": "పైథాన్‌లో లెక్కింపు సున్నా నుండి మొదలవుతుంది కాబట్టి చివరి విలువ రెండు."
                }
            ]
        }
    },

    # 2. Binary Search
    "binary_search": {
        "en": {
            "title": "Understanding Binary Search",
            "level": "intermediate",
            "language": "en",
            "target_length": 50,
            "scenes": [
                {
                    "type": "title_card",
                    "heading": "What is Binary Search?",
                    "narration": "Binary search is an ultra-fast algorithm to find a target in a sorted list by repeatedly halving the search space."
                },
                {
                    "type": "diagram",
                    "heading": "Step 1: Divide and Conquer",
                    "items": ["Left: 0", "Mid: 4", "Right: 8"],
                    "arrows": [["Left: 0", "Mid: 4"], ["Mid: 4", "Right: 8"]],
                    "narration": "We check the middle element. If our target is smaller, we discard the right half entirely."
                },
                {
                    "type": "code_walkthrough",
                    "heading": "Step 2: Core Search Logic",
                    "code": "mid = (low + high) // 2\nif arr[mid] == target:\n    return mid\nelif arr[mid] < target:\n    low = mid + 1",
                    "highlight_lines": [1, 2],
                    "narration": "Calculate the mid index. If match found, return it. Otherwise adjust low or high boundary."
                },
                {
                    "type": "timeline",
                    "heading": "Step 3: Halving the List",
                    "steps": ["Full List (16 items)", "8 items left", "4 items left", "Target Found!"],
                    "narration": "In each step, half of the remaining elements disappear, yielding logarithmic O of log N speed."
                },
                {
                    "type": "quiz",
                    "heading": "Concept Check",
                    "question": "What is the prerequisite for Binary Search?",
                    "options": ["Array must be sorted", "Array must contain numbers only", "Array size must be even", "Array must be empty"],
                    "correct_index": 0,
                    "narration": "Binary search only works on sorted collections so that halving correctly determines which half contains the target."
                }
            ]
        },
        "hi": {
            "title": "बाइनरी सर्च को समझें",
            "level": "intermediate",
            "language": "hi",
            "target_length": 50,
            "scenes": [
                {
                    "type": "title_card",
                    "heading": "बाइनरी सर्च क्या है?",
                    "narration": "बाइनरी सर्च क्रमबद्ध सूची में किसी तत्व को खोजने का बहुत ही तेज़ तरीका है।"
                },
                {
                    "type": "diagram",
                    "heading": "चरण 1: बीच का तत्व जांचें",
                    "items": ["बायां भाग", "मध्य तत्व", "दायां भाग"],
                    "arrows": [["बायां भाग", "मध्य तत्व"], ["मध्य तत्व", "दायां भाग"]],
                    "narration": "हम बीच के तत्व की तुलना करते हैं और हर बार आधी सूची को छोड़ देते हैं।"
                },
                {
                    "type": "code_walkthrough",
                    "heading": "चरण 2: बाइनरी सर्च कोड",
                    "code": "mid = (low + high) // 2\nif arr[mid] == target:\n    return mid\nelif arr[mid] < target:\n    low = mid + 1",
                    "highlight_lines": [1, 2],
                    "narration": "मध्य इंडेक्स निकालें। यदि लक्ष्य मिल जाए तो वापस करें, नहीं तो सीमा बदलें।"
                },
                {
                    "type": "timeline",
                    "heading": "चरण 3: गति और समय जटिलता",
                    "steps": ["पूरी सूची (16)", "बचे 8 तत्व", "बचे 4 तत्व", "लक्ष्य मिल गया!"],
                    "narration": "हर कदम पर सूची आधी हो जाती है, जिससे यह O of log N समय में काम करता है।"
                },
                {
                    "type": "quiz",
                    "heading": "अभ्यास प्रश्न",
                    "question": "बाइनरी सर्च के लिए अनिवार्य शर्त क्या है?",
                    "options": ["सूची क्रमबद्ध (sorted) होनी चाहिए", "केवल सम संख्याएं हों", "सूची छोटी होनी चाहिए", "कोई शर्त नहीं"],
                    "correct_index": 0,
                    "narration": "बाइनरी सर्च तभी काम करता है जब डेटा पहले से क्रमबद्ध यानी सॉर्टेड हो।"
                }
            ]
        }
    },

    # 3. Photosynthesis
    "photosynthesis": {
        "en": {
            "title": "How Photosynthesis Works",
            "level": "beginner",
            "language": "en",
            "target_length": 45,
            "scenes": [
                {
                    "type": "title_card",
                    "heading": "How Photosynthesis Works",
                    "narration": "Photosynthesis is the process plants use to convert sunlight, water, and carbon dioxide into food and oxygen."
                },
                {
                    "type": "diagram",
                    "heading": "Step 1: Ingredients & Energy",
                    "items": ["Sunlight", "Water (H2O)", "CO2", "Chlorophyll"],
                    "arrows": [["Sunlight", "Chlorophyll"], ["Water (H2O)", "Chlorophyll"], ["CO2", "Chlorophyll"]],
                    "narration": "Chlorophyll in green leaves captures photon energy to split water and capture carbon dioxide."
                },
                {
                    "type": "code_walkthrough",
                    "heading": "Step 2: Chemical Reaction",
                    "code": "6 CO2 + 6 H2O + Light Energy\n  ==> C6H12O6 (Glucose)\n    + 6 O2 (Oxygen)",
                    "highlight_lines": [1, 2, 3],
                    "narration": "Six carbon dioxide molecules and six water molecules produce one glucose molecule and six oxygen molecules."
                },
                {
                    "type": "timeline",
                    "heading": "Step 3: Energy Flow",
                    "steps": ["Light Absorption", "Water Splitting", "ATP Energy", "Glucose Production", "Oxygen Released"],
                    "narration": "Solar energy is stored in chemical bonds, fueling the plant while releasing vital oxygen into the air."
                },
                {
                    "type": "quiz",
                    "heading": "Concept Check",
                    "question": "What vital gas is released into the atmosphere during photosynthesis?",
                    "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Methane"],
                    "correct_index": 0,
                    "narration": "Plants release oxygen as a byproduct, providing the air that animals and humans breathe."
                }
            ]
        },
        "hi": {
            "title": "प्रकाश संश्लेषण कैसे काम करता है",
            "level": "beginner",
            "language": "hi",
            "target_length": 45,
            "scenes": [
                {
                    "type": "title_card",
                    "heading": "प्रकाश संश्लेषण की प्रक्रिया",
                    "narration": "प्रकाश संश्लेषण वह प्रक्रिया है जिससे पौधे सूर्य के प्रकाश, पानी और कार्बन डाइऑक्साइड से भोजन बनाते हैं।"
                },
                {
                    "type": "diagram",
                    "heading": "चरण 1: आवश्यक तत्व",
                    "items": ["सूर्य का प्रकाश", "पानी (H2O)", "कार्बन डाइऑक्साइड", "क्लोरोफिल"],
                    "arrows": [["सूर्य का प्रकाश", "क्लोरोफिल"], ["पानी (H2O)", "क्लोरोफिल"], ["कार्बन डाइऑक्साइड", "क्लोरोफिल"]],
                    "narration": "पत्तियों में मौजूद क्लोरोफिल सूर्य की ऊर्जा को सोखता है और रासायनिक क्रिया करता है।"
                },
                {
                    "type": "code_walkthrough",
                    "heading": "चरण 2: रासायनिक समीकरण",
                    "code": "6 CO2 + 6 H2O + प्रकाश\n  ==> C6H12O6 (ग्लूकोज)\n    + 6 O2 (ऑक्सीजन)",
                    "highlight_lines": [1, 2, 3],
                    "narration": "छह CO2 और छह पानी के अणु मिलकर ग्लूकोज और सांस लेने योग्य ऑक्सीजन बनाते हैं।"
                },
                {
                    "type": "timeline",
                    "heading": "चरण 3: ऊर्जा का चक्र",
                    "steps": ["प्रकाश अवशोषण", "जल विघटन", "ऊर्जा निर्माण", "ग्लूकोज संचय", "ऑक्सीजन विसर्जन"],
                    "narration": "सौर ऊर्जा को रासायनिक ऊर्जा में बदलकर पौधे अपना भोजन बनाते हैं और वातावरण में ऑक्सीजन छोड़ते हैं।"
                },
                {
                    "type": "quiz",
                    "heading": "अभ्यास प्रश्न",
                    "question": "प्रकाश संश्लेषण के दौरान कौन सी गैस बाहर निकलती है?",
                    "options": ["ऑक्सीजन", "कार्बन डाइऑक्साइड", "नाइट्रोजन", "हाइड्रोजन"],
                    "correct_index": 0,
                    "narration": "पौधे ऑक्सीजन को उप-उत्पाद के रूप में छोड़ते हैं, जिससे हम सांस लेते हैं।"
                }
            ]
        }
    }
}


def get_sample_lesson(topic: str, lang: str = "en") -> dict:
    """
    Returns a matching sample lesson if topic matches, or a robust default.
    """
    topic_clean = topic.lower().strip()
    
    if "python" in topic_clean or "loop" in topic_clean:
        key = "python_loops"
    elif "search" in topic_clean or "binary" in topic_clean or "algorithm" in topic_clean:
        key = "binary_search"
    elif "photo" in topic_clean or "plant" in topic_clean or "biology" in topic_clean:
        key = "photosynthesis"
    else:
        key = "python_loops"
        
    lesson_bundle = SAMPLE_LESSONS[key]
    if lang in lesson_bundle:
        return lesson_bundle[lang]
    elif "en" in lesson_bundle:
        return lesson_bundle["en"]
    return SAMPLE_LESSONS["python_loops"]["en"]
