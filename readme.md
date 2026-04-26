# LockInLauncher

**Ever sit down to study and somehow lose 3 hours to absolutely nothing? LockInLauncher fixes that. One command kills the distractions, launches your tools, and starts your focus timer — no willpower required.**

> ⚠️ Windows only for now. Mac & Linux support is on the roadmap.

---

## Features

- **App Launcher** — Automatically opens your productivity apps at the start of every session
- **App Killer** — Kills distracting apps and keeps them closed for the entire session
- **Focus Timer** — Counts down your session in real time and ends automatically when time's up
- **Lock-In Mode** — Adds friction to quitting mid-session so you actually stay focused
- **Config Menu** — Add and remove blocked apps on the fly with `lockin config`

---

## Quickstart

```bash
lockin start
```

That's it. You're locked in.

---

## Installation

> Requires Python 3.8+

**Option 1 — Install via pip (recommended):**
```bash
pip install lockinlauncher
```

**Option 2 — Install from source:**
```bash
git clone https://github.com/johnnydunal/LockInLauncher.git
cd LockInLauncher
pip install -e .
```

> ⚠️ Must be run as Administrator (required for managing system processes)

---

## Getting Started

On your first run, set up your apps with the config menu:
```bash
lockin config
```
From there you can add apps to block, apps to launch, and set your name. Once configured, you're ready to lock in.

---

## Commands

| Command | Description |
|---|---|
| `lockin start` | Start a focus session |
| `lockin config` | Open the config menu to customize your settings |

---

## Configuration

All configuration is handled through `lockin config`. From there you can:
- Add and remove apps to block during sessions
- Add and remove apps to launch at the start of sessions
- Set your name so the app can greet you on startup

### Finding the right app names

**For blocking apps:**
Open the app, then open Task Manager (`Ctrl+Shift+Esc`) → **Details tab**. The exact `.exe` name is listed there (e.g. `discord.exe`, `chrome.exe`).

**For launching apps:**
- If it's a dev tool like VS Code, just use its command name (e.g. `code`)
- Otherwise, open the app → open Task Manager (`Ctrl+Shift+Esc`) → Details tab → right click the process → **"Open file location"** → copy the path from the address bar and add the `.exe` name at the end (e.g. `C:/Program Files/Notion/Notion.exe`)

---

## Roadmap

- [ ] Music/soundtrack integration
- [ ] To-do list for sessions
- [ ] Session stats and streak tracking
- [ ] Custom session profiles (study, coding, writing)
- [ ] Mac & Linux support

---

## Contributing

Found a bug or have a feature request? Open an issue at [github.com/johnnydunal/LockInLauncher/issues](https://github.com/johnnydunal/LockInLauncher/issues)

---

## License

MIT License — free to use, modify, and share.

---

*Built for people who actually want to get stuff done.*
