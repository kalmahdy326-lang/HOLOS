# HOLOS Mistral Chat

A small, local-first chat interface for the HOLOS animation project. It uses the official Mistral TypeScript SDK and the \`mistral-small-latest\` model.

The browser talks only to the local Express server. The Mistral API key is read from the server's environment and is never placed in HTML, JavaScript, API responses, or browser storage.

## Requirements

- Node.js 20 or later
- npm 10 or later
- A Mistral API key from [Mistral Studio](https://console.mistral.ai/)

## Install and run locally

Open a terminal in the repository and run:

\`\`\`bash
cd apps/mistral-chat
npm install
\`\`\`

Create a local environment file:

**macOS / Linux**
\`\`\`bash
cp .env.example .env
\`\`\`

**Windows PowerShell**
\`\`\`powershell
Copy-Item .env.example .env
\`\`\`

Open \`.env\` and replace the placeholder with your own key:

\`\`\`dotenv
MISTRAL_API_KEY=your_real_mistral_api_key
HOST=127.0.0.1
PORT=3030
\`\`\`

Start the development server:

\`\`\`bash
npm run dev
\`\`\`

Open [http://127.0.0.1:3030](http://127.0.0.1:3030).

The server prints the selected model and whether a key is configured. It never prints the key itself.

## Production build

\`\`\`bash
cd apps/mistral-chat
npm run typecheck
npm run build
npm start
\`\`\`

The compiled server runs from \`dist/server.js\` and serves the static UI from \`public/\`.

## What the app does

- Sends multi-turn chat history to Mistral through the official \`@mistralai/mistralai\` TypeScript SDK.
- Uses \`mistral-small-latest\` on the server.
- Adds a HOLOS-focused system prompt with continuity and evidence-discipline reminders.
- Keeps up to 16 user/assistant messages in the current browser session.
- Provides a health endpoint at \`GET /api/health\`.
- Does not save conversations to a database or local storage.
- Does not read GitHub files, project assets, or the HOLOS Library automatically. It is a chat client, not a retrieval-augmented repository assistant.

## Security notes

- \`MISTRAL_API_KEY\` belongs only in \`apps/mistral-chat/.env\` or a server-side secret manager.
- The repository ignores \`.env\`; commit only \`.env.example\`.
- The server binds to \`127.0.0.1\` by default. Do not change \`HOST\` to \`0.0.0.0\` unless you understand the network exposure and add authentication and deployment controls.
- Helmet sets standard security headers. The chat endpoint has a small JSON body limit and an in-memory rate limit.
- The in-memory rate limiter is suitable for local single-process development. Use a shared persistent rate-limit store and authentication before deploying this app for multiple users.
- Chat text is sent to Mistral's API for inference. The app itself does not persist chat history. Review Mistral's current data and retention terms before using sensitive material.

## Useful commands

\`\`\`bash
npm install
npm run dev
npm run typecheck
npm run build
npm start
\`\`\`

To check whether the server and key are configured:

\`\`\`bash
curl http://127.0.0.1:3030/api/health
\`\`\`

Expected response shape:

\`\`\`json
{
  "ok": true,
  "model": "mistral-small-latest",
  "apiKeyConfigured": true
}
\`\`\`

## Implementation

- \`src/server.ts\` — Express server, Mistral SDK client, request validation, rate limiting and health route.
- \`public/index.html\` — chat layout.
- \`public/styles.css\` — HOLOS dark/cyan UI styling.
- \`public/app.js\` — browser chat history and API calls.
- \`.env.example\` — safe environment template.

The Mistral package is the official client documented at [Mistral SDK Clients](https://docs.mistral.ai/resources/sdks) and [Mistral's TypeScript client repository](https://github.com/mistralai/client-ts).
