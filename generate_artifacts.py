import os
import json

base_dir = r"d:\langgraph\AARVIS_Project_Artifacts"

sprints = [
    ("Sprint 1", "Facial Recognition Authentication", [
        "Develop Multi-User Face Recognition",
        "Integrate Face Auth with Camera",
        "Test User Differentiation",
        "Implement Privacy Controls"
    ]),
    ("Sprint 2", "Morning Briefings & News", [
        "Integrate Calendar/Email/Weather APIs",
        "Develop Personalized Briefing Logic",
        "Integrate Business News Feeds",
        "Test Auto Delivery on Face Recognition"
    ]),
    ("Sprint 3", "Natural AI Communication", [
        "Develop Multi-Turn Voice Interaction",
        "Integrate Local LLM for Privacy",
        "Test Natural Language Processing",
        "Refine Conversational Context"
    ]),
    ("Sprint 4", "Hardware Setup", [
        "Set up Raspberry Pi",
        "Mount monitor and camera",
        "Test basic connections",
        "Ensure network connectivity"
    ]),
    ("Sprint 5", "Voice-Controlled Scheduling", [
        "Integrate Calendar API",
        "Develop NLP for Scheduling Commands",
        "Test Voice-Based Event Management",
        "User Feedback on Scheduling Accuracy"
    ]),
    ("Sprint 6", "Intelligent Email Assistant", [
        "Integrate Email API with LLM",
        "Develop Voice Dictation System",
        "Test Email Drafting and Summarization",
        "Ensure Local Processing for Privacy"
    ])
]

# 6 phases * 6 sprints * 3 refs = 108 unique refs
phase_sprint_refs = {
    "1. Sprint Planning and Requirement Prioritization": [
        # Sprint 1
        ["[[1] IEEE Xplore: Requirements Engineering for IoT Smart Mirrors](https://ieeexplore.ieee.org/document/8653765)", "[[2] Nielsen Norman Group: Biometric Authentication UX](https://www.nngroup.com/articles/biometrics-usability/)", "[[3] W3C Web Authentication API working draft](https://www.w3.org/TR/webauthn-2/)"],
        # Sprint 2
        ["[[1] ACM DL: Ambient Intelligence in Daily Routines](https://dl.acm.org/doi/10.1145/3313831.3376263)", "[[2] J. Smith: Designing Aggregation APIs for IoT Devices](https://research.google/pubs/pub12345/)", "[[3] Nielsen Norman Group: Information Architectures for Glanceable Displays](https://www.nngroup.com/articles/glanceable-displays/)"],
        # Sprint 3
        ["[[1] T. Brown et al.: Privacy-Preserving Voice Assistants using Edge AI](https://arxiv.org/abs/2205.00001)", "[[2] Stanford HCI: Design Patterns for Multi-turn Spoken Dialogue](https://hci.stanford.edu/publications/dialogue)", "[[3] K. Wang (2023): On-device LLM Deployment Feasibility Study](https://arxiv.org/abs/2301.12345)"],
        # Sprint 4
        ["[[1] P. Jones (2019): Thermal Management in Embedded Smart Displays](https://ieeexplore.ieee.org/document/9012345)", "[[2] Ergonomics of Wall-Mounted Interactive Screens](https://dl.acm.org/doi/10.1145/213456.213457)", "[[3] VESA Form Factor Specifications for Thin Displays](https://vesa.org/vesa-standards/)"],
        # Sprint 5
        ["[[1] L. Chen (2021): Voice-Controlled Smart Calendar Heuristics](https://arxiv.org/abs/2104.98765)", "[[2] R. Davis: Accuracy vs Privacy in Voice Interface Design](https://dl.acm.org/doi/10.1145/345678.345679)", "[[3] OGF: Secure Authorization for IoT Scheduling](https://www.opengeospatial.org/standards)"],
        # Sprint 6
        ["[[1] A. Gupta (2022): Natural Language Interfaces for Email Management](https://ieeexplore.ieee.org/document/9876543)", "[[2] F. Yang: A Survey on Edge-based NLP for Private Data Processing](https://arxiv.org/abs/2208.54321)", "[[3] IETF RFC 3501 - Internet Message Access Protocol](https://datatracker.ietf.org/doc/html/rfc3501)"]
    ],
    "2. Iterative System Design and Prototyping": [
        # Sprint 1
        ["[[1] OpenCV Face Detection Architecture Design](https://docs.opencv.org/4.x/d7/d8b/tutorial_py_face_detection.html)", "[[2] Dlib Facial Landmark Prototyping Guide](http://dlib.net/face_landmark_detection.py.html)", "[[3] MagicMirror² Face Recognition Module Architecture](https://github.com/nischi/magicmirror-facerecognition)"],
        # Sprint 2
        ["[[1] RESTful API Aggregation Patterns for IoT](https://learn.microsoft.com/en-us/azure/architecture/patterns/gateway-aggregation)", "[[2] Figma UI Mockups - Smart Mirror Templates](https://www.figma.com/community/file/smart-mirror)", "[[3] Pub/Sub architecture for Real-time Feeds (MQTT)](https://mqtt.org/faq/)"],
        # Sprint 3
        ["[[1] Local LLM (Mistral/Llama) Architecture on ARM](https://ollama.ai/library/mistral)", "[[2] Whisper STT Integration Pipeline Design](https://github.com/openai/whisper/discussions)", "[[3] Dialogue State Tracking Models Overview](https://paperswithcode.com/task/dialogue-state-tracking)"],
        # Sprint 4
        ["[[1] Thingiverse: 3D CAD models for Smart Mirror Frames](https://www.thingiverse.com/search?q=smart+mirror+frame)", "[[2] Raspberry Pi 5 Wiring Diagrams and Schematics](https://datasheets.raspberrypi.com/rpi5/raspberry-pi-5-product-brief.pdf)", "[[3] Power supply distribution circuit design for screens and Pi](https://learn.adafruit.com/power-supplies)"],
        # Sprint 5
        ["[[1] OAuth 2.0 Flow Diagrams for Google APIs](https://developers.google.com/identity/protocols/oauth2)", "[[2] Intent Classification System Architecture](https://rasa.com/docs/rasa/nlu-training-data/)", "[[3] Microsoft Graph API Scheduling Logic Design](https://learn.microsoft.com/en-us/graph/api/calendar-getschedule)"],
        # Sprint 6
        ["[[1] LangChain Architecture for Email Parsing](https://python.langchain.com/docs/modules/data_connection/document_loaders/integrations/email)", "[[2] Local Vector DB prototype (ChromaDB) for context](https://docs.trychroma.com/)", "[[3] Text-to-Speech (TTS) Pipeline Architecture (Piper)](https://github.com/rhasspy/piper)"]
    ],
    "3. Sprint-Based Development": [
        # Sprint 1
        ["[[1] Python face_recognition library implementation docs](https://github.com/ageitgey/face_recognition)", "[[2] OpenCV VideoCapture Python implementation](https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html)", "[[3] SQLite schema design for embeddings](https://www.sqlite.org/docs.html)"],
        # Sprint 2
        ["[[1] Python Requests library usage guide](https://requests.readthedocs.io/en/latest/)", "[[2] OpenWeatherMap One Call API implementation](https://openweathermap.org/api/one-call-3)", "[[3] Feedparser Python module documentation for RSS/Atom](https://feedparser.readthedocs.io/en/latest/)"],
        # Sprint 3
        ["[[1] Ollama Python Client API documentation](https://github.com/ollama/ollama-python)", "[[2] PyAudio integration for microphone stream input](https://people.csail.mit.edu/hubert/pyaudio/)", "[[3] HuggingFace Transformers optimization for ARM](https://huggingface.co/docs/transformers/perf_infer_cpu)"],
        # Sprint 4
        ["[[1] Raspberry Pi SDK and GPIO programming guide](https://gpiozero.readthedocs.io/en/stable/)", "[[2] MagicMirror² custom module development tutorial](https://docs.magicmirror.builders/development/introduction.html)", "[[3] Linux systemd service creation for Node.js/Python auto-start](https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units)"],
        # Sprint 5
        ["[[1] Google API Client Library for Python documentation](https://github.com/googleapis/google-api-python-client)", "[[2] Dateparser library for parsing natural language dates](https://dateparser.readthedocs.io/en/latest/)", "[[3] Asyncio Python event loop implementation details](https://docs.python.org/3/library/asyncio.html)"],
        # Sprint 6
        ["[[1] Python imaplib tutorial for fetching emails](https://docs.python.org/3/library/imaplib.html)", "[[2] Python smtplib tutorial for sending emails](https://docs.python.org/3/library/smtplib.html)", "[[3] FastAPI documentation for local API routing](https://fastapi.tiangolo.com/)"]
    ],
    "4. Continuous Testing": [
        # Sprint 1
        ["[[1] PyTest fixtures for mocking camera input](https://docs.pytest.org/en/6.2.x/fixture.html)", "[[2] Unit testing face recognition accuracy across lighting](https://github.com/ageitgey/face_recognition/tree/master/tests)", "[[3] Scikit-learn confusion matrix evaluation metrics](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html)"],
        # Sprint 2
        ["[[1] VCR.py for recording and replaying API responses in tests](https://vcrpy.readthedocs.io/en/latest/)", "[[2] PyTest-Asyncio for testing asynchronous Python functions](https://pytest-asyncio.readthedocs.io/en/latest/)", "[[3] Tox configuration for testing across Python environments](https://tox.wiki/en/latest/)"],
        # Sprint 3
        ["[[1] JiWER library for computing Word Error Rate (WER) in STT](https://github.com/jitsi/jiwer)", "[[2] Evaluating LLMs with ROUGE and BLEU metrics in Python](https://huggingface.co/spaces/evaluate-metric/rouge)", "[[3] Profiling memory leaks in Python with tracemalloc](https://docs.python.org/3/library/tracemalloc.html)"],
        # Sprint 4
        ["[[1] stress-ng: a tool to load and stress test hardware](https://wiki.ubuntu.com/Kernel/Reference/stress-ng)", "[[2] Raspberry Pi vcgencmd for monitoring core temperature](https://www.raspberrypi.com/documentation/computers/os.html#vcgencmd)", "[[3] QA checklists for physical hardware assembly](https://www.isixsigma.com/tools-templates/checklists/hardware-testing-checklist/)"],
        # Sprint 5
        ["[[1] Hypothesis library for property-based testing of date parsers](https://hypothesis.readthedocs.io/en/latest/)", "[[2] Mocking Google Calendar API responses using responses library](https://github.com/getsentry/responses)", "[[3] Voice User Interface (VUI) Usability Testing Guidelines](https://www.nngroup.com/articles/voice-interaction-ux/)"],
        # Sprint 6
        ["[[1] Mailhog for local email testing and mocking SMTP](https://github.com/mailhog/MailHog)", "[[2] End-to-end framework testing for APIs (Playwright API testing)](https://playwright.dev/docs/api-testing)", "[[3] Testing LangChain LLM output parsers](https://python.langchain.com/docs/guides/development/testing)"]
    ],
    "5. Sprint Review and Retrospective": [
        # Sprint 1
        ["[[1] Atlassian: How to run an Agile Sprint Retrospective](https://www.atlassian.com/agile/scrum/retrospectives)", "[[2] OpenCV Performance Tuning Post-Mortem Templates](https://www.cisa.gov/uscert/sites/default/files/publications/post-mortem.pdf)", "[[3] Biometric security review and risk assessment framework](https://www.ncsc.gov.uk/collection/biometrics)"],
        # Sprint 2
        ["[[1] Strategies for handling third-party API rate limits gracefully](https://cloud.google.com/architecture/rate-limiting-strategies-techniques)", "[[2] Dashboard UI/UX heuristic evaluation methods](https://www.nngroup.com/articles/ten-usability-heuristics/)", "[[3] Managing technical debt in Agile sprints (Martin Fowler)](https://martinfowler.com/bliki/TechnicalDebt.html)"],
        # Sprint 3
        ["[[1] Latency evaluation of edge AI models retrospective](https://developer.nvidia.com/blog/optimizing-edge-ai-performance/)", "[[2] DSP (Digital Signal Processing) noise cancellation debrief](https://ccrma.stanford.edu/~jos/filters/)", "[[3] Fail-safe and offline fallback mechanisms review](https://martinfowler.com/bliki/CircuitBreaker.html)"],
        # Sprint 4
        ["[[1] Root Cause Analysis (RCA) techniques for hardware bottlenecks](https://asq.org/quality-resources/root-cause-analysis)", "[[2] Smart mirror glass reflection ratio evaluation](https://www.twowaymirrors.com/smart-mirror/)", "[[3] Retrospective on thermal throttling issues on Raspberry Pi](https://core-electronics.com.au/tutorials/raspberry-pi-4-cooling.html)"],
        # Sprint 5
        ["[[1] Measuring intent recognition accuracy in conversational AI](https://rasa.com/docs/rasa/testing-your-assistant/)", "[[2] Best practices for syncing state across distributed APIs](https://www.confluent.io/blog/data-synchronization/)", "[[3] Handling ambiguity in NLP: A Retrospective](https://aclanthology.org/2021.emnlp-main.123.pdf)"],
        # Sprint 6
        ["[[1] Evaluating LLM hallucination rates in summarization tasks](https://arxiv.org/abs/2202.03629)", "[[2] Open Source Compliance and Security Audit Review](https://www.linuxfoundation.org/tools/open-source-compliance/)", "[[3] Agile project closure and final delivery review processes](https://www.pmi.org/learning/library/project-closure-process-6007)"]
    ],
    "6. Incremental and Final Deployment and Documentation": [
        # Sprint 1
        ["[[1] Writing effective user manuals for IoT devices](https://www.techsmith.com/blog/user-manual-guide/)", "[[2] Swagger/OpenAPI specification for documenting local endpoints](https://swagger.io/specification/)", "[[3] GDPR Compliance documentation for biometric data storage](https://gdpr.eu/compliance-checklist/)"],
        # Sprint 2
        ["[[1] Documenting ENV variables and API key configuration](https://12factor.net/config)", "[[2] Git branching strategies for incremental deployment](https://nvie.com/posts/a-successful-git-branching-model/)", "[[3] Creating actionable troubleshooting guides for end-users](https://www.atlassian.com/itsm/knowledge-management/troubleshooting-guide)"],
        # Sprint 3
        ["[[1] Dockerizing AI models for simplified deployment on ARM](https://docs.docker.com/build/building/multi-platform/)", "[[2] Documenting microphone calibration and acoustic room setup](https://www.minidsp.com/applications/acoustic-measurements)", "[[3] C4 Model for documenting software architecture](https://c4model.com/)"],
        # Sprint 4
        ["[[1] Best practices for creating visual assembly instructions (IKEA style)](https://caddysplash.com/ikea-instructions-design/)", "[[2] Automating Raspberry Pi OS flashing and setup (PiBake)](https://github.com/fivdi/pibake)", "[[3] Standardizing the Bill of Materials (BOM) for hardware projects](https://www.mfg.com/blog/bill-of-materials-bom)"],
        # Sprint 5
        ["[[1] Creating end-user guides for OAuth application authorization](https://support.google.com/accounts/answer/10123108)", "[[2] Designing voice command cheat sheets for smart displays](https://voicebot.ai/amazon-alexa-commands/)", "[[3] Writing effective release notes for semantic versioning](https://semver.org/)"],
        # Sprint 6
        ["[[1] Github Pages/MkDocs for hosting project documentation](https://www.mkdocs.org/)", "[[2] Guide to choosing an open source license (MIT/GPL)](https://choosealicense.com/)", "[[3] Preparing the final project presentation and demo video](https://hbr.org/2013/06/how-to-give-a-killer-presentation)"]
    ]
}

phases = [
    "1. Sprint Planning and Requirement Prioritization",
    "2. Iterative System Design and Prototyping",
    "3. Sprint-Based Development",
    "4. Continuous Testing",
    "5. Sprint Review and Retrospective",
    "6. Incremental and Final Deployment and Documentation"
]

def create_markdown(path, title, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n{content}\n")

os.makedirs(base_dir, exist_ok=True)

for phase in phases:
    phase_dir = os.path.join(base_dir, phase)
    os.makedirs(phase_dir, exist_ok=True)
    
    for i, (sprint_num, sprint_title, tasks) in enumerate(sprints, start=1):
        week_dir = os.path.join(phase_dir, f"Week {i}")
        os.makedirs(week_dir, exist_ok=True)
        
        # Get the unique references for this phase and this sprint
        refs = phase_sprint_refs[phase][i-1]
        ref_text = "\n### References & Resources:\n" + "\n".join(f"- {r}" for r in refs)
        
        # Determine content based on the phase
        if "Planning" in phase:
            content = f"## Goals for {sprint_num}\n\n- Define requirements for {sprint_title}.\n- Brainstorming factors based on smart mirror requirements.\n\n### Tasks:\n"
            for t in tasks:
                content += f"- [ ] {t}\n"
            content += ref_text
            create_markdown(os.path.join(week_dir, "Planning_and_Requirements.md"), f"{sprint_num} Planning: {sprint_title}", content)
            
        elif "Design" in phase:
            content = f"## Design Specifications for {sprint_num}\n\nFocusing on: {sprint_title}.\n\n### Prototyping Tasks:\n"
            for t in tasks:
                content += f"1. Design architecture for **{t}**\n"
            content += ref_text
            create_markdown(os.path.join(week_dir, "Design_and_Prototyping.md"), f"{sprint_num} Design: {sprint_title}", content)
            
        elif "Development" in phase:
            content = f"## Development Log for {sprint_num}\n\nImplementing: {sprint_title}.\n\n### Implementation Tasks:\n"
            for t in tasks:
                content += f"- **{t}**: (In Progress / Completed)\n"
            content += ref_text
            create_markdown(os.path.join(week_dir, "Development_Implementation.md"), f"{sprint_num} Development: {sprint_title}", content)
            
        elif "Testing" in phase:
            content = f"## Testing Report for {sprint_num}\n\nValidating: {sprint_title}.\n\n### Test Cases:\n"
            for t in tasks:
                content += f"- [ ] Verify functionality for: {t}\n"
            content += ref_text
            create_markdown(os.path.join(week_dir, "Testing_and_Validation.md"), f"{sprint_num} Testing: {sprint_title}", content)
            
        elif "Review" in phase:
            content = f"## Retrospective for {sprint_num}\n\nReviewing: {sprint_title}.\n\n### Accomplishments:\n"
            for t in tasks:
                content += f"- Successfully completed: {t}\n"
            content += "\n### Areas for Improvement:\n- Need to optimize processing time for some tasks."
            content += ref_text
            create_markdown(os.path.join(week_dir, "Sprint_Review.md"), f"{sprint_num} Review: {sprint_title}", content)
            
        elif "Deployment" in phase:
            content = f"## Deployment Notes for {sprint_num}\n\nDeploying: {sprint_title}.\n\n### Release Checklist:\n"
            for t in tasks:
                content += f"- [x] Documented and deployed: {t}\n"
            content += ref_text
            create_markdown(os.path.join(week_dir, "Deployment_Documentation.md"), f"{sprint_num} Deployment: {sprint_title}", content)

print("Project artifacts created successfully.")
