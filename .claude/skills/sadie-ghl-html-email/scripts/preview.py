#!/usr/bin/env python3
"""Screenshot finished emails at desktop (700px) and phone (375px) width.

    python3 preview.py OUT_DIR email1.html [email2.html ...]

Needs Playwright with Chromium (pre-installed under /opt/pw-browsers in Claude Code on the web). The GHL-hosted
logo, avatar and uploaded images won't load in a sandbox, and merge fields show raw: both are expected.
"""
import asyncio
import glob
import os
import sys


async def main(out, files):
    from playwright.async_api import async_playwright
    os.makedirs(out, exist_ok=True)
    cands = glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome') or ['/opt/pw-browsers/chromium']
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=cands[0])
        for f in files:
            name = os.path.basename(f)[:-5]
            for tag, w in (('desktop', 700), ('phone', 375)):
                pg = await b.new_page(viewport={'width': w, 'height': 800})
                await pg.goto('file://' + os.path.abspath(f))
                await pg.wait_for_timeout(300)
                await pg.screenshot(path=os.path.join(out, '%s-%s.png' % (name, tag)), full_page=True)
                await pg.close()
        await b.close()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    asyncio.run(main(sys.argv[1], sys.argv[2:]))
