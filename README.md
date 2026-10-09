# Steam Launcher Addon for Kodi

Launches Steam, closes Kodi, waits for Steam to close, starts Kodi. Doesn't use AutoHotKey so games that run anti-cheat detection won't flag it.

---

## Development

- Used https://convertico.com/ to convert a 256x256 `.png` to a `.ico` file.
- To get the `LICENSE.txt` file, go to https://www.gnu.org/licenses/#LicenseURLs. Click on one of the license links (I chose `GPLv3`), and then click the `plain text` link in the **GPL in other formats** area. Or you can add the license while you're creating a repo in GitHub, then copy and rename it.
- Run `pip install Kodistubs --target ./kodi_stubs` so the linter doesn't complain about missing deps.
