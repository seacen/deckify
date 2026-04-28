"""_ab_common.py — shared agent-browser invocation helpers.

The deckify pipeline drives `agent-browser` for every Phase 1 fetch: home page,
each subpage, and (in embed_logo) the logo asset itself. Brand CDNs that front
their site on Akamai / Cloudflare bot-management products (Tiffany, P&G, large
fashion houses, anything LVMH / Kering) deny the default agent-browser session
because two client-side signals leak that they're talking to a bot:

  1. `navigator.webdriver === true`  (set by Chromium's automation switch)
  2. The user-agent string includes "HeadlessChrome" or the bare "Chrome for
     Testing" UA, which fingerprints differently from real Chrome.

Both go away with two flags on every agent-browser call:

  --args "--disable-blink-features=AutomationControlled"
        # untangles navigator.webdriver — Chromium switches off the automation
        # surface area that the flag controls; downstream sites read
        # navigator.webdriver === undefined the way they would for a normal user.
  --user-agent "<real Chrome UA>"
        # masks the HeadlessChrome substring; Akamai's heuristic UA list stops
        # matching.

Verified on 2026-04-28 against https://www.tiffany.com — without these two
flags, the home request lands on Akamai's "Access Denied" template; with
them, the same agent-browser session pulls a 448 KB hydrated DOM with 290
links and 71 images. No Chrome profile is required.

Why default-on (no opt-in env var):
  - These flags do NOT degrade any honest site. They only tell Chrome "don't
    advertise yourself as automation".
  - They DO unblock a wide class of brand sites that would otherwise fail
    Phase 1a in a way the user can't diagnose.
  - The env var DECKIFY_NO_STEALTH=1 disables them as an emergency escape
    hatch, never required in normal operation.

Usage:
    from _ab_common import agent_browser_cmd
    subprocess.run(agent_browser_cmd("open", url), ...)
    subprocess.run(agent_browser_cmd("eval", js), ...)
"""
from __future__ import annotations

import os


# Real macOS Chrome 131 UA (current stable channel as of late 2025/early 2026).
# Sites that fingerprint UA in detail compare this against Client Hints; the
# CH headers Chromium sends still match modern Chrome, so the pair stays
# internally consistent.
_REAL_CHROME_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)

# Chromium switch — tells the engine NOT to expose the AutomationControlled
# blink-feature, which is what makes navigator.webdriver=true.
_STEALTH_CHROME_ARGS = "--disable-blink-features=AutomationControlled"


def stealth_enabled() -> bool:
    """Stealth flags ON unless DECKIFY_NO_STEALTH=1 is set."""
    return os.environ.get("DECKIFY_NO_STEALTH", "").strip() not in ("1", "true", "yes")


def agent_browser_cmd(*verb_and_args: str) -> list[str]:
    """Build a full ['agent-browser', ...flags, ...verb_args] arg list.

    Pass the verb and its arguments as you would to subprocess: e.g.
        agent_browser_cmd("open", "https://example.com")
        agent_browser_cmd("eval", "document.title")
        agent_browser_cmd("set", "viewport", "1440", "900")

    The returned list always starts with the agent-browser binary and (when
    stealth is enabled) the two anti-bot flags.
    """
    cmd: list[str] = ["agent-browser"]
    if stealth_enabled():
        cmd.extend(["--args", _STEALTH_CHROME_ARGS, "--user-agent", _REAL_CHROME_UA])
    cmd.extend(verb_and_args)
    return cmd
