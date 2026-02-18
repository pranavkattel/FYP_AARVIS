(function () {
  const config = window.SMART_MIRROR_CONFIG || {};

  const introContainer = document.getElementById("intro");
  const introTextEl = document.getElementById("introText");
  const introDotsEl = document.getElementById("introDots");
  const mainScreen = document.getElementById("mainScreen");
  const scheduleList = document.getElementById("scheduleList");
  const reminderList = document.getElementById("reminderList");
  const statusPanel = document.getElementById("statusPanel");
  const idleMessageEl = document.getElementById("idleMessage");

  const introConfig = config.intro || {};
  const mainConfig = config.mainScreen || {};
  const ttsConfig = config.tts || {};
  const userConfig = config.user || {};

  let idleTimer = null;
  let idleInterval = null;

  document.addEventListener("DOMContentLoaded", () => {
    populateMainScreen();
    startIntroSequence();
  });

  function populateMainScreen() {
    renderSchedule(mainConfig.schedule || []);
    renderReminders(mainConfig.reminders || []);
    renderStatus();
  }

  function renderSchedule(entries) {
    scheduleList.innerHTML = "";
    entries.forEach((item) => {
      const li = document.createElement("li");
      li.className = "schedule-item";

      li.innerHTML = `
        <div class="schedule-item__time">${item.time || "--:--"}</div>
        <div class="schedule-item__details">
          <p class="schedule-item__title">${item.title || "Event"}</p>
          <p class="schedule-item__location">${item.location || ""}</p>
        </div>
      `;

      scheduleList.appendChild(li);
    });
  }

  function renderReminders(reminders) {
    reminderList.innerHTML = "";
    reminders.forEach((reminder) => {
      const li = document.createElement("li");
      li.textContent = reminder;
      reminderList.appendChild(li);
    });
  }

  function renderStatus() {
    statusPanel.innerHTML = "";

    const name = userConfig.isRecognized ? userConfig.recognizedName : userConfig.defaultName;
    const nextEvent = userConfig.nextEvent;

    const lines = [];
    if (name) {
      lines.push(`Good morning, ${name}.`);
    }
    if (nextEvent && nextEvent.time && nextEvent.label) {
      lines.push(`Next up at ${nextEvent.time}: ${nextEvent.label}.`);
    } else {
      lines.push("No upcoming events right now.");
    }

    lines.forEach((line) => {
      const p = document.createElement("p");
      p.className = "status-panel__line";
      p.textContent = line;
      statusPanel.appendChild(p);
    });
  }

  async function startIntroSequence() {
    const activeName = userConfig.isRecognized ? userConfig.recognizedName : userConfig.defaultName;
    const sequence = buildIntroSequence(activeName);

    if (ttsConfig.enabled) {
      speakIntro(activeName);
      playAmbientAudio();
    }

    introDotsEl.classList.add("show");

    for (const step of sequence) {
      await displayMessage(step.text, step.duration);
    }

    introDotsEl.classList.remove("show");

    await wait(introConfig.fadeOutDelay || 1000);
    finishIntro();
  }

  function buildIntroSequence(activeName) {
    const baseMessages = Array.isArray(introConfig.messages) ? introConfig.messages : [];
    const personalizedLine = createPersonalizedLine(activeName);

    const merged = baseMessages.map(({ text, duration }) => ({
      text: fillTemplate(text, {
        name: activeName,
        time: userConfig.nextEvent && userConfig.nextEvent.time,
      }),
      duration: Math.max(duration || 2500, 1600),
    }));

    if (personalizedLine) {
      merged.splice(1, 0, {
        text: personalizedLine,
        duration: 3200,
      });
    }

    return merged;
  }

  function createPersonalizedLine(name) {
    if (!userConfig.isRecognized || !introConfig.personalizedTemplate) {
      return "";
    }

    return fillTemplate(introConfig.personalizedTemplate, {
      name,
      time: userConfig.nextEvent && userConfig.nextEvent.time,
    });
  }

  function displayMessage(text, duration) {
    return new Promise((resolve) => {
      introTextEl.textContent = text;
      introTextEl.classList.remove("fade-out");

      // Force reflow so the fade-in animation retriggers for each line.
      void introTextEl.offsetWidth;

      introTextEl.classList.add("fade-in");

      const fadeOutTimeout = setTimeout(() => {
        introTextEl.classList.remove("fade-in");
        introTextEl.classList.add("fade-out");
      }, Math.max(duration - 900, 600));

      setTimeout(() => {
        clearTimeout(fadeOutTimeout);
        introTextEl.classList.remove("fade-in");
        introTextEl.classList.add("fade-out");
        resolve();
      }, duration);
    });
  }

  function finishIntro() {
    introContainer.classList.add("completed");

    setTimeout(() => {
      mainScreen.classList.remove("hidden");
      requestAnimationFrame(() => {
        mainScreen.classList.add("show");
      });
      scheduleIdleMessages();
    }, 700);
  }

  function scheduleIdleMessages() {
    clearTimeout(idleTimer);
    clearInterval(idleInterval);

    const idleDelay = introConfig.idleDelay || 8000;
    idleTimer = setTimeout(() => {
      rotateIdleMessage();
      idleInterval = setInterval(rotateIdleMessage, idleDelay);
    }, idleDelay);
  }

  function rotateIdleMessage() {
    if (!Array.isArray(mainConfig.idleMessages) || !mainConfig.idleMessages.length) {
      return;
    }

    const message = pickRandom(mainConfig.idleMessages);
    idleMessageEl.textContent = message;
    idleMessageEl.classList.add("show");

    setTimeout(() => {
      idleMessageEl.classList.remove("show");
    }, 3800);
  }

  function speakIntro(activeName) {
    if (!("speechSynthesis" in window)) {
      console.warn("Speech Synthesis API is not supported in this browser.");
      return;
    }

    const lines = (ttsConfig.introLines || []).map((line) =>
      fillTemplate(line, {
        name: activeName,
        time: userConfig.nextEvent && userConfig.nextEvent.time,
      })
    );

    const utterance = new SpeechSynthesisUtterance(lines.join(" \n"));
    utterance.rate = 1;
    utterance.pitch = 1;

    if (ttsConfig.preferredVoice) {
      const voices = window.speechSynthesis.getVoices();
      const matchingVoice = voices.find((voice) =>
        voice.lang.startsWith(ttsConfig.preferredVoice)
      );
      if (matchingVoice) {
        utterance.voice = matchingVoice;
      }
    }

    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
  }

  function playAmbientAudio() {
    if (!ttsConfig.ambientAudioUrl) {
      return;
    }

    const ambientAudio = document.getElementById("ambientAudio");
    if (!ambientAudio) {
      return;
    }

    ambientAudio.src = ttsConfig.ambientAudioUrl;
    ambientAudio.loop = true;
    ambientAudio.volume = 0.3;
    const playPromise = ambientAudio.play();
    if (playPromise && typeof playPromise.catch === "function") {
      playPromise.catch(() => {
        console.warn("Ambient audio playback was blocked by the browser.");
      });
    }
  }

  function fillTemplate(template, data) {
    if (!template) {
      return "";
    }
    return template.replace(/{{(\w+)}}/g, (_, key) => data[key] || "");
  }

  function pickRandom(collection) {
    return collection[Math.floor(Math.random() * collection.length)];
  }

  function wait(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
})();
