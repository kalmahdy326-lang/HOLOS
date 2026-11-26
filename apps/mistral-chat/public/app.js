const form = document.querySelector("#chat-form");
const input = document.querySelector("#prompt-input");
const sendButton = document.querySelector("#send-button");
const clearButton = document.querySelector("#clear-button");
const messagesEl = document.querySelector("#messages");
const connectionStatus = document.querySelector("#connection-status");

const conversation = [];
let pending = false;

function appendMessage(role, text, options = {}) {
  const article = document.createElement("article");
  article.className = role === "user" ? "message user-message" : "message assistant-message";

  const avatar = document.createElement("div");
  avatar.className = role === "user" ? "avatar user-avatar" : "avatar assistant-avatar";
  avatar.textContent = role === "user" ? "K" : "H";

  const wrap = document.createElement("div");
  wrap.className = "bubble-wrap";

  const label = document.createElement("div");
  label.className = "message-label";
  label.textContent = role === "user" ? "YOU" : "HOLOS ASSISTANT";

  const bubble = document.createElement("div");
  bubble.className = options.typing ? "bubble typing" : "bubble";
  bubble.textContent = text;

  wrap.append(label, bubble);
  article.append(avatar, wrap);
  messagesEl.append(article);
  messagesEl.scrollTop = messagesEl.scrollHeight;

  return { article, bubble };
}

function setPending(value) {
  pending = value;
  sendButton.disabled = value;
  input.disabled = value;
  sendButton.querySelector("span:first-child").textContent = value ? "Thinking…" : "Send";
}

async function checkServer() {
  try {
    const response = await fetch("/api/health");
    if (!response.ok) throw new Error("Health check failed");
    const health = await response.json();

    if (health.apiKeyConfigured) {
      connectionStatus.textContent = "Server ready · " + health.model;
    } else {
      connectionStatus.textContent = "Server running · API key not configured";
    }
  } catch (_error) {
    connectionStatus.textContent = "Cannot reach the local server";
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (pending) return;

  const prompt = input.value.trim();
  if (!prompt) return;

  conversation.push({ role: "user", content: prompt });
  appendMessage("user", prompt);
  input.value = "";
  input.style.height = "auto";
  setPending(true);

  const typingMessage = appendMessage("assistant", "Thinking through that…", { typing: true });

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: conversation.slice(-16) })
    });

    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(data.error || "The chat request failed.");
    }

    const reply = typeof data.reply === "string" ? data.reply : "";
    if (!reply) throw new Error("The server returned an empty reply.");

    conversation.push({ role: "assistant", content: reply });
    typingMessage.bubble.className = "bubble";
    typingMessage.bubble.textContent = reply;
  } catch (error) {
    typingMessage.bubble.className = "bubble";
    typingMessage.bubble.textContent = error instanceof Error ? error.message : "Unexpected chat error.";
  } finally {
    setPending(false);
    input.focus();
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }
});

input.addEventListener("input", () => {
  input.style.height = "auto";
  input.style.height = Math.min(input.scrollHeight, 150) + "px";
});

input.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    form.requestSubmit();
  }
});

clearButton.addEventListener("click", () => {
  if (pending) return;
  conversation.length = 0;
  messagesEl.replaceChildren();
  appendMessage("assistant", "Conversation cleared. What would you like to work on?");
  input.focus();
});

checkServer();
