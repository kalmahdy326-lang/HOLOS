import "dotenv/config";

import express, { type NextFunction, type Request, type Response } from "express";
import { rateLimit } from "express-rate-limit";
import helmet from "helmet";
import { Mistral } from "@mistralai/mistralai";
import { fileURLToPath } from "node:url";

const MODEL = "mistral-small-latest";
const MAX_HISTORY_MESSAGES = 16;
const MAX_MESSAGE_LENGTH = 6_000;
const PORT = readPort(process.env.PORT);
const HOST = process.env.HOST?.trim() || "127.0.0.1";
const PUBLIC_DIR = fileURLToPath(new URL("../public/", import.meta.url));

type ChatRole = "user" | "assistant";
type ChatMessage = {
  role: ChatRole;
  content: string;
};

const SYSTEM_PROMPT = [
  "You are the HOLOS project assistant.",
  "Help with the HOLOS animated science-fiction series, its scripts, characters, visual development, story continuity, and local-first production workflow.",
  "Treat HOLOS animation production and the separate HOLOS scientific research programme as related but distinct workstreams.",
  "Do not invent project canon, files, approvals, technical test results, or production status. Clearly distinguish documented facts, owner-supplied information, proposals, and unresolved questions.",
  "Keep these continuity rules in view: Khaled and Kevin are the central investigators; ORBIT is the station AI/system voice and is distinct from the unidentified Moon presence; the Moon's identity and origin remain unresolved; the Regions A/B/C binary pattern and gravitational/geometric deviation are observations, not proof of causation.",
  "For real scientific claims, separate established results from hypotheses and fiction. Do not present a fictional event or HOLOS interpretation as a verified scientific discovery.",
  "Be practical, direct, and collaborative. Prefer preserving existing work and making reviewable changes over silently replacing project assets."
].join(" ");

let cachedClient: Mistral | undefined;

function readPort(value: string | undefined): number {
  if (!value) return 3030;
  const parsed = Number.parseInt(value, 10);
  if (!Number.isInteger(parsed) || parsed < 1 || parsed > 65_535) {
    throw new Error("PORT must be an integer between 1 and 65535.");
  }
  return parsed;
}

function getMistralClient(): Mistral | undefined {
  const apiKey = process.env.MISTRAL_API_KEY?.trim();
  if (!apiKey) return undefined;

  if (!cachedClient) {
    cachedClient = new Mistral({ apiKey });
  }

  return cachedClient;
}

function parseMessages(value: unknown): ChatMessage[] | null {
  if (!Array.isArray(value) || value.length < 1 || value.length > MAX_HISTORY_MESSAGES) {
    return null;
  }

  const messages: ChatMessage[] = [];

  for (const item of value) {
    if (typeof item !== "object" || item === null) return null;

    const candidate = item as Record<string, unknown>;
    const role = candidate.role;
    const content = candidate.content;

    if (role !== "user" && role !== "assistant") return null;
    if (typeof content !== "string") return null;

    const normalized = content.trim();
    if (normalized.length === 0 || normalized.length > MAX_MESSAGE_LENGTH) return null;

    messages.push({ role, content: normalized });
  }

  // The browser may only send user/assistant history, and each request must end with a user turn.
  if (messages[messages.length - 1]?.role !== "user") return null;

  return messages;
}

function extractText(content: unknown): string {
  if (typeof content === "string") return content;

  if (Array.isArray(content)) {
    return content.map((part: unknown) => {
      if (typeof part === "string") return part;
      if (typeof part === "object" && part !== null && "text" in part) {
        const text = (part as { text?: unknown }).text;
        return typeof text === "string" ? text : "";
      }
      return "";
    }).join("");
  }

  return "";
}

const app = express();

app.disable("x-powered-by");
app.use(helmet());
app.use(express.json({ limit: "128kb" }));

const chatLimiter = rateLimit({
  windowMs: 10 * 60 * 1_000,
  limit: 30,
  standardHeaders: "draft-8",
  legacyHeaders: false,
  handler: (_request: Request, response: Response) => {
    response.status(429).json({
      error: "Too many requests. Wait a few minutes and try again."
    });
  }
});

app.get("/api/health", (_request: Request, response: Response) => {
  response.json({
    ok: true,
    model: MODEL,
    apiKeyConfigured: Boolean(process.env.MISTRAL_API_KEY?.trim())
  });
});

app.post("/api/chat", chatLimiter, async (request: Request, response: Response) => {
  const messages = parseMessages(request.body?.messages);

  if (!messages) {
    response.status(400).json({
      error: "Send 1–16 user/assistant messages. Each message must contain text, and the final message must be from the user."
    });
    return;
  }

  const mistral = getMistralClient();
  if (!mistral) {
    response.status(503).json({
      error: "MISTRAL_API_KEY is not configured. Add it to apps/mistral-chat/.env and restart the server."
    });
    return;
  }

  try {
    const completion = await mistral.chat.complete({
      model: MODEL,
      messages: [
        { role: "system", content: SYSTEM_PROMPT },
        ...messages
      ]
    });

    const reply = extractText(completion.choices?.[0]?.message?.content).trim();

    if (!reply) {
      response.status(502).json({
        error: "Mistral returned an empty response. Please try again."
      });
      return;
    }

    response.json({
      model: MODEL,
      reply
    });
  } catch (error: unknown) {
    // Do not send provider error details or credentials back to the browser.
    const message = error instanceof Error ? error.message : "Unknown Mistral API error";
    console.error("Mistral chat request failed:", message);
    response.status(502).json({
      error: "The Mistral request failed. Check the server key, model access, and network connection, then try again."
    });
  }
});

app.use(express.static(PUBLIC_DIR, { etag: true, maxAge: "1h" }));

app.use((error: unknown, _request: Request, response: Response, _next: NextFunction) => {
  const status = typeof error === "object" && error !== null && "status" in error
    ? Number((error as { status?: unknown }).status)
    : 500;

  if (status === 413) {
    response.status(413).json({ error: "The request is too large." });
    return;
  }

  response.status(status >= 400 && status < 600 ? status : 500).json({
    error: "The server could not process that request."
  });
});

app.listen(PORT, HOST, () => {
  console.log("HOLOS Mistral chat is running at http://" + HOST + ":" + PORT);
  console.log("Model: " + MODEL);
  console.log("MISTRAL_API_KEY configured: " + Boolean(process.env.MISTRAL_API_KEY?.trim()));
});
