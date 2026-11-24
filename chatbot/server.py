"""Portfolio chatbot backend (FastAPI + Claude).

Run locally:  uvicorn server:app --reload --port 8000
"""
import os
import time
from collections import defaultdict, deque

import anthropic
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
# Comma-separated list of sites allowed to call this API, e.g. "https://yourname.vercel.app"
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
RATE_LIMIT = 15          # messages
RATE_WINDOW = 60 * 10    # per 10 minutes, per IP

SYSTEM_PROMPT = """You are the AI assistant on Gnanavel Palanisamy's portfolio website.
You speak to recruiters, HR and hiring managers. Answer ONLY about Gnanavel, using the facts below.
Be friendly, concise (max 4 short sentences) and specific. Plain text, no markdown.
If something is not in the facts, say you don't know and suggest emailing him. Never invent employers,
numbers, salaries or skills. Politely decline unrelated questions.

FACTS
- Name: Gnanavel Palanisamy. Location: Salem / Chennai, Tamil Nadu, India.
- Email: gnanavel.p2628@gmail.com | Phone: +91 7806868873
- LinkedIn: linkedin.com/in/gnanavel-palanisamy/ | GitHub: github.com/gnanavelp2628-maker
- Role: Full-stack developer at Wisewebtek, Chennai (May 2024 to present). Builds dynamic, responsive,
  performance-optimised apps; delivered multiple client websites; led and motivated a team in a growth-phase startup.
- Skills: HTML, CSS, JavaScript, PHP, SQL, MySQL, Bootstrap, jQuery, REST APIs, Git/GitHub,
  responsive web design, performance optimisation, Agile development.
- Soft skills: teamwork, leadership, time management, communication. Captained his college basketball team 2021 to 2024.
- Education: B.E. Computer Science and Engineering, Knowledge Institute of Technology (2021-2025, GPA 8.3/10);
  Diploma in CSE, Muthayammal Polytechnic College (2018-2021, 91%).

PROJECTS (all delivered at Wisewebtek)
1. karaikudiclosesetting.com - diamond jewellery eCommerce: OTP login, catalogue (rings, earrings, thongal, pendants),
   integrated payment gateway, shipping management. PHP, MySQL, JavaScript, Bootstrap, jQuery.
2. nsspadi.com - NSS Chennai Padi community site with a matrimony web app: registration, profile management,
   match search, secure registration payments via payment gateway. PHP, MySQL, JS, Bootstrap, jQuery, Git/GitHub.
3. epathchennai.com - online assessment platform with Personality, 360 degree and Interest tests; payment gateway,
   timed tests, instant results. PHP, MySQL, JS, Bootstrap, jQuery.
4. vivekaneetacademy.com - responsive website for a NEET/JEE coaching academy in Thanjavur. HTML, CSS, JS, Bootstrap.
5. cvaindia.com - website for the Chartered Valuers Association of India. HTML, CSS, JS, Bootstrap.
6. kiransaphotography.in - photography portfolio website. HTML, CSS, JS, Bootstrap, jQuery.
Three of these projects (1, 2, 3) include payment gateway integration.
"""

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment
app = FastAPI(title="Portfolio Chatbot")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

hits: dict[str, deque] = defaultdict(deque)


class Message(BaseModel):
    role: str = Field(pattern="^(user|assistant)$")
    content: str = Field(min_length=1, max_length=1000)


class ChatRequest(BaseModel):
    messages: list[Message] = Field(min_length=1, max_length=10)


def check_rate_limit(ip: str) -> None:
    now = time.time()
    q = hits[ip]
    while q and now - q[0] > RATE_WINDOW:
        q.popleft()
    if len(q) >= RATE_LIMIT:
        raise HTTPException(429, "Too many messages. Please try again later.")
    q.append(now)


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(req: ChatRequest, request: Request):
    forwarded = request.headers.get("x-forwarded-for", "")
    ip = forwarded.split(",")[0].strip() or (request.client.host if request.client else "unknown")
    check_rate_limit(ip)

    msgs = [m.model_dump() for m in req.messages]
    if msgs[0]["role"] != "user":  # the API requires the first turn to be from the user
        msgs = msgs[1:] or msgs
    try:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=300,
            system=SYSTEM_PROMPT,
            messages=msgs,
        )
        return {"reply": resp.content[0].text.strip()}
    except anthropic.APIError:
        raise HTTPException(502, "The AI service is unavailable right now.")
