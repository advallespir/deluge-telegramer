# Troubleshooting Telegramer Plugin

## Common Issues on linuxserver/deluge

### "Cannot enable non-existent plugin Telegramer"

This means Deluge cannot find or load the .egg file. Common causes:

#### 1. Version Conflict
**Symptom**: `pkg_resources.ContextualVersionConflict: (python-telegram-bot X.Y ...)`

**Cause**: The installed `python-telegram-bot` version doesn't match what the egg expects.

**Fix**: Make sure `INSTALL_PIP_PACKAGES` installs a compatible version. The plugin requires `python-telegram-bot>=20.0` with no upper bound.

#### 2. pkg_resources Not Found
**Symptom**: `ModuleNotFoundError: No module named 'pkg_resources'`

**Cause**: Modern setuptools (70+) removed `pkg_resources` as a standalone module. Deluge needs it to scan plugin eggs.

**Fix**: Pin setuptools to <70 in your pip packages:
```yaml
- INSTALL_PIP_PACKAGES=python-telegram-bot>=20.0|setuptools<70
```

#### 3. PYTHONPATH Not Set
**Symptom**: Deluge can't find pip-installed packages (telegram, pkg_resources)

**Cause**: linuxserver images install pip packages in `/lsiopy/` which isn't in system Python's path.

**Fix**: Add to your docker-compose environment:
```yaml
- PYTHONPATH=/lsiopy/lib/python3.12/site-packages
```

#### 4. Wrong Python Version Egg
**Symptom**: Egg file is present but Deluge doesn't see it.

**Cause**: The egg filename contains the Python version (e.g., `-py3.12.egg`). If your container uses a different Python version, it won't load.

**Fix**: Check your Python version with `docker exec <container> python3 --version` and download the matching egg.

### Recommended docker-compose for linuxserver/deluge

```yaml
deluge:
  image: lscr.io/linuxserver/deluge:latest
  environment:
    - DOCKER_MODS=linuxserver/mods:universal-package-install
    - INSTALL_PIP_PACKAGES=python-telegram-bot>=20.0|setuptools<70
    - PYTHONPATH=/lsiopy/lib/python3.12/site-packages
  volumes:
    - ./config/Deluge:/config
```

Then place the `.egg` file in `./config/Deluge/plugins/`.

### Debugging Commands

```bash
# Check Python version
docker exec <container> python3 --version

# Check if python-telegram-bot is importable
docker exec <container> python3 -c "import telegram; print(telegram.__version__)"

# Check if pkg_resources works
docker exec <container> python3 -c "import pkg_resources; print('OK')"

# Check if egg is scannable
docker exec <container> python3 -c "
import pkg_resources
pkg_resources.working_set.add_entry('/config/plugins')
for ep in pkg_resources.iter_entry_points('deluge.plugin.core'):
    print(f'Found: {ep.name}')
"

# Check egg metadata
docker exec <container> python3 -c "
import zipfile
z = zipfile.ZipFile('/config/plugins/Telegramer-2.2.0.0-py3.12.egg')
print(z.read('EGG-INFO/requires.txt').decode())
"
```

### APK Error "unable to select packages"
The error `ERROR: unable to select packages: python3-3.12...` in container logs is **harmless**. It's caused by Alpine repo conflicts (Python 3.14 packages in repos but container uses 3.12). The pip install continues successfully after this error.
