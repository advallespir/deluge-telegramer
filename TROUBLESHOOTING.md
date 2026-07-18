# Troubleshooting Telegramer Plugin

## The #1 Issue: Egg Must Be Extracted

**Deluge 2.2.0 does NOT load zipped `.egg` files.** It uses `importlib.metadata` with `Distribution.at()` which requires an extracted directory.

If you see "Cannot enable non-existent plugin Telegramer" — this is almost certainly the cause.

**Fix**: Unzip the egg so it becomes a directory:

```bash
cd /config/plugins/   # or your plugins path
unzip Telegramer-2.2.0.0-py3.12.egg -d Telegramer-2.2.0.0-py3.12.egg.tmp
rm Telegramer-2.2.0.0-py3.12.egg
mv Telegramer-2.2.0.0-py3.12.egg.tmp Telegramer-2.2.0.0-py3.12.egg
```

Verify the structure:
```
plugins/
└── Telegramer-2.2.0.0-py3.12.egg/   ← directory, NOT a zip file
    ├── EGG-INFO/
    │   ├── PKG-INFO
    │   ├── entry_points.txt
    │   ├── requires.txt
    │   └── top_level.txt
    └── telegramer/
        ├── __init__.py
        ├── core.py
        └── ...
```

---

## Common Issues on linuxserver/deluge

### PYTHONPATH Not Set

**Symptom**: Deluge can't find `telegram` module at runtime — plugin fails silently or shows import errors.

**Cause**: linuxserver images install pip packages in `/lsiopy/` which isn't in Deluge's Python path by default.

**Fix**: Add to your docker-compose environment:
```yaml
- PYTHONPATH=/lsiopy/lib/python3.12/site-packages
```

### Wrong Python Version Egg

**Symptom**: Egg directory is present but Deluge doesn't see the plugin.

**Cause**: The egg directory name contains the Python version (e.g., `-py3.12.egg`). If your container uses a different Python version, Deluge won't load it.

**Fix**: Check your Python version and download the matching egg:
```bash
docker exec <container> python3 --version
```

### Version Conflict

**Symptom**: Plugin fails to load with version-related errors.

**Cause**: The installed `python-telegram-bot` version doesn't match what the egg expects.

**Fix**: Ensure `INSTALL_PIP_PACKAGES` installs a compatible version. The plugin requires `python-telegram-bot>=20.0` with no upper bound.

---

## Recommended docker-compose for linuxserver/deluge

```yaml
deluge:
  image: lscr.io/linuxserver/deluge:latest
  environment:
    - DOCKER_MODS=linuxserver/mods:universal-package-install
    - INSTALL_PIP_PACKAGES=python-telegram-bot>=20.0
    - PYTHONPATH=/lsiopy/lib/python3.12/site-packages
  volumes:
    - ./config/Deluge:/config
```

Then extract the `.egg` into `./config/Deluge/plugins/` as described above.

---

## Debugging Commands

```bash
# Check Python version in container
docker exec <container> python3 --version

# Check if python-telegram-bot is importable
docker exec <container> python3 -c "import telegram; print(telegram.__version__)"

# Check if Deluge can discover the plugin
docker exec <container> python3 -c "
from importlib.metadata import Distribution
import pathlib
d = Distribution.at(pathlib.Path('/config/plugins/Telegramer-2.2.0.0-py3.12.egg'))
print('Name:', d.metadata['Name'])
print('Version:', d.metadata['Version'])
for ep in d.entry_points:
    print(f'  Entry point: {ep.group} -> {ep.name} = {ep.value}')
"

# List what's in the plugins directory
docker exec <container> ls -la /config/plugins/

# Check if the egg is a directory (should show 'd' in permissions)
docker exec <container> stat /config/plugins/Telegramer-2.2.0.0-py3.12.egg

# Check egg metadata files exist
docker exec <container> cat /config/plugins/Telegramer-2.2.0.0-py3.12.egg/EGG-INFO/entry_points.txt
```

---

## APK Error "unable to select packages"

The error `ERROR: unable to select packages: python3-3.12...` in container logs is **harmless**. It's caused by Alpine repo conflicts (newer Python packages in repos vs container's Python version). The pip install continues successfully after this error.
