window.SMART_MIRROR_CONFIG = {
  user: {
    defaultName: "there",
    recognizedName: "Pranav",
    // Toggle this flag when face recognition provides a verified identity.
    isRecognized: true,
    nextEvent: {
      time: "09:00",
      label: "Product kickoff sync"
    }
  },
  intro: {
    // Messages appear sequentially during the intro sequence.
    messages: [
      {
        text: "Welcome to your Smart Mirror Assistant",
        duration: 2600
      },
      {
        text: "I'm here to help you manage your tasks, meetings, and emails.",
        duration: 4000
      },
      {
        text: "Let me know how I can assist you today!",
        duration: 3200
      }
    ],
    // Optional personalized line appended when a user is recognized.
    personalizedTemplate: "Good morning, {{name}}! You have a meeting at {{time}}.",
    fadeOutDelay: 1000,
    idleDelay: 8000
  },
  mainScreen: {
    schedule: [
      {
        time: "09:00",
        title: "Product kickoff sync",
        location: "Conference Room B"
      },
      {
        time: "11:30",
        title: "Design review",
        location: "Zoom"
      },
      {
        time: "14:00",
        title: "1:1 with Sarah",
        location: "Office"
      }
    ],
    reminders: [
      "Draft follow-up email to marketing team",
      "Share daily status update by 5 PM"
    ],
    idleMessages: [
      "You have a meeting at 2 PM. Would you like to see details?",
      "Need a quick summary of your emails? Just ask.",
      "Remember to take a short break and stretch."
    ]
  },
  tts: {
    enabled: true,
    // Speech synthesis voice hint; browsers may ignore unfamiliar names.
    preferredVoice: "en-US",
    introLines: [
      "Good morning, {{name}}! Welcome to your Smart Mirror Assistant.",
      "I'm here to help you manage your day. Ask me about your schedule, emails, and tasks.",
      "How can I assist you today?"
    ],
    ambientAudioUrl: ""
  }
};
