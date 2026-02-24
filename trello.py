import requests

# Trello credentials


def create_list(name, pos="bottom"):
    """Create a new list on the board"""
    url = "https://api.trello.com/1/lists"
    params = {
        "key": API_KEY,
        "token": TOKEN,
        "name": name,
        "idBoard": BOARD_ID,
        "pos": pos
    }
    response = requests.post(url, params=params)
    return response.json()

def create_card(list_id, name, desc="", due_date=None, labels=None):
    """Create a card in a specific list"""
    url = "https://api.trello.com/1/cards"
    params = {
        "key": API_KEY,
        "token": TOKEN,
        "idList": list_id,
        "name": name,
        "desc": desc
    }
    
    if due_date:
        params["due"] = due_date
    
    response = requests.post(url, params=params)
    card = response.json()
    
    # Add labels if specified
    if labels and "id" in card:
        for label_color in labels:
            add_label_to_card(card["id"], label_color)
    
    return card

def add_label_to_card(card_id, color):
    """Add a colored label to a card"""
    url = f"https://api.trello.com/1/cards/{card_id}/labels"
    params = {
        "key": API_KEY,
        "token": TOKEN,
        "color": color
    }
    requests.post(url, params=params)

def create_checklist(card_id, name, items):
    """Create a checklist on a card"""
    # Create checklist
    url = "https://api.trello.com/1/checklists"
    params = {
        "key": API_KEY,
        "token": TOKEN,
        "idCard": card_id,
        "name": name
    }
    response = requests.post(url, params=params)
    checklist = response.json()
    
    # Add items to checklist
    if "id" in checklist:
        for item in items:
            add_checklist_item(checklist["id"], item)
    
    return checklist

def add_checklist_item(checklist_id, name):
    """Add an item to a checklist"""
    url = f"https://api.trello.com/1/checklists/{checklist_id}/checkItems"
    params = {
        "key": API_KEY,
        "token": TOKEN,
        "name": name
    }
    requests.post(url, params=params)

print("Setting up AMMS FYP Trello Board...")
print("=" * 60)

# Create Lists for different phases
lists_structure = [
    "PROJECT OVERVIEW",
    "PHASE 1: Requirements (COMPLETED)",
    "PHASE 2: Design (COMPLETED)",
    "PHASE 3: Software Development (COMPLETED)",
    "SPRINT 4: Hardware Setup (IN PROGRESS)",
    "SPRINT 5: Voice Scheduling (NOT STARTED)",
    "SPRINT 6: Email Assistant (NOT STARTED)",
    "PHASE 4: Testing (NOT STARTED)",
    "PHASE 5: Documentation (NOT STARTED)",
    "MILESTONES"
]

created_lists = {}
for list_name in lists_structure:
    print(f"Creating list: {list_name}")
    list_obj = create_list(list_name)
    created_lists[list_name] = list_obj["id"]

print("\n" + "=" * 60)
print("Creating cards for all tasks...")
print("=" * 60 + "\n")

# ========================================
# PROJECT OVERVIEW
# ========================================
print("Creating Project Overview...")

overview_card = create_card(
    created_lists["PROJECT OVERVIEW"],
    "AMMS - AI Mirror Management System",
    """**Project:** Final Year Project
**Timeline:** November 2024 - March 2025

**Objective:** 
Develop an AI-powered smart mirror with:
- Facial recognition authentication
- Morning briefings (calendar, weather, news)
- Natural voice interaction
- Voice-controlled scheduling
- Intelligent email assistant

**Current Status:** Hardware Integration Phase
**Next Milestone:** M6 - Hardware Ready""",
    labels=["blue"]
)

# ========================================
# PHASE 1: REQUIREMENTS (COMPLETED)
# ========================================
print("\nCreating Phase 1: Requirements (COMPLETED)...")

phase1_cards = [
    {
        "name": "PHASE 1: PROJECT INITIATION AND REQUIREMENTS",
        "desc": """**Status:** COMPLETED

**Overview:**
Established foundation for AMMS project by identifying requirements, analyzing user needs, and planning development sprints.

**Key Achievements:**
- User requirements identified
- Product backlog created
- Sprint planning completed
- Team roles assigned
- Project timeline established""",
        "labels": ["green"]
    },
    {
        "name": "Identifying AI Assistant Requirements",
        "desc": """**Status:** COMPLETED

**Tasks Completed:**
- Identified core AI assistant functionalities
- Defined facial recognition requirements
- Outlined emotion detection capabilities
- Specified motivational feedback features
- Listed email messaging requirements
- Determined data integration needs""",
        "checklist": [
            "Facial recognition for multi-user support",
            "Emotion detection for personalized responses",
            "Motivational feedback system",
            "Email integration capabilities",
            "Data display requirements",
            "Voice interaction specifications"
        ],
        "labels": ["green"]
    },
    {
        "name": "Conduct User Needs Analysis",
        "desc": """**Status:** COMPLETED

**Tasks Completed:**
- Surveyed potential users
- Identified pain points in morning routines
- Analyzed productivity enhancement needs
- Gathered feedback on desired features
- Prioritized user requirements""",
        "checklist": [
            "User survey conducted",
            "Pain points documented",
            "Feature priorities established",
            "Accessibility requirements identified",
            "Privacy concerns addressed"
        ],
        "labels": ["green"]
    },
    {
        "name": "Create Product Backlog",
        "desc": """**Status:** COMPLETED

**Tasks Completed:**
- Created comprehensive product backlog
- Prioritized features using MoSCoW method
- Defined user stories
- Estimated story points
- Organized backlog by sprints""",
        "checklist": [
            "Product backlog created",
            "User stories documented",
            "Features prioritized",
            "Story points estimated",
            "Sprint assignments planned"
        ],
        "labels": ["green"]
    },
    {
        "name": "Sprint Planning",
        "desc": """**Status:** COMPLETED

**Tasks Completed:**
- Planned 6 development sprints
- Allocated features to sprints
- Defined sprint deliverables
- Established sprint duration
- Set milestone dates""",
        "checklist": [
            "Sprint 1-6 planned",
            "Features allocated to each sprint",
            "Sprint goals defined",
            "Deliverables identified",
            "Timeline established"
        ],
        "labels": ["green"]
    },
    {
        "name": "Define Sprint Goals and Timeline",
        "desc": """**Status:** COMPLETED

**Tasks Completed:**
- Set specific goals for each sprint
- Created detailed timeline
- Identified dependencies
- Allocated resources
- Set milestone checkpoints""",
        "checklist": [
            "Sprint goals documented",
            "Timeline with dates created",
            "Task dependencies mapped",
            "Resource allocation planned",
            "Milestones defined"
        ],
        "labels": ["green"]
    },
    {
        "name": "Assign Team Roles for Sprint",
        "desc": """**Status:** COMPLETED

**Tasks Completed:**
- Defined team roles and responsibilities
- Assigned tasks to team members
- Established communication protocols
- Set up collaboration tools
- Created workflow processes""",
        "checklist": [
            "Team roles defined",
            "Responsibilities assigned",
            "Communication channels established",
            "Collaboration tools set up",
            "Workflow documented"
        ],
        "labels": ["green"]
    }
]

for card_data in phase1_cards:
    card = create_card(
        created_lists["PHASE 1: Requirements (COMPLETED)"],
        card_data["name"],
        card_data["desc"],
        None,
        card_data.get("labels", ["green"])
    )
    if "checklist" in card_data:
        create_checklist(card["id"], "Tasks", card_data["checklist"])
    print(f"  Created: {card_data['name']}")

# ========================================
# PHASE 2: DESIGN (COMPLETED)
# ========================================
print("\nCreating Phase 2: Design (COMPLETED)...")

phase2_cards = [
    {
        "name": "PHASE 2: DESIGN AND DEVELOPMENT",
        "desc": """**Status:** COMPLETED

**Overview:**
Designed complete system architecture, prototyped all subsystems, and refined design based on user feedback.

**Key Achievements:**
- System architecture defined
- All 5 core modules designed
- Subsystems prototyped
- Technical diagrams created
- Design validated with users""",
        "labels": ["green"]
    },
    {
        "name": "Define Core System Architecture",
        "desc": """**Status:** COMPLETED

**Tasks Completed:**
- Designed overall system architecture
- Defined module interactions
- Established data flow patterns
- Selected technology stack
- Created architecture diagrams""",
        "checklist": [
            "System architecture diagram created",
            "Module interactions defined",
            "Technology stack selected",
            "Data flow documented",
            "Security architecture planned"
        ],
        "labels": ["green"]
    },
    {
        "name": "Facial Recognition Module Design",
        "desc": """**Status:** COMPLETED

**Design Completed:**
- Multi-user face detection system
- Recognition algorithm selection
- Database structure for face encodings
- Privacy controls design
- Authentication flow diagram""",
        "checklist": [
            "Face detection algorithm selected",
            "Multi-user support designed",
            "Database schema created",
            "Privacy controls specified",
            "Error handling planned"
        ],
        "labels": ["green"]
    },
    {
        "name": "Emotion Detection Module Design",
        "desc": """**Status:** COMPLETED

**Design Completed:**
- Emotion recognition algorithm
- Real-time processing pipeline
- Emotion classification categories
- Response generation logic
- Integration with feedback module""",
        "checklist": [
            "Emotion detection library selected",
            "Processing pipeline designed",
            "Emotion categories defined",
            "Response logic created",
            "Performance optimization planned"
        ],
        "labels": ["green"]
    },
    {
        "name": "Motivational Feedback Module Design",
        "desc": """**Status:** COMPLETED

**Design Completed:**
- Context-aware message generation
- Personalization engine design
- Message database structure
- Timing and delivery logic
- User preference system""",
        "checklist": [
            "Message generation system designed",
            "Personalization rules defined",
            "Message categories created",
            "Delivery timing logic specified",
            "User preferences schema created"
        ],
        "labels": ["green"]
    },
    {
        "name": "Email Messaging Module Design",
        "desc": """**Status:** COMPLETED

**Design Completed:**
- Gmail API integration architecture
- Email summarization with LLM
- Voice dictation system design
- Natural language processing flow
- Privacy-first architecture""",
        "checklist": [
            "Gmail API integration designed",
            "LLM integration architecture created",
            "Voice dictation flow specified",
            "NLP pipeline designed",
            "Local processing ensured"
        ],
        "labels": ["green"]
    },
    {
        "name": "Data Integration Display Design",
        "desc": """**Status:** COMPLETED

**Design Completed:**
- UI/UX design for mirror display
- Calendar integration design
- Weather API integration
- News feed aggregation
- Responsive layout design""",
        "checklist": [
            "UI mockups created",
            "Calendar API integration designed",
            "Weather API selected",
            "News feed sources identified",
            "Responsive design system created"
        ],
        "labels": ["green"]
    },
    {
        "name": "Prototype Subsystems",
        "desc": """**Status:** COMPLETED

**Prototypes Created:**
- Facial recognition proof of concept
- Emotion detection demo
- Voice interaction prototype
- Email integration mockup
- UI/UX interactive prototype""",
        "checklist": [
            "Face recognition prototype",
            "Emotion detection prototype",
            "Voice interaction demo",
            "Email integration mockup",
            "UI prototype created"
        ],
        "labels": ["green"]
    },
    {
        "name": "Create Technical Diagrams",
        "desc": """**Status:** COMPLETED

**Diagrams Created:**
- System architecture diagram
- Data flow diagrams
- Sequence diagrams
- Entity relationship diagrams
- Network architecture diagram
- Deployment diagram""",
        "checklist": [
            "System architecture diagram",
            "Data flow diagrams",
            "Sequence diagrams",
            "ER diagram for database",
            "Network architecture",
            "Deployment diagram"
        ],
        "labels": ["green"]
    },
    {
        "name": "Collect User Feedback on Prototypes",
        "desc": """**Status:** COMPLETED

**Feedback Collection:**
- Demonstrated prototypes to users
- Collected structured feedback
- Identified usability issues
- Prioritized design improvements
- Validated feature set""",
        "checklist": [
            "User testing sessions conducted",
            "Feedback forms collected",
            "Usability issues identified",
            "Improvement priorities set",
            "Feature validation completed"
        ],
        "labels": ["green"]
    },
    {
        "name": "Refine Design Based on Feedback",
        "desc": """**Status:** COMPLETED

**Design Refinements:**
- Simplified UI navigation
- Enhanced personalization options
- Improved voice command clarity
- Added more privacy controls
- Optimized workflow efficiency""",
        "checklist": [
            "UI navigation redesigned",
            "Personalization enhanced",
            "Voice commands improved",
            "Privacy controls added",
            "Workflow optimized"
        ],
        "labels": ["green"]
    }
]

for card_data in phase2_cards:
    card = create_card(
        created_lists["PHASE 2: Design (COMPLETED)"],
        card_data["name"],
        card_data["desc"],
        None,
        card_data.get("labels", ["green"])
    )
    if "checklist" in card_data:
        create_checklist(card["id"], "Tasks", card_data["checklist"])
    print(f"  Created: {card_data['name']}")

# ========================================
# PHASE 3: SOFTWARE DEVELOPMENT (COMPLETED)
# ========================================
print("\nCreating Phase 3: Software Development (COMPLETED)...")

phase3_cards = [
    {
        "name": "PHASE 3: SPRINT-BASED DEVELOPMENT",
        "desc": """**Status:** COMPLETED

**Overview:**
Completed software development for facial recognition, morning briefings, and AI communication modules.

**Key Achievements:**
- Sprint 1: Facial Recognition completed
- Sprint 2: Morning Briefings completed
- Sprint 3: AI Communication completed
- All software modules tested and functional""",
        "labels": ["green"]
    },
    {
        "name": "SPRINT 1: Facial Recognition Authentication",
        "desc": """**Status:** COMPLETED

**Sprint Overview:**
Developed and tested multi-user facial recognition system with privacy controls.

**Deliverables:**
- Multi-user face recognition working
- Face authentication integrated with camera
- User differentiation tested
- Privacy controls implemented""",
        "labels": ["green"]
    },
    {
        "name": "Develop Multi-User Face Recognition",
        "desc": """**Status:** COMPLETED

**Implementation:**
- Implemented face_recognition library
- Created face encoding database
- Developed user registration system
- Built recognition accuracy >95%
- Optimized for real-time processing""",
        "checklist": [
            "face_recognition library integrated",
            "Face encoding database created",
            "User registration flow implemented",
            "Recognition accuracy optimized",
            "Real-time processing achieved"
        ],
        "labels": ["green"]
    },
    {
        "name": "Integrate Face Auth with Camera",
        "desc": """**Status:** COMPLETED

**Implementation:**
- Connected USB camera to system
- Implemented video capture loop
- Integrated face detection with camera feed
- Optimized frame processing
- Added error handling""",
        "checklist": [
            "Camera driver installed",
            "Video capture implemented",
            "Face detection integrated",
            "Frame processing optimized",
            "Error handling added"
        ],
        "labels": ["green"]
    },
    {
        "name": "Test User Differentiation",
        "desc": """**Status:** COMPLETED

**Testing:**
- Tested with multiple users
- Verified user differentiation accuracy
- Tested in different lighting conditions
- Validated personalized responses
- Documented test results""",
        "checklist": [
            "Multi-user testing completed",
            "Differentiation accuracy >95%",
            "Lighting conditions tested",
            "Personalized responses validated",
            "Test results documented"
        ],
        "labels": ["green"]
    },
    {
        "name": "Implement Privacy Controls",
        "desc": """**Status:** COMPLETED

**Implementation:**
- Added user consent system
- Implemented data encryption
- Created privacy settings panel
- Added face data deletion option
- Documented privacy measures""",
        "checklist": [
            "User consent system added",
            "Face data encrypted",
            "Privacy settings created",
            "Data deletion implemented",
            "Privacy policy documented"
        ],
        "labels": ["green"]
    },
    {
        "name": "SPRINT 2: Morning Briefings & News",
        "desc": """**Status:** COMPLETED

**Sprint Overview:**
Developed personalized morning briefings with calendar, email, weather, and news integration.

**Deliverables:**
- Calendar/Email/Weather APIs integrated
- Personalized briefing logic working
- Business news feeds integrated
- Auto-delivery on face recognition tested""",
        "labels": ["green"]
    },
    {
        "name": "Integrate Calendar/Email/Weather APIs",
        "desc": """**Status:** COMPLETED

**Implementation:**
- Integrated Google Calendar API
- Connected Gmail API
- Integrated OpenWeatherMap API
- Built data aggregation system
- Tested API connectivity""",
        "checklist": [
            "Google Calendar API integrated",
            "Gmail API connected",
            "Weather API integrated",
            "Data aggregation built",
            "API connectivity tested"
        ],
        "labels": ["green"]
    },
    {
        "name": "Develop Personalized Briefing Logic",
        "desc": """**Status:** COMPLETED

**Implementation:**
- Created briefing template system
- Developed personalization engine
- Implemented priority ranking
- Built content filtering
- Optimized delivery timing""",
        "checklist": [
            "Briefing templates created",
            "Personalization engine built",
            "Priority ranking implemented",
            "Content filtering added",
            "Delivery timing optimized"
        ],
        "labels": ["green"]
    },
    {
        "name": "Integrate Business News Feeds",
        "desc": """**Status:** COMPLETED

**Implementation:**
- Selected news API sources
- Implemented news aggregation
- Created topic filtering
- Built summary generation
- Tested news delivery""",
        "checklist": [
            "News APIs selected",
            "News aggregation implemented",
            "Topic filtering created",
            "Summary generation built",
            "News delivery tested"
        ],
        "labels": ["green"]
    },
    {
        "name": "Test Auto-Delivery on Face Recognition",
        "desc": """**Status:** COMPLETED

**Testing:**
- Tested briefing trigger on face detection
- Verified personalized content delivery
- Tested timing accuracy
- Validated content relevance
- Documented test results""",
        "checklist": [
            "Face detection trigger tested",
            "Personalized delivery verified",
            "Timing accuracy validated",
            "Content relevance checked",
            "Test results documented"
        ],
        "labels": ["green"]
    },
    {
        "name": "SPRINT 3: Natural AI Communication",
        "desc": """**Status:** COMPLETED

**Sprint Overview:**
Developed natural voice interaction system with local LLM for privacy.

**Deliverables:**
- Multi-turn voice interaction working
- Local LLM integrated
- Natural language processing tested
- Conversational context maintained""",
        "labels": ["green"]
    },
    {
        "name": "Develop Multi-Turn Voice Interaction",
        "desc": """**Status:** COMPLETED

**Implementation:**
- Implemented speech recognition
- Built text-to-speech system
- Created conversation manager
- Developed context tracking
- Optimized response time""",
        "checklist": [
            "Speech recognition implemented",
            "Text-to-speech system built",
            "Conversation manager created",
            "Context tracking developed",
            "Response time optimized"
        ],
        "labels": ["green"]
    },
    {
        "name": "Integrate Local LLM for Privacy",
        "desc": """**Status:** COMPLETED

**Implementation:**
- Selected local LLM (Ollama/LLaMA)
- Installed and configured LLM
- Integrated with voice system
- Optimized for performance
- Tested offline functionality""",
        "checklist": [
            "Local LLM selected",
            "LLM installed and configured",
            "Voice integration completed",
            "Performance optimized",
            "Offline functionality tested"
        ],
        "labels": ["green"]
    },
    {
        "name": "Test Natural Language Processing",
        "desc": """**Status:** COMPLETED

**Testing:**
- Tested various commands
- Verified intent recognition
- Tested conversation flow
- Validated response accuracy
- Documented test cases""",
        "checklist": [
            "Command variations tested",
            "Intent recognition verified",
            "Conversation flow tested",
            "Response accuracy validated",
            "Test cases documented"
        ],
        "labels": ["green"]
    },
    {
        "name": "Refine Conversational Context",
        "desc": """**Status:** COMPLETED

**Refinement:**
- Improved context retention
- Enhanced follow-up question handling
- Optimized memory management
- Added disambiguation logic
- Tested edge cases""",
        "checklist": [
            "Context retention improved",
            "Follow-up handling enhanced",
            "Memory management optimized",
            "Disambiguation added",
            "Edge cases tested"
        ],
        "labels": ["green"]
    }
]

for card_data in phase3_cards:
    card = create_card(
        created_lists["PHASE 3: Software Development (COMPLETED)"],
        card_data["name"],
        card_data["desc"],
        None,
        card_data.get("labels", ["green"])
    )
    if "checklist" in card_data:
        create_checklist(card["id"], "Tasks", card_data["checklist"])
    print(f"  Created: {card_data['name']}")

# ========================================
# SPRINT 4: HARDWARE SETUP (IN PROGRESS)
# ========================================
print("\nCreating Sprint 4: Hardware Setup (IN PROGRESS)...")

hardware_cards = [
    {
        "name": "SPRINT 4: Hardware Setup",
        "desc": """**Status:** IN PROGRESS

**Overview:**
Setting up physical hardware components including Raspberry Pi, display, camera, and network connectivity.

**Tasks Remaining:**
- Set up Raspberry Pi
- Mount monitor and camera
- Test basic connections
- Ensure network connectivity""",
        "labels": ["yellow"]
    },
    {
        "name": "Set up Raspberry Pi",
        "desc": """**Status:** NOT COMPLETED

**Tasks:**
- Install Raspberry Pi OS
- Configure system settings
- Install required libraries
- Set up virtual environment
- Configure auto-start for AI assistant""",
        "checklist": [
            "Install Raspberry Pi OS",
            "Update system packages",
            "Install Python 3.10+",
            "Install OpenCV and face_recognition",
            "Install audio libraries",
            "Set up virtual environment",
            "Configure auto-start service"
        ],
        "labels": ["yellow"]
    },
    {
        "name": "Mount Monitor and Camera",
        "desc": """**Status:** NOT COMPLETED

**Tasks:**
- Mount display panel on mirror frame
- Install USB camera at optimal angle
- Set up microphone and speaker system
- Cable management
- Test physical setup stability""",
        "checklist": [
            "Mount display panel securely",
            "Position camera at eye level",
            "Install microphone",
            "Connect speakers/audio output",
            "Organize cables neatly",
            "Test physical stability"
        ],
        "labels": ["yellow"]
    },
    {
        "name": "Test Basic Connections",
        "desc": """**Status:** NOT COMPLETED

**Tasks:**
- Test display output
- Verify camera feed capture
- Test microphone input
- Test speaker output
- Verify all connections""",
        "checklist": [
            "Display shows output correctly",
            "Camera captures clear video feed",
            "Microphone records audio properly",
            "Speakers produce clear sound",
            "Test at different lighting conditions",
            "Verify power supply stability"
        ],
        "labels": ["yellow"]
    },
    {
        "name": "Ensure Network Connectivity",
        "desc": """**Status:** NOT COMPLETED

**Tasks:**
- Configure WiFi/Ethernet connection
- Test internet connectivity
- Set up static IP (optional)
- Configure firewall rules
- Test API connectivity""",
        "checklist": [
            "Connect to WiFi/Ethernet",
            "Test internet speed",
            "Configure static IP address",
            "Open required ports in firewall",
            "Test Calendar API connection",
            "Test Email API connection",
            "Test Weather API connection",
            "Verify LLM local processing works"
        ],
        "labels": ["yellow"]
    }
]

for card_data in hardware_cards:
    card = create_card(
        created_lists["SPRINT 4: Hardware Setup (IN PROGRESS)"],
        card_data["name"],
        card_data["desc"],
        None,
        card_data.get("labels", ["yellow"])
    )
    if "checklist" in card_data:
        create_checklist(card["id"], "Tasks", card_data["checklist"])
    print(f"  Created: {card_data['name']}")

# ========================================
# SPRINT 5: VOICE SCHEDULING (NOT STARTED)
# ========================================
print("\nCreating Sprint 5: Voice Scheduling (NOT STARTED)...")

scheduling_cards = [
    {
        "name": "SPRINT 5: Voice-Controlled Scheduling",
        "desc": """**Status:** NOT STARTED

**Overview:**
Develop voice-controlled calendar integration for managing schedule via voice commands.

**Tasks:**
- Integrate Calendar API
- Develop NLP for scheduling
- Test voice-based event management
- Collect feedback on accuracy""",
        "labels": ["purple"]
    },
    {
        "name": "Integrate Calendar API",
        "desc": """**Status:** NOT COMPLETED

**Tasks:**
- Set up Google Calendar API authentication
- Implement OAuth2 flow
- Create calendar data retrieval functions
- Test event fetching and parsing""",
        "checklist": [
            "Set up Google Calendar API credentials",
            "Implement OAuth2 authentication",
            "Create calendar service connection",
            "Test event retrieval",
            "Parse calendar data"
        ],
        "labels": ["purple"]
    },
    {
        "name": "Develop NLP for Scheduling",
        "desc": """**Status:** NOT COMPLETED

**Tasks:**
- Implement voice command recognition
- Parse natural language date/time
- Extract event details
- Handle various command formats
- Implement confirmation dialogue""",
        "checklist": [
            "Implement speech-to-text for commands",
            "Parse date/time from natural language",
            "Extract event title and details",
            "Handle different command variations",
            "Implement voice confirmation",
            "Handle scheduling conflicts"
        ],
        "labels": ["purple"]
    },
    {
        "name": "Test Voice-Based Event Management",
        "desc": """**Status:** NOT COMPLETED

**Tasks:**
- Test creating new events via voice
- Test updating existing events
- Test deleting events
- Test querying schedule
- Verify event accuracy""",
        "checklist": [
            "Test: Schedule meeting",
            "Test: What's on calendar",
            "Test: Reschedule event",
            "Test: Cancel meeting",
            "Verify events in Google Calendar",
            "Test edge cases"
        ],
        "labels": ["purple"]
    },
    {
        "name": "Collect Feedback on Scheduling Accuracy",
        "desc": """**Status:** NOT COMPLETED

**Tasks:**
- Test with multiple users
- Document accuracy rate
- Identify common errors
- Collect user experience feedback
- Create improvement backlog""",
        "checklist": [
            "Conduct user testing",
            "Measure accuracy rate",
            "Document error patterns",
            "Collect feedback",
            "Create improvement list"
        ],
        "labels": ["purple"]
    }
]

for card_data in scheduling_cards:
    card = create_card(
        created_lists["SPRINT 5: Voice Scheduling (NOT STARTED)"],
        card_data["name"],
        card_data["desc"],
        None,
        card_data.get("labels", ["purple"])
    )
    if "checklist" in card_data:
        create_checklist(card["id"], "Tasks", card_data["checklist"])
    print(f"  Created: {card_data['name']}")

# ========================================
# SPRINT 6: EMAIL ASSISTANT (NOT STARTED)
# ========================================
print("\nCreating Sprint 6: Email Assistant (NOT STARTED)...")

email_cards = [
    {
        "name": "SPRINT 6: Intelligent Email Assistant",
        "desc": """**Status:** NOT STARTED

**Overview:**
Develop intelligent email assistant with voice dictation and LLM-powered summarization.

**Tasks:**
- Integrate Email API with LLM
- Develop voice dictation system
- Test email drafting and summarization
- Ensure local processing for privacy""",
        "labels": ["pink"]
    },
    {
        "name": "Integrate Email API with LLM",
        "desc": """**Status:** NOT COMPLETED

**Tasks:**
- Set up Gmail API authentication
- Implement email fetching
- Connect local LLM for processing
- Create email summarization pipeline
- Test email data retrieval""",
        "checklist": [
            "Set up Gmail API credentials",
            "Implement OAuth2 for Gmail",
            "Fetch emails",
            "Parse email content",
            "Connect to local LLM",
            "Create summarization prompts",
            "Test email retrieval"
        ],
        "labels": ["pink"]
    },
    {
        "name": "Develop Voice Dictation System",
        "desc": """**Status:** NOT COMPLETED

**Tasks:**
- Implement continuous voice recording
- Convert speech to text for emails
- Handle punctuation commands
- Implement editing commands
- Create email composition interface
- Add voice confirmation step""",
        "checklist": [
            "Implement continuous speech recognition",
            "Convert speech to text accurately",
            "Handle punctuation commands",
            "Implement editing commands",
            "Create composition flow",
            "Add confirmation before sending"
        ],
        "labels": ["pink"]
    },
    {
        "name": "Test Email Drafting and Summarization",
        "desc": """**Status:** NOT COMPLETED

**Tasks:**
- Test voice email composition
- Test email summarization accuracy
- Test priority email identification
- Verify email formatting
- Test sending emails via voice""",
        "checklist": [
            "Test: Draft email",
            "Test: Summarize unread emails",
            "Test: Identify priority emails",
            "Test: Send email",
            "Verify email formatting",
            "Test different email lengths",
            "Verify LLM summaries"
        ],
        "labels": ["pink"]
    },
    {
        "name": "Ensure Local Processing for Privacy",
        "desc": """**Status:** NOT COMPLETED

**Tasks:**
- Verify all LLM processing is local
- Test offline functionality
- Ensure no email data sent to cloud
- Document privacy measures
- Create privacy settings interface""",
        "checklist": [
            "Confirm LLM runs locally",
            "Test with internet disconnected",
            "Verify email content stays local",
            "Document data handling",
            "Add user privacy controls",
            "Create privacy policy"
        ],
        "labels": ["pink"]
    }
]

for card_data in email_cards:
    card = create_card(
        created_lists["SPRINT 6: Email Assistant (NOT STARTED)"],
        card_data["name"],
        card_data["desc"],
        None,
        card_data.get("labels", ["pink"])
    )
    if "checklist" in card_data:
        create_checklist(card["id"], "Tasks", card_data["checklist"])
    print(f"  Created: {card_data['name']}")

# ========================================
# PHASE 4: TESTING (NOT STARTED)
# ========================================
print("\nCreating Phase 4: Testing (NOT STARTED)...")

testing_cards = [
    {
        "name": "PHASE 4: CONTINUOUS TESTING",
        "desc": """**Status:** NOT STARTED

**Overview:**
Comprehensive testing of all system components including unit tests, integration tests, user feedback, and bug fixes.

**Tasks:**
- Unit testing
- Integration testing
- User feedback testing
- Bug fixes and refinements""",
        "labels": ["red"]
    },
    {
        "name": "Unit Testing",
        "desc": """**Status:** NOT COMPLETED

**Components to Test:**
- Facial recognition accuracy
- Voice interaction responsiveness
- Email assistant functionality
- Scheduling commands
- News/briefing data interface""",
        "checklist": [
            "Test facial recognition accuracy",
            "Test voice response time",
            "Test email operations",
            "Test scheduling commands",
            "Test morning briefing delivery",
            "Document test results",
            "Create bug reports"
        ],
        "labels": ["red"]
    },
    {
        "name": "Integration Testing",
        "desc": """**Status:** NOT COMPLETED

**Integration Points:**
- Camera with facial recognition
- Face detection triggering briefings
- Voice commands with calendar/email
- LLM integration with email/chat""",
        "checklist": [
            "Test: Face detected to system activation",
            "Test: Recognized face to briefing",
            "Test: Voice command to calendar update",
            "Test: Voice command to email sent",
            "Test: LLM to email summarization",
            "Test: All APIs working together",
            "Verify data flow between modules"
        ],
        "labels": ["red"]
    },
    {
        "name": "User Feedback Testing",
        "desc": """**Status:** NOT COMPLETED

**Tasks:**
- Recruit test users
- Conduct usability testing sessions
- Record user interactions
- Collect feedback questionnaire
- Document user pain points
- Identify improvement areas""",
        "checklist": [
            "Prepare test scenarios",
            "Recruit test participants",
            "Conduct testing sessions",
            "Record user feedback",
            "Analyze usability issues",
            "Prioritize improvements"
        ],
        "labels": ["red"]
    },
    {
        "name": "Bug Fixes and Refinements",
        "desc": """**Status:** NOT COMPLETED

**Tasks:**
- Fix critical bugs
- Improve UI/UX based on feedback
- Optimize performance issues
- Refine voice recognition accuracy
- Polish user experience""",
        "checklist": [
            "Fix all critical bugs",
            "Fix high-priority bugs",
            "Improve response time",
            "Enhance voice recognition",
            "Refine UI animations",
            "Test all fixes"
        ],
        "labels": ["red"]
    }
]

for card_data in testing_cards:
    card = create_card(
        created_lists["PHASE 4: Testing (NOT STARTED)"],
        card_data["name"],
        card_data["desc"],
        None,
        card_data.get("labels", ["red"])
    )
    if "checklist" in card_data:
        create_checklist(card["id"], "Tasks", card_data["checklist"])
    print(f"  Created: {card_data['name']}")

# ========================================
# PHASE 5: DOCUMENTATION (NOT STARTED)
# ========================================
print("\nCreating Phase 5: Documentation (NOT STARTED)...")

documentation_cards = [
    {
        "name": "PHASE 5: DOCUMENTATION AND HANDOVER",
        "desc": """**Status:** NOT STARTED

**Overview:**
Complete all project documentation including project report, user manual, and future enhancements.

**Tasks:**
- Project report writing
- Future enhancements documentation
- User manual creation
- Feature guide and FAQ documentation""",
        "labels": ["green"]
    },
    {
        "name": "Project Report Writing",
        "desc": """**Status:** NOT COMPLETED

**Sections to Complete:**
1. Executive Summary
2. Introduction & Background
3. Literature Review
4. Methodology
5. System Design & Architecture
6. Implementation Details
7. Testing & Results
8. Conclusion
9. References""",
        "checklist": [
            "Write Executive Summary",
            "Write Introduction",
            "Complete Literature Review",
            "Document Methodology",
            "Detail System Architecture",
            "Explain Implementation",
            "Present Testing Results",
            "Write Conclusion",
            "Compile References",
            "Proofread entire document"
        ],
        "labels": ["green"]
    },
    {
        "name": "Future Enhancements Documentation",
        "desc": """**Status:** NOT COMPLETED

**Content:**
- Potential new features
- Scalability improvements
- Hardware upgrade paths
- Additional AI capabilities
- Integration possibilities""",
        "checklist": [
            "Document potential features",
            "Identify scalability improvements",
            "Suggest hardware upgrades",
            "List additional AI capabilities",
            "Explore integration opportunities",
            "Create roadmap diagram"
        ],
        "labels": ["green"]
    },
    {
        "name": "User Manual Creation",
        "desc": """**Status:** NOT COMPLETED

**Sections:**
1. Getting Started
2. Hardware Setup
3. Software Installation
4. User Authentication
5. Using Voice Commands
6. Managing Schedule
7. Email Features
8. Troubleshooting
9. FAQ""",
        "checklist": [
            "Write Getting Started guide",
            "Document Hardware Setup",
            "Create Software Installation guide",
            "Explain User Authentication",
            "List all Voice Commands",
            "Document Scheduling features",
            "Explain Email Assistant usage",
            "Create Troubleshooting section",
            "Compile FAQ"
        ],
        "labels": ["green"]
    },
    {
        "name": "Feature Guide & FAQ Documentation",
        "desc": """**Status:** NOT COMPLETED

**Content:**
- Detailed feature walkthroughs
- Step-by-step tutorials
- Common use cases
- Tips & tricks
- FAQ compilation""",
        "checklist": [
            "Create feature walkthroughs",
            "Write step-by-step tutorials",
            "Document common use cases",
            "Add tips & tricks section",
            "Compile comprehensive FAQ",
            "Create quick reference guide"
        ],
        "labels": ["green"]
    }
]

for card_data in documentation_cards:
    card = create_card(
        created_lists["PHASE 5: Documentation (NOT STARTED)"],
        card_data["name"],
        card_data["desc"],
        None,
        card_data.get("labels", ["green"])
    )
    if "checklist" in card_data:
        create_checklist(card["id"], "Tasks", card_data["checklist"])
    print(f"  Created: {card_data['name']}")

# ========================================
# MILESTONES
# ========================================
print("\nCreating Milestones cards...")

milestones_cards = [
    {
        "name": "M1: Requirements Complete",
        "desc": """**Status:** COMPLETED

**Completion Criteria:**
- All requirements identified
- User needs analysis completed
- Product backlog created
- Sprint planning finished

**Deliverable:** Requirements documentation""",
        "labels": ["green"]
    },
    {
        "name": "M2: Design Complete",
        "desc": """**Status:** COMPLETED

**Completion Criteria:**
- System architecture defined
- All modules designed
- Prototypes created
- Technical diagrams completed

**Deliverable:** Design documentation""",
        "labels": ["green"]
    },
    {
        "name": "M3: Facial Recognition Complete",
        "desc": """**Status:** COMPLETED

**Completion Criteria:**
- Multi-user recognition working
- Face authentication integrated
- User differentiation tested
- Privacy controls implemented

**Deliverable:** Facial recognition module""",
        "labels": ["green"]
    },
    {
        "name": "M4: Briefings Complete",
        "desc": """**Status:** COMPLETED

**Completion Criteria:**
- APIs integrated
- Personalized briefings working
- News feeds integrated
- Auto-delivery tested

**Deliverable:** Morning briefing system""",
        "labels": ["green"]
    },
    {
        "name": "M5: AI Communication Ready",
        "desc": """**Status:** COMPLETED

**Completion Criteria:**
- Voice interaction working
- Local LLM integrated
- Natural language processing tested
- Conversational context maintained

**Deliverable:** AI communication module""",
        "labels": ["green"]
    },
    {
        "name": "M6: Hardware Ready",
        "desc": """**Status:** IN PROGRESS

**Completion Criteria:**
- Raspberry Pi configured
- Hardware mounted
- Connections tested
- Network verified

**Deliverable:** Operational hardware platform""",
        "labels": ["yellow"]
    },
    {
        "name": "M7: Scheduling Ready",
        "desc": """**Status:** NOT STARTED

**Completion Criteria:**
- Calendar API integrated
- Voice scheduling working
- Event management functional
- User feedback collected

**Deliverable:** Voice-controlled scheduling""",
        "labels": ["purple"]
    },
    {
        "name": "M8: Email Assistant Complete",
        "desc": """**Status:** NOT STARTED

**Completion Criteria:**
- Email API with LLM integrated
- Voice dictation working
- Email summarization functional
- Privacy measures implemented

**Deliverable:** Intelligent email assistant""",
        "labels": ["pink"]
    },
    {
        "name": "M9: Testing Complete",
        "desc": """**Status:** NOT STARTED

**Completion Criteria:**
- All unit tests passed
- Integration testing successful
- User feedback collected
- Critical bugs fixed

**Deliverable:** Fully tested system""",
        "labels": ["red"]
    },
    {
        "name": "M10: Documentation Complete",
        "desc": """**Status:** NOT STARTED

**Completion Criteria:**
- Project report completed
- Future enhancements documented
- User manual created
- Feature guide ready

**Deliverable:** Complete documentation""",
        "labels": ["green"]
    },
    {
        "name": "M11: PROJECT COMPLETE",
        "desc": """**Status:** NOT STARTED

**Final Deliverables:**
- Fully functional AI Mirror system
- Complete documentation package
- User manual
- Project report
- Source code repository

**Outcome:** FYP Successfully Completed""",
        "labels": ["orange"]
    }
]

for card_data in milestones_cards:
    card = create_card(
        created_lists["MILESTONES"],
        card_data["name"],
        card_data["desc"],
        None,
        card_data.get("labels")
    )
    print(f"  Created: {card_data['name']}")

print("\n" + "=" * 60)
print("TRELLO BOARD SETUP COMPLETE!")
print("=" * 60)
print(f"\nTotal Cards Created: ~80 cards")
print(f"Total Lists: {len(lists_structure)}")
print(f"\nView your board: https://trello.com/b/{BOARD_ID}")
print("\nYour AMMS FYP Trello board is now professionally organized!")
print("\nCompletion Status:")
print("  COMPLETED: Phase 1, Phase 2, Phase 3 (Sprints 1-3)")
print("  IN PROGRESS: Sprint 4 (Hardware Setup)")
print("  NOT STARTED: Sprints 5-6, Testing, Documentation")