# Telegramer

<p align="center"><a href="https://github.com/noam09/deluge-telegramer" title="Telegramer"><img src="https://i.imgur.com/xXIPX44.png" alt="Telegramer"></a></p>

**Fork of [noam09/deluge-telegramer](https://github.com/noam09/deluge-telegramer)**, modernized for `python-telegram-bot` v20+ and Deluge 2.2.0+.

> ⚠️ **This fork does NOT work with Deluge 1.x or 2.1.x.** Deluge 2.2.0 uses a completely different plugin scanning mechanism (`importlib.metadata` + `Distribution.at()`) that is incompatible with older versions.

> ⚠️ **setuptools version issue:** The `linuxserver/mods:universal-package-install` mod auto-upgrades setuptools to v83+, which removes `pkg_resources` and **breaks Deluge**. You must pin `setuptools==81.0.0` in your `INSTALL_PIP_PACKAGES` to prevent this. See the docker-compose example below.

---

- [Requirements](#requirements)
- [Installation](#installation)
- [Bot Setup](#bot-setup)
- [Commands](#commands)
- [Troubleshooting](#troubleshooting)
- [Screenshots](#screenshots)
- [License](#license)

## Requirements

| Dependency          | Version    |
| ------------------- | ---------- |
| Deluge              | **2.2.0+** |
| Python              | **3.11+**  |
| python-telegram-bot | **>=20.0** |

## Installation

### linuxserver/deluge Docker (recommended)

#### 1. docker-compose environment

```yaml
deluge:
  image: lscr.io/linuxserver/deluge:latest
  environment:
    - DOCKER_MODS=linuxserver/mods:universal-package-install
    - INSTALL_PIP_PACKAGES=setuptools==81.0.0|python-telegram-bot>=20.0
    - PYTHONPATH=/lsiopy/lib/python3.12/site-packages
  volumes:
    - ./config/Deluge:/config
```

- `DOCKER_MODS` enables pip package installation on container start.
- `INSTALL_PIP_PACKAGES` installs the Telegram bot library and **pins setuptools to 81.0.0** (v83+ removes `pkg_resources` which Deluge needs).
- `PYTHONPATH` ensures Deluge can find pip-installed packages at runtime (linuxserver installs them under `/lsiopy/`).

#### 2. Download the egg

Download the latest `.egg` from the [Releases](https://github.com/Avallone-io/deluge-telegramer/releases) page matching your Python version (e.g. `Telegramer-2.2.0.0-py3.12.egg`).

#### 3. Extract the egg (CRITICAL)

**Deluge 2.2.0 only loads extracted `.egg` directories, not zip files.** You must unzip the egg into the plugins folder:

```bash
cd ./config/Deluge/plugins/
unzip Telegramer-2.2.0.0-py3.12.egg -d Telegramer-2.2.0.0-py3.12.egg.tmp
rm Telegramer-2.2.0.0-py3.12.egg
mv Telegramer-2.2.0.0-py3.12.egg.tmp Telegramer-2.2.0.0-py3.12.egg
```

The result should be a **directory** named `Telegramer-2.2.0.0-py3.12.egg/` containing `EGG-INFO/` and `telegramer/`.

#### 4. Restart the container

```bash
docker compose restart deluge
```

#### 5. Enable in Web UI

Go to **Preferences → Plugins** and enable **Telegramer**.

### Manual install (non-Docker)

1. Build the egg: `python setup.py bdist_egg`
2. Copy the egg to `~/.config/deluge/plugins/`
3. **Extract it** (same unzip procedure as above)
4. Restart `deluged` and enable in the UI

## Bot Setup

1. **Create a bot**: Message [@BotFather](https://telegram.me/BotFather) on Telegram and follow instructions to create a new bot. Copy the **token**.

2. **Get your user ID**: Message [@MyIDBot](https://telegram.me/myidbot) and send `/getid`. Copy your **user ID**.

3. **Configure the plugin**: In Deluge Web UI → Preferences → Telegramer:
   - Paste your bot token into "Telegram Bot Token"
   - Paste your user ID into "Telegram User ID"
   - Optionally add comma-separated additional user IDs (they can use `/add` but won't get notifications)

4. **Start conversation**: Send `/start` to your bot on Telegram.

5. **Test**: Click the **Test** button in Telegramer preferences. You should receive a message from your bot.

## Commands

| Command   | Description                                   |
| --------- | --------------------------------------------- |
| `/help`   | Show available commands                       |
| `/list`   | List all torrents                             |
| `/down`   | List downloading torrents                     |
| `/up`     | List uploading/seeding torrents               |
| `/add`    | Add a torrent (magnet, URL, or .torrent file) |
| `/cancel` | Cancel current operation                      |
| `/rss`    | Add RSS filter (requires YaRSS2 plugin)       |

**Categories**: Configure category/directory pairs in Telegramer preferences. When adding a torrent, the bot will prompt you to pick a category and move the completed download to the matching directory.

**Labels**: Works with Deluge's built-in Label plugin to tag torrents.

**Proxy**: Configure proxy in format `protocol://HOST:PORT` (e.g. `socks5://127.0.0.1:9051`).

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and debugging commands.

## Screenshots

GTK UI:

![preview thumb](http://i.imgur.com/aWh2i4e.jpg)

Web UI:

![preview thumb](http://i.imgur.com/GIkoCV3.jpg)

Example bot:

![preview thumb](http://i.imgur.com/qnZWIip.jpg)

Initiating communication with the new bot:

![preview thumb](http://i.imgur.com/h7TaMtz.jpg)

Quick-access commands (set via [@BotFather](https://telegram.me/BotFather) `/setcommands`):

![preview thumb](http://i.imgur.com/HoM9j6O.jpg)

Category selection when adding a torrent:

![preview thumb](http://i.imgur.com/VaBVlYs.jpg)

Label selection:

![preview thumb](http://i.imgur.com/Obs3DZj.jpg)

Adding by URL:

![preview thumb](http://i.imgur.com/LYPDy3y.jpg)

Adding a .torrent file:

![preview thumb](http://i.imgur.com/jdGO6TI.jpg)

Adding a magnet link:

![preview thumb](http://i.imgur.com/BiOh7lw.jpg)

Listing downloads:

![preview thumb](http://i.imgur.com/S7Zf2fN.jpg)

Seeding status:

![preview thumb](http://i.imgur.com/CRdBwJa.jpg)

RSS filter configuration:

![preview thumb](https://i.imgur.com/dMBgWuC.png?2)

YaRSS2 configuration:

![preview thumb](https://i.imgur.com/K3vwVs7.png?2)

Adding RSS filter via chat:

![preview thumb](https://i.imgur.com/BZDZC6W.jpg?2)

## License

This is free software under the GPL v3 open source license. Feel free to do with it what you wish, but any modification must be open sourced. A copy of the license is included.
