#!/usr/bin/env python3
"""Bygger den installerbare nettappen (PWA) av Matplan.

Bruk:  python3 build_pwa.py            (leser matplan.html, skriver til docs/)
Kilden er matplan.html. docs/ kan publiseres som den er, f.eks. med GitHub Pages
(Settings > Pages > Deploy from branch > main /docs) eller Netlify Drop.
"""
import hashlib, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "matplan.html"
OUT = ROOT / "docs"

HERB, BG, LEAF_LIGHT = "#2E6A4E", "#EFF2EC", "#FFFFFF"


def make_icons():
    from PIL import Image, ImageDraw
    (OUT / "icons").mkdir(parents=True, exist_ok=True)

    def draw(size, maskable):
        S = size * 4  # supersampling
        im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        if maskable:
            d.rectangle([0, 0, S, S], fill=HERB)
            scale = 0.58          # innhold innenfor trygg sone (80 %)
        else:
            d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.22), fill=HERB)
            scale = 0.72
        c = S / 2
        R = S * scale / 2
        w = max(2, int(R * 0.13))
        d.ellipse([c - R, c - R, c + R, c + R], outline=LEAF_LIGHT, width=w)
        r2 = R * 0.56
        d.ellipse([c - r2, c - r2, c + r2, c + r2], fill=(83, 133, 110, 255))
        # blad: to sirkelbuer som danner en mandelform, pluss stilk
        lw, lh = R * 0.42, R * 0.62
        top = c - R * 0.52
        pts = []
        import math
        for i in range(0, 181, 6):
            t = math.radians(i)
            pts.append((c + math.sin(t) * lw * 0.55 * math.sin(t) ** 0.2, top + (1 - math.cos(t)) / 2 * lh))
        for i in range(180, -1, -6):
            t = math.radians(i)
            pts.append((c - math.sin(t) * lw * 0.55 * math.sin(t) ** 0.2, top + (1 - math.cos(t)) / 2 * lh))
        d.polygon(pts, fill=LEAF_LIGHT)
        d.line([(c, top + lh * 0.92), (c, top + lh + R * 0.36)], fill=LEAF_LIGHT, width=int(w * 0.85))
        return im.resize((size, size), Image.LANCZOS)

    files = {}
    for size in (192, 512):
        p = OUT / "icons" / f"icon-{size}.png"
        draw(size, False).save(p)
        files[f"icons/icon-{size}.png"] = p
    for size in (192, 512):
        p = OUT / "icons" / f"maskable-{size}.png"
        draw(size, True).save(p)
        files[f"icons/maskable-{size}.png"] = p
    p = OUT / "icons" / "apple-touch-icon.png"
    draw(180, True).save(p)
    files["icons/apple-touch-icon.png"] = p
    return files


MANIFEST = {
    "name": "Matplan",
    "short_name": "Matplan",
    "description": "Meny og handleliste for en periode ut fra budsjett, tid og ernæring, med logg over hva du har spist.",
    "lang": "nb",
    "dir": "ltr",
    "start_url": "./?kilde=app",
    "scope": "./",
    "id": "./",
    "display": "standalone",
    "orientation": "portrait",
    "background_color": BG,
    "theme_color": HERB,
    "categories": ["food", "health", "lifestyle"],
    "icons": [
        {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "icons/maskable-192.png", "sizes": "192x192", "type": "image/png", "purpose": "maskable"},
        {"src": "icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
    "shortcuts": [
        {"name": "Handleliste", "url": "./#liste", "icons": [{"src": "icons/icon-192.png", "sizes": "192x192"}]},
        {"name": "Logg", "url": "./#logg", "icons": [{"src": "icons/icon-192.png", "sizes": "192x192"}]},
        {"name": "Trening", "url": "./#trening", "icons": [{"src": "icons/icon-192.png", "sizes": "192x192"}]},
    ],
}

HEAD = """<!doctype html>
<html lang="nb">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#2E6A4E">
<meta name="color-scheme" content="light dark">
<meta name="description" content="{desc}">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="mobile-web-app-capable" content="yes">
<style>
:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}
html,body{{margin:0}}
body{{font:14px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif;-webkit-tap-highlight-color:transparent;overscroll-behavior-y:contain}}
img{{max-width:100%}}
</style>
"""

BOOT = """
<script>
/* Installerbar app: offline-støtte, varig lagring og snarveier */
(function(){
  if("serviceWorker" in navigator&&location.protocol!=="file:"){
    var hadCtl=!!navigator.serviceWorker.controller,shown=false;
    function banner(){
      if(shown)return;shown=true;
      var b=document.createElement("div");
      b.setAttribute("role","status");
      b.style.cssText="position:fixed;left:12px;right:12px;bottom:calc(84px + env(safe-area-inset-bottom,0px));z-index:9999;display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:14px;background:#1f2a24;color:#fff;font:14px/1.35 system-ui,sans-serif;box-shadow:0 6px 24px rgba(0,0,0,.25)";
      b.innerHTML='<span style="flex:1">Ny versjon av Matplan er klar.</span><button style="border:0;border-radius:999px;padding:8px 14px;background:#fff;color:#1f2a24;font:600 14px system-ui,sans-serif">Oppdater</button>';
      b.querySelector("button").onclick=function(){location.reload()};
      document.body.appendChild(b);
    }
    navigator.serviceWorker.addEventListener("controllerchange",function(){if(hadCtl)banner();hadCtl=true});
    window.addEventListener("load",function(){
      navigator.serviceWorker.register("sw.js",{updateViaCache:"none"}).then(function(reg){
        function check(){reg.update().catch(function(){})}
        document.addEventListener("visibilitychange",function(){if(document.visibilityState==="visible")check()});
        setInterval(check,30*60*1000);
      }).catch(function(e){console.warn("Service worker:",e)});
    });
  }
  try{if(navigator.storage&&navigator.storage.persist)navigator.storage.persist()}catch(e){}
  function fromHash(){var h=(location.hash||"").slice(1);if(["meny","liste","logg","trening","oppsett"].indexOf(h)>=0){try{setTab(h)}catch(e){}}}
  fromHash();window.addEventListener("hashchange",fromHash);
})();
</script>
"""

SW = """/* Matplan service worker – versjon {version} */
const CACHE = "matplan-{version}";
const SHELL = {shell};
self.addEventListener("install", e => {{
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL.map(u => new Request(u, {{cache: "reload"}})))).then(() => self.skipWaiting()));
}});
self.addEventListener("message", e => {{ if (e.data === "skipWaiting") self.skipWaiting(); }});
self.addEventListener("activate", e => {{
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith("matplan-") && k !== CACHE && k !== "matplan-fonts").map(k => caches.delete(k)))).then(() => self.clients.claim()));
}});
self.addEventListener("fetch", e => {{
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.hostname === "fonts.googleapis.com" || url.hostname === "fonts.gstatic.com") {{
    e.respondWith(caches.open("matplan-fonts").then(async c => {{
      const hit = await c.match(req);
      const net = fetch(req).then(r => {{ if (r.ok || r.type === "opaque") c.put(req, r.clone()); return r; }}).catch(() => hit);
      return hit || net;
    }}));
    return;
  }}
  if (url.origin !== location.origin) return;
  if (req.mode === "navigate") {{
    e.respondWith(fetch(req.url, {{cache: "no-store"}}).then(r => {{ if (!r.ok) throw r; const copy = r.clone(); caches.open(CACHE).then(c => c.put("./", copy)); return r; }})
      .catch(() => caches.match("./", {{ignoreSearch: true}}).then(r => r || caches.match("index.html"))));
    return;
  }}
  e.respondWith(caches.match(req, {{ignoreSearch: true}}).then(hit => hit || fetch(req)));
}});
"""


def main():
    src = SRC.read_text(encoding="utf-8")
    src = re.sub(r'^<meta charset="utf-8">\s*', "", src)
    OUT.mkdir(exist_ok=True)
    icons = make_icons()
    (OUT / "manifest.webmanifest").write_text(json.dumps(MANIFEST, ensure_ascii=False, indent=2), encoding="utf-8")

    # <title>, fonter og <style> fra kilden flyttes inn i <head>
    m = re.search(r"(<title>.*?</style>)", src, re.S)
    head_part, body_part = m.group(1), src[m.end():]
    html = (HEAD.format(desc=MANIFEST["description"]) + head_part + "\n</head>\n<body>\n" +
            body_part.strip() + "\n" + BOOT + "</body>\n</html>\n")
    (OUT / "index.html").write_text(html, encoding="utf-8")

    shell = ["./", "index.html", "manifest.webmanifest"] + sorted(icons)
    h = hashlib.sha256()
    for f in ["index.html", "manifest.webmanifest"] + sorted(icons):
        h.update((OUT / f).read_bytes())
    version = h.hexdigest()[:10]
    (OUT / "sw.js").write_text(SW.format(version=version, shell=json.dumps(shell)), encoding="utf-8")
    (OUT / ".nojekyll").write_text("")
    print(f"Bygget docs/ (versjon {version})")


if __name__ == "__main__":
    sys.exit(main())
