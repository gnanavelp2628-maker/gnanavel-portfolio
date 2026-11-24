# Gnanavel Palanisamy | Full-Stack Portfolio

A portfolio that is itself a working full-stack app, run with one Docker command.

| Service | Tech | Job |
|---|---|---|
| `web` | HTML, CSS, JavaScript, PHP 8.3, Apache | Serves the site, `/api/*` endpoints, contact form, admin page |
| `db` | MySQL 8.4 | Stores projects and contact messages |
| `chatbot` | Python 3.12, FastAPI, Claude API | AI assistant that answers questions about me |

```
Browser ──> Apache (PHP) ──/api/*──> MySQL
                  └──/chat──> Python FastAPI ──> Claude API
```

## Run it (any computer with Docker)
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
cp .env.example .env        # then edit .env: set passwords and ANTHROPIC_API_KEY
docker compose up -d --build
```
Open http://localhost:8080
- Contact messages: http://localhost:8080/admin/messages.php (any username, password = `ADMIN_PASSWORD`)
- Stop: `docker compose down`  |  Reset database: `docker compose down -v`
- The database is filled from `db/init.sql` the first time only.

## Push to GitHub
```bash
git init
git add .
git commit -m "Portfolio: PHP + MySQL + Python AI chatbot in Docker"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```
`.env` is in `.gitignore`, so your API key and passwords are never uploaded. Check this before pushing.
The workflow in `.github/workflows/ci.yml` checks the code and builds the images on every push.

## Put it live on the internet
**Option A: quick demo (free, no server).** On the machine running Docker:
`cloudflared tunnel --url http://localhost:8080` gives a public https link. It lasts while your computer is on.

**Option B: real hosting (recommended for HR).**
1. Get a small Linux VPS (DigitalOcean, AWS Lightsail, Oracle free tier) and install Docker.
2. Clone the repo, create `.env`, set `WEB_PORT=8080`, run `docker compose up -d --build`.
3. Point your domain's A record to the server and add HTTPS with Caddy. `/etc/caddy/Caddyfile`:
   ```
   yourname.com {
     reverse_proxy localhost:8080
   }
   ```
4. Use HTTPS before opening the admin page, because it uses basic login.

## Customise
- Projects: edit `db/init.sql` (new database) or insert rows with
  `docker compose exec db mysql -u root -p portfolio`.
- Screenshots: save images in `web/public/images/`, then add `img:"images/name.webp"` to a project in `index.html`.
- AI answers: edit the facts in `SYSTEM_PROMPT` in `chatbot/server.py`, then `docker compose up -d --build`.
- Add your link back for Kiran Sa Photography in `db/init.sql` once that site is restored.
- `archive/` holds earlier design versions (they need `images/` copied beside them).

## Security notes
Prepared SQL statements, input validation, a hidden honeypot field, a 3-messages-per-10-minutes limit, hashed IPs,
and a rate limit on the chatbot. Change all default passwords in `.env`.
