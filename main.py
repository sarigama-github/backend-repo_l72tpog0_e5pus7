import os
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from database import db, create_document, get_documents
from bson import ObjectId

app = FastAPI(title="CriM🔥Son API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProjectCreateRequest(BaseModel):
    prompt: str
    name: Optional[str] = None


class ChatMessageRequest(BaseModel):
    message: str


class CodeUpdateRequest(BaseModel):
    html: str


class DeployResponse(BaseModel):
    url: str
    status: str


def oid_str(oid: ObjectId) -> str:
    return str(oid)


def seo_from_prompt(prompt: str) -> Dict[str, str]:
    title = prompt.strip().capitalize()[:60]
    description = f"Auto-generated website: {prompt.strip()}"
    keywords = ", ".join([w for w in prompt.lower().split() if w.isalpha()][:8])
    return {"title": title or "CriM🔥Son Site", "description": description, "keywords": keywords}


def generate_site_html(prompt: str, accent="#DC143C") -> str:
    seo = seo_from_prompt(prompt)
    # Tailwind CDN for instant styling, Inter font, Lucide icons optional
    # Spline hero section per system instructions
    spline = "https://prod.spline.design/4cHQr84zOGAHOehh/scene.splinecode"
    return f"""
<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>{seo['title']}</title>
    <meta name=\"description\" content=\"{seo['description']}\" />
    <meta name=\"keywords\" content=\"{seo['keywords']}\" />
    <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\" />
    <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin />
    <link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap\" rel=\"stylesheet\" />
    <script src=\"https://cdn.tailwindcss.com\"></script>
    <style>
      :root {{ --accent: {accent}; }}
      html, body {{ height: 100%; }}
      body {{ font-family: 'Inter', system-ui, -apple-system, Segoe UI, Roboto, sans-serif; }}
      .crimson-gradient {{ background: radial-gradient(1200px 600px at 50% -20%, rgba(220,20,60,0.25), transparent),
                           radial-gradient(800px 400px at 120% 20%, rgba(99,102,241,0.15), transparent),
                           #0b0b10; }}
      .glass {{ backdrop-filter: blur(12px); background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.08); }}
      .btn {{ background: var(--accent); color: white; box-shadow: 0 10px 30px rgba(220,20,60,0.35); }}
      .btn:hover {{ filter: brightness(1.05); transform: translateY(-1px); }}
    </style>
  </head>
  <body class=\"min-h-full crimson-gradient text-white\">
    <header class=\"sticky top-0 z-50 border-b border-white/10 bg-black/30 backdrop-blur\">
      <div class=\"max-w-7xl mx-auto px-6 py-4 flex items-center justify-between\">
        <a href=\"#\" class=\"font-extrabold tracking-tight text-xl\">CriM🔥Son</a>
        <nav class=\"hidden md:flex gap-8 text-white/80\">
          <a href=\"#features\" class=\"hover:text-white transition\">Features</a>
          <a href=\"#templates\" class=\"hover:text-white transition\">Templates</a>
          <a href=\"#contact\" class=\"hover:text-white transition\">Contact</a>
        </nav>
        <a href=\"#cta\" class=\"btn px-4 py-2 rounded-lg font-semibold\">Get Started</a>
      </div>
    </header>

    <section class=\"relative\" aria-label=\"Hero\">
      <div class=\"absolute inset-0 opacity-80\" style=\"pointer-events:none\">
        <iframe src=\"{spline}\" title=\"AI Aura\" style=\"width:100%;height:100%;border:0;\"></iframe>
      </div>
      <div class=\"relative z-10 max-w-5xl mx-auto px-6 pt-28 pb-24 text-center\">
        <h1 class=\"text-4xl md:text-6xl font-extrabold leading-tight\">{prompt}</h1>
        <p class=\"mt-6 text-white/80 text-lg md:text-xl\">Production-ready site generated instantly. Clean, accessible, responsive, and fast.</p>
        <div class=\"mt-10 flex items-center justify-center gap-4\" id=\"cta\">
          <a href=\"#contact\" class=\"btn px-6 py-3 rounded-xl font-semibold\">Start Now</a>
          <a href=\"#features\" class=\"px-6 py-3 rounded-xl font-semibold glass\">Explore Features</a>
        </div>
      </div>
    </section>

    <main class=\"relative z-10\">
      <section id=\"features\" class=\"max-w-6xl mx-auto px-6 py-20 grid md:grid-cols-3 gap-6\">
        <div class=\"glass rounded-2xl p-6\">
          <h3 class=\"text-xl font-bold\">Instant Preview</h3>
          <p class=\"text-white/80 mt-2\">Your site renders as you describe it. No waiting, no compiling.</p>
        </div>
        <div class=\"glass rounded-2xl p-6\">
          <h3 class=\"text-xl font-bold\">Clean Code</h3>
          <p class=\"text-white/80 mt-2\">Accessible, semantic HTML with responsive layouts out of the box.</p>
        </div>
        <div class=\"glass rounded-2xl p-6\">
          <h3 class=\"text-xl font-bold\">SEO Ready</h3>
          <p class=\"text-white/80 mt-2\">Meta tags, performance hints, and fast loading by default.</p>
        </div>
      </section>

      <section id=\"templates\" class=\"max-w-6xl mx-auto px-6 pb-24\">
        <h2 class=\"text-2xl font-bold mb-6\">Featured Sections</h2>
        <div class=\"grid md:grid-cols-3 gap-6\">
          <article class=\"glass rounded-xl overflow-hidden\">
            <img src=\"https://picsum.photos/seed/hero/800/500\" alt=\"Placeholder image\" class=\"w-full h-40 object-cover\" />
            <div class=\"p-5\">
              <h3 class=\"font-semibold\">Hero + CTA</h3>
              <p class=\"text-white/80 text-sm mt-1\">Crisp hero section with strong call-to-action.</p>
            </div>
          </article>
          <article class=\"glass rounded-xl overflow-hidden\">
            <img src=\"https://picsum.photos/seed/feature/800/500\" alt=\"Placeholder image\" class=\"w-full h-40 object-cover\" />
            <div class=\"p-5\">
              <h3 class=\"font-semibold\">Feature Grid</h3>
              <p class=\"text-white/80 text-sm mt-1\">Explain value with icons and concise text.</p>
            </div>
          </article>
          <article class=\"glass rounded-xl overflow-hidden\">
            <img src=\"https://picsum.photos/seed/contact/800/500\" alt=\"Placeholder image\" class=\"w-full h-40 object-cover\" />
            <div class=\"p-5\">
              <h3 class=\"font-semibold\">Contact Form</h3>
              <p class=\"text-white/80 text-sm mt-1\">Accessible form with client-side validation.</p>
            </div>
          </article>
        </div>
      </section>

      <section id=\"contact\" class=\"max-w-2xl mx-auto px-6 pb-24\">
        <div class=\"glass rounded-2xl p-8\">
          <h2 class=\"text-2xl font-bold\">Get in touch</h2>
          <form class=\"mt-6 grid gap-4\" onsubmit=\"event.preventDefault(); alert('Submitted!')\">
            <div>
              <label class=\"block text-sm text-white/70\">Name</label>
              <input class=\"w-full mt-1 p-3 rounded-lg bg-white/10 border border-white/10 outline-none focus:border-white/30\" required />
            </div>
            <div>
              <label class=\"block text-sm text-white/70\">Email</label>
              <input type=\"email\" class=\"w-full mt-1 p-3 rounded-lg bg-white/10 border border-white/10 outline-none focus:border-white/30\" required />
            </div>
            <div>
              <label class=\"block text-sm text-white/70\">Message</label>
              <textarea rows=\"4\" class=\"w-full mt-1 p-3 rounded-lg bg-white/10 border border-white/10 outline-none focus:border-white/30\" required></textarea>
            </div>
            <button class=\"btn px-5 py-3 rounded-xl font-semibold\">Send</button>
          </form>
        </div>
      </section>
    </main>

    <footer class=\"border-t border-white/10 py-10 text-center text-white/60\">
      <p>© {datetime.now().year} CriM🔥Son — Generated by natural language</p>
    </footer>
  </body>
</html>
"""


@app.get("/")
def read_root():
    return {"message": "CriM🔥Son API running"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set",
        "database_name": "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": [],
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            try:
                response["collections"] = db.list_collection_names()[:10]
                response["connection_status"] = "Connected"
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but error: {str(e)[:60]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:60]}"
    return response


# ------------------------------- AUTH (mock) -------------------------------
@app.post("/auth/guest")
def auth_guest():
    # In a real app, integrate Google/Apple. Here we return a pseudo user id
    uid = f"guest_{int(datetime.now(tz=timezone.utc).timestamp())}"
    return {"user_id": uid, "name": "Guest"}


# ------------------------------ PROJECTS CRUD ------------------------------
@app.post("/projects")
def create_project(req: ProjectCreateRequest, x_user_id: Optional[str] = Header(default=None)):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")

    html = generate_site_html(req.prompt)
    project = {
        "user_id": x_user_id or "guest",
        "name": req.name or (req.prompt[:40] + "…" if len(req.prompt) > 40 else req.prompt),
        "prompt": req.prompt,
        "html": html,
        "versions": [
            {"timestamp": datetime.now(timezone.utc), "html": html, "note": "Initial generation"}
        ],
        "history": [
            {"timestamp": datetime.now(timezone.utc), "role": "user", "content": req.prompt},
            {"timestamp": datetime.now(timezone.utc), "role": "assistant", "content": "Generated initial site"},
        ],
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
        "status": "draft",
    }
    pid = create_document("projects", project)
    return {"project_id": pid, "html": html}


@app.get("/projects")
def list_projects(x_user_id: Optional[str] = Header(default=None)):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    items = get_documents("projects", {"user_id": x_user_id or "guest"}, limit=50)
    for it in items:
        it["id"] = oid_str(it["_id"]) if "_id" in it else None
        it.pop("_id", None)
        it.pop("html", None)  # list view
    return {"projects": items}


@app.get("/projects/{project_id}")
def get_project(project_id: str, x_user_id: Optional[str] = Header(default=None)):
    from bson import ObjectId
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    doc = db.projects.find_one({"_id": ObjectId(project_id), "user_id": x_user_id or "guest"})
    if not doc:
        raise HTTPException(status_code=404, detail="Project not found")
    doc["id"] = oid_str(doc["_id"]) if "_id" in doc else None
    doc.pop("_id", None)
    return doc


@app.put("/projects/{project_id}/code")
def update_code(project_id: str, req: CodeUpdateRequest, x_user_id: Optional[str] = Header(default=None)):
    from bson import ObjectId
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    res = db.projects.update_one(
        {"_id": ObjectId(project_id), "user_id": x_user_id or "guest"},
        {
            "$set": {"html": req.html, "updated_at": datetime.now(timezone.utc)},
            "$push": {"versions": {"timestamp": datetime.now(timezone.utc), "html": req.html, "note": "Manual edit"}},
        },
    )
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"status": "ok"}


@app.post("/projects/{project_id}/chat")
def project_chat(project_id: str, req: ChatMessageRequest, x_user_id: Optional[str] = Header(default=None)):
    from bson import ObjectId
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")

    doc = db.projects.find_one({"_id": ObjectId(project_id), "user_id": x_user_id or "guest"})
    if not doc:
        raise HTTPException(status_code=404, detail="Project not found")

    msg = req.message.lower()
    html = doc.get("html", "")

    # Very simple rule-based edits as a placeholder for LLM tool-use
    note = ""
    if "sci-fi" in msg or "sci fi" in msg:
        html = html.replace("#0b0b10", "#05060a").replace("rgba(99,102,241,0.15)", "rgba(56,189,248,0.18)")
        html = html.replace("Production-ready", "Sci‑fi neon aesthetic with holographic accents")
        note = "Applied sci-fi theme"
    elif "make it dark" in msg or "dark mode" in msg:
        html = html.replace("#0b0b10", "#0a0a0a")
        note = "Darkened base colors"
    elif "add pricing" in msg or "pricing" in msg:
        insertion = """
<section id=\"pricing\" class=\"max-w-6xl mx-auto px-6 pb-24\">
  <h2 class=\"text-2xl font-bold mb-6\">Pricing</h2>
  <div class=\"grid md:grid-cols-3 gap-6\">
    <div class=\"glass rounded-2xl p-6\"><h3 class=\"font-semibold\">Starter</h3><p class=\"text-4xl font-extrabold mt-2\">$0</p><p class=\"text-white/70 mt-2\">For experiments</p></div>
    <div class=\"glass rounded-2xl p-6 border border-white/20\"><h3 class=\"font-semibold\">Pro</h3><p class=\"text-4xl font-extrabold mt-2\">$19</p><p class=\"text-white/70 mt-2\">For builders</p></div>
    <div class=\"glass rounded-2xl p-6\"><h3 class=\"font-semibold\">Scale</h3><p class=\"text-4xl font-extrabold mt-2\">$99</p><p class=\"text-white/70 mt-2\">For teams</p></div>
  </div>
</section>
"""
        html = html.replace("</main>", insertion + "\n    </main>")
        note = "Added pricing section"
    elif "change accent" in msg or "make it crimson" in msg or "crimson" in msg:
        html = html.replace("--accent: #DC143C", "--accent: #b80f2a")
        note = "Adjusted accent color"
    else:
        # Regenerate using the new instruction appended to original prompt
        combined = f"{doc.get('prompt','')} — {req.message}"
        html = generate_site_html(combined)
        note = "Regenerated site with new instruction"

    db.projects.update_one(
        {"_id": ObjectId(project_id)},
        {
            "$set": {"html": html, "updated_at": datetime.now(timezone.utc)},
            "$push": {
                "history": {"timestamp": datetime.now(timezone.utc), "role": "user", "content": req.message},
                "history": {"timestamp": datetime.now(timezone.utc), "role": "assistant", "content": note},
                "versions": {"timestamp": datetime.now(timezone.utc), "html": html, "note": note},
            },
        },
    )

    return {"status": "ok", "note": note, "html": html}


@app.post("/projects/{project_id}/deploy", response_model=DeployResponse)
def deploy_project(project_id: str, x_user_id: Optional[str] = Header(default=None)):
    # Simulate deployment. A real implementation would build and upload to a CDN provider
    fake_url = f"https://deploy.crimson.site/{project_id}"
    return DeployResponse(url=fake_url, status="deployed")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
