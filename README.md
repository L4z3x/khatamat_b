# KHATAMAT
A platform for gathering **"Ghoraba" غرباء** (Muslims) in one place where they can read the Quran, discuss, and do Khatmas together inside a group.

## What is a Khatma?
A **Khatma** is when a person or a group reads the Quran or a part of it by splitting it into shares (pages, thomon, hizbs, etc.). Each member reads their assigned share before the specified end time.

---

## Contributing

### Prerequisites
Make sure you have **Docker** and **Docker Compose** installed on your machine.

### Server Side

#### Clone the Repository
```bash
git clone https://github.com/L4z3x/khatamat_b.git
```

#### Modify `app.dev.env` File

Add the following fields to the `app.dev.env` file:

```env
EMAIL_USER=app-email-address
APP_PASSWORD=email-app-password
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH_CALLBACK_URL=your-google-callback-url
```

#### Note
Ensure that the `env_file` in the `docker-compose.yml` file points to `./app.dev.env`.

#### Run Docker Compose
```bash
cd khatamat_b
docker compose up --build -d
```
Now the server is ready.

---

### Client Side

#### Clone the Repository
```bash
git clone https://github.com/KMalek101/gharib
```

#### Run the Client Code
Ensure you have **Next.js** installed on your machine.

```bash
cd gharib/
npm install
npm run dev
```

Open a new branch and start contributing!

---
