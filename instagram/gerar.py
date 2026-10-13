"""Gera as artes do Instagram do Sono Perfeito (HTML -> PNG via Chrome headless).

Uso:  python gerar.py
Saída: instagram/png/*.png
"""
import subprocess
from pathlib import Path

AQUI = Path(__file__).resolve().parent
HTML = AQUI / "html"
PNG = AQUI / "png"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ICONE = (AQUI.parent / "site" / "icon.svg").as_uri()

# ícones em traço, no estilo do app
I = {
    "moon": '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
    "drop": '<path d="M12 3s-6 7-6 11a6 6 0 0 0 12 0c0-4-6-11-6-11z"/>',
    "thermo": '<path d="M10 14V5a2 2 0 1 1 4 0v9a4 4 0 1 1-4 0z"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "tv": '<rect x="3" y="5" width="18" height="12" rx="2"/><path d="M8 21h8"/>',
    "snow": '<path d="M12 2v20M3.3 7l17.4 10M20.7 7L3.3 17"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7"/>',
    "wave": '<circle cx="12" cy="12" r="2"/><path d="M7.8 7.8a6 6 0 0 0 0 8.4M16.2 7.8a6 6 0 0 1 0 8.4M4.9 4.9a10 10 0 0 0 0 14.2M19.1 4.9a10 10 0 0 1 0 14.2"/>',
    "phone": '<rect x="6" y="2" width="12" height="20" rx="3"/><path d="M11 18h2"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/>',
}


def ic(nome, cls=""):
    return (f'<svg class="i {cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{I[nome]}</svg>')


def gauge(valor, rotulo, cor, pct, icone):
    off = 314 * (1 - pct)
    return f'''<div class="gauge"><svg viewBox="0 0 120 120"><circle class="g-bg" cx="60" cy="60" r="50"/>
      <circle cx="60" cy="60" r="50" fill="none" stroke="{cor}" stroke-width="8" stroke-linecap="round"
      stroke-dasharray="314" stroke-dashoffset="{off:.0f}" transform="rotate(-90 60 60)"/></svg>
      <div class="g-val"><span style="color:{cor}">{ic(icone)}</span><b>{valor}</b><small>{rotulo}</small></div></div>'''


CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:__W__;height:__H__;overflow:hidden}
body{font-family:"Manrope",sans-serif;color:#eef0ff;-webkit-font-smoothing:antialiased;position:relative}
em{font-family:"Instrument Serif",serif;font-style:italic;font-weight:400}
.i{width:1em;height:1em;display:inline-block;vertical-align:-.12em}
.dark{background:radial-gradient(120% 90% at 60% 60%,#121a5a 0%,#070a1f 62%)}
.aurora::before{content:"";position:absolute;inset:-20%;background:
  radial-gradient(40% 30% at 30% 50%,rgba(90,100,255,.55),transparent 70%),
  radial-gradient(35% 25% at 70% 42%,rgba(70,180,200,.22),transparent 70%),
  radial-gradient(50% 30% at 55% 62%,rgba(120,80,230,.35),transparent 70%);filter:blur(40px)}
.stars{position:absolute;inset:0;opacity:.75;background-image:
  radial-gradient(2px 2px at 10% 20%,#fff,transparent),radial-gradient(1.5px 1.5px at 30% 70%,#fff,transparent),
  radial-gradient(2.4px 2.4px at 72% 28%,#fff,transparent),radial-gradient(1.5px 1.5px at 85% 80%,#fff,transparent),
  radial-gradient(2px 2px at 55% 10%,#fff,transparent),radial-gradient(1.5px 1.5px at 18% 88%,#fff,transparent),
  radial-gradient(1.6px 1.6px at 92% 45%,#fff,transparent),radial-gradient(2px 2px at 44% 52%,#fff,transparent),
  radial-gradient(1.4px 1.4px at 64% 92%,#fff,transparent),radial-gradient(1.8px 1.8px at 5% 50%,#fff,transparent)}
.light{background:radial-gradient(80% 60% at 80% 0%,#f8f9fc,#eef0f5);color:#1f2540}
.morning{background:linear-gradient(180deg,#8fb0f2 0%,#c9d8f6 55%,#f1dfd2 100%);color:#1f2540}
.pad{position:absolute;inset:0;padding:96px 88px;display:flex;flex-direction:column;z-index:2}
.brand{display:flex;align-items:center;gap:16px;font-weight:800;font-size:30px;letter-spacing:-.01em}
.brand img{width:52px;height:52px;border-radius:14px}
.foot{margin-top:auto;display:flex;justify-content:space-between;align-items:center;font-size:26px;font-weight:600;opacity:.7}
.eyebrow{font-size:28px;font-weight:700;opacity:.65;letter-spacing:.02em}
h1{font-weight:800;letter-spacing:-.035em;line-height:1.02}
.glow{text-shadow:0 0 50px rgba(180,190,255,.5)}
.blue{color:#9fb0ff}
.card{background:rgba(18,24,64,.6);border:1.5px solid rgba(160,175,255,.2);border-radius:44px;backdrop-filter:blur(20px)}
.wcard{background:rgba(255,255,255,.82);border:2px solid #fff;border-radius:44px;box-shadow:0 40px 90px -40px rgba(40,50,90,.4)}
.gauge{position:relative;width:250px;aspect-ratio:1}
.gauge>svg{width:100%;height:100%}
.g-bg{fill:rgba(18,24,60,.9);stroke:rgba(255,255,255,.08);stroke-width:8}
.g-val{position:absolute;inset:0;display:grid;place-content:center;text-align:center;line-height:1.1}
.g-val span{font-size:26px} .g-val b{font-size:52px;font-weight:800;letter-spacing:-.02em} .g-val small{font-size:20px;opacity:.6}
.row{display:flex;align-items:center;justify-content:space-between;padding:30px 36px;border-radius:30px;
  background:rgba(255,255,255,.06);border:1.5px solid rgba(255,255,255,.09);font-size:36px;font-weight:700}
.row .l{display:flex;align-items:center;gap:20px}
.ok{width:46px;height:46px;border-radius:50%;border:2.5px solid #9fb0ff;color:#9fb0ff;display:grid;place-items:center;font-size:26px}
.pillbtn{display:inline-flex;align-items:center;gap:22px;padding:30px 48px;border-radius:99px;background:#f7f8fb;color:#5b6cf0;
  font-weight:800;font-size:42px;box-shadow:0 0 70px rgba(150,170,255,.5)}
.pillbtn .sep{width:2px;height:40px;background:#e3e6ee}
.chip{display:inline-block;padding:18px 30px;border-radius:99px;background:#fff;font-size:30px;color:#5b6182;
  box-shadow:inset 0 1px 0 #fff,0 12px 30px -14px rgba(40,50,90,.3)}
.chip.on{background:#e3e8ff;color:#5b6cf0;font-weight:800}
"""

HEAD = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Instrument+Serif:ital@0;1&display=block" rel="stylesheet">
<style>{css}{extra}</style></head><body class="{body}">"""

BRAND = f'<div class="brand"><img src="{ICONE}" alt=""><span>Sono Perfeito</span></div>'
FOOT = '<div class="foot"><span>sonoperfeito.app</span><span>{dir}</span></div>'

POSTS = {}

# 1. Lançamento / apresentação
POSTS["01-apresentacao"] = dict(body="dark aurora", extra="""
.c{margin:auto;text-align:center}
.c img{width:230px;border-radius:30%;box-shadow:0 0 0 2px rgba(255,255,255,.2),0 0 110px rgba(140,160,255,.65)}
.c h1{font-size:128px;margin-top:56px}
.c p{font-size:78px;margin-top:22px}
.c .k{font-size:26px;letter-spacing:.32em;text-transform:uppercase;opacity:.6;margin-top:40px}
""", html=f"""<div class="stars"></div><div class="pad">
<div class="c"><img src="{ICONE}" alt="">
<h1 class="glow">Sono Perfeito</h1>
<p><em>Respire melhor.</em> <em class="blue">Durma melhor.</em></p>
<p class="k">Temperatura · Umidade · Luz</p></div>
{FOOT.format(dir="")}</div>""")

# 2. O problema
POSTS["02-o-problema"] = dict(body="dark", extra="""
.moon{position:absolute;right:110px;top:150px;font-size:230px;color:#f1efe6;filter:drop-shadow(0 0 60px rgba(220,225,255,.7))}
.moon .i{stroke:none;fill:currentColor}
.lines{margin-top:250px}
.lines p{font-size:92px;font-weight:800;letter-spacing:-.03em;line-height:1.15;color:#d8dbe8}
.lines b{color:#fff}
.lines .cold{color:#8fd3ff;text-shadow:0 0 40px rgba(120,200,255,.7)}
.chips{display:flex;gap:18px;margin-top:40px}
.chips span{padding:16px 28px;border-radius:99px;background:rgba(255,255,255,.08);border:1.5px solid rgba(255,255,255,.14);font-size:30px;font-weight:600}
.q{margin-top:auto;margin-bottom:60px;font-family:"Instrument Serif",serif;font-style:italic;font-size:70px;line-height:1.1}
.q span{color:#b9c4ff}
""", html=f"""<div class="stars"></div><div class="moon">{ic("moon")}</div><div class="pad">
{BRAND}
<div class="lines"><p>Nariz <b>entupido.</b></p><p>Garganta <b>seca.</b></p><p>O quarto <b class="cold">frio demais.</b></p></div>
<div class="chips"><span style="color:#ff9b9b">{ic("thermo")} 17°</span><span style="color:#8fd3ff">{ic("drop")} 28% umidade</span><span>03:12</span></div>
<p class="q">E se o quarto se <span>ajustasse sozinho</span> enquanto você dorme?</p>
{FOOT.format(dir="")}</div>""")

# 3. Como funciona
POSTS["03-como-funciona"] = dict(body="light", extra="""
.light .foot{opacity:.55}
h1{font-size:118px;margin-top:70px}
.steps{display:grid;gap:24px;margin-top:48px}
.st{display:flex;align-items:center;gap:36px;padding:30px 40px}
.ico{position:relative;flex:none;width:116px;height:116px;border-radius:50%;background:#f7f8fb;display:grid;place-items:center;font-size:52px;color:#5b6cf0;
  box-shadow:inset 0 1px 0 #fff,0 14px 34px -14px rgba(40,50,90,.35)}
.n{position:absolute;top:-6px;right:-6px;width:46px;height:46px;border-radius:50%;background:#5b6cf0;color:#fff;font-size:24px;font-weight:800;display:grid;place-items:center}
.st h3{font-size:46px;font-weight:800;letter-spacing:-.01em}
.st p{font-size:29px;color:#5b6182;line-height:1.45;margin-top:6px}
""", html=f"""<div class="pad">
{BRAND}
<p class="eyebrow" style="margin-top:56px">como funciona</p>
<h1 style="margin-top:14px">Mede. Decide.<br><em style="color:#5b6cf0">Ajusta.</em></h1>
<div class="steps">
 <div class="st wcard"><div class="ico">{ic("wave")}<span class="n">1</span></div><div><h3>Mede</h3><p>Um sensor em cada cômodo acompanha temperatura, umidade e luz.</p></div></div>
 <div class="st wcard"><div class="ico">{ic("phone")}<span class="n">2</span></div><div><h3>Decide</h3><p>O app compara com a faixa que você escolheu.</p></div></div>
 <div class="st wcard"><div class="ico">{ic("gear")}<span class="n">3</span></div><div><h3>Ajusta</h3><p>Ar, umidificador, luz e TV — sem você levantar.</p></div></div>
</div>
{FOOT.format(dir="")}</div>""")

# 4. Hora de dormir
POSTS["04-hora-de-dormir"] = dict(body="dark", extra="""
h1{font-size:88px;margin-top:56px}
.btnwrap{margin-top:44px}
.clock{font-size:128px;font-weight:300;letter-spacing:-.02em;margin:28px 0 30px;font-variant-numeric:tabular-nums;opacity:.95}
.list{display:grid;gap:16px}
.list .row{padding:22px 32px;font-size:33px}
""", html=f"""<div class="stars"></div><div class="pad">
{BRAND}
<h1 class="glow">Um toque.<br><em class="blue">Boa noite.</em></h1>
<div class="btnwrap"><span class="pillbtn">{ic("moon")} Hora de dormir <span class="sep"></span>{ic("gear")}</span></div>
<div class="clock">22:30</div>
<div class="list">
 <div class="row"><span class="l"><span style="color:#ffb648">{ic("sun")}</span>Luz quente a 2700K</span><span class="ok">{ic("check")}</span></div>
 <div class="row"><span class="l"><span style="color:#8fd3ff">{ic("snow")}</span>Ar em 23°</span><span class="ok">{ic("check")}</span></div>
 <div class="row"><span class="l"><span style="color:#4c8dff">{ic("drop")}</span>Umidificador ligado</span><span class="ok">{ic("check")}</span></div>
 <div class="row"><span class="l"><span style="color:#c4c9e6">{ic("tv")}</span>TV desligada</span><span class="ok">{ic("check")}</span></div>
</div>
{FOOT.format(dir="")}</div>""")

# 5. Luz e melatonina
POSTS["05-luz-e-melatonina"] = dict(body="dark", extra="""
.warm{position:absolute;left:50%;top:44%;width:900px;height:900px;margin:-450px;border-radius:50%;
  background:radial-gradient(circle,rgba(255,182,72,.28),transparent 65%)}
.bulb{width:250px;height:250px;border-radius:50%;margin:150px auto 0;background:radial-gradient(circle at 40% 35%,#fff7e3,#ffc56a);
  box-shadow:0 0 90px #ffb648,0 0 200px rgba(255,182,72,.6)}
.k{text-align:center;font-size:44px;font-weight:800;color:#ffcf85;margin-top:44px;letter-spacing:.04em}
h1{font-size:84px;text-align:center;margin-top:60px}
.t{font-size:34px;line-height:1.5;text-align:center;color:#c4c9e6;margin:30px auto 0;max-width:820px}
""", html=f"""<div class="warm"></div><div class="pad">
{BRAND}
<div class="bulb"></div>
<p class="k">2700K</p>
<h1>Luz quente à noite,<br><em style="color:#ffcf85">sono mais cedo.</em></h1>
<p class="t">Quando escurece, o corpo libera melatonina, o sinal de que é hora de dormir. O Sono Perfeito deixa a luz quente e mais fraca no fim do dia.</p>
{FOOT.format(dir="")}</div>""")

# 6. Medidores
POSTS["06-quarto-no-ponto"] = dict(body="dark aurora", extra="""
h1{font-size:104px;margin-top:100px}
.panel{margin-top:80px;padding:56px 50px}
.ph{display:flex;justify-content:space-between;font-size:30px;font-weight:700;color:#c4c9e6}
.ph .clk{color:#ff5a6e;background:#2a0d14;padding:6px 18px;border-radius:12px;font-variant-numeric:tabular-nums}
.gs{display:flex;justify-content:space-between;margin-top:50px}
""", html=f"""<div class="stars"></div><div class="pad">
{BRAND}
<h1 class="glow">Seu quarto no ponto.<br><em class="blue">A noite inteira.</em></h1>
<div class="panel card">
 <div class="ph"><span>Quarto · agora</span><span class="clk">03:12</span></div>
 <div class="gs">{gauge("23°", "temperatura", "#ef5b5b", .55, "thermo")}{gauge("55%", "umidade", "#4c8dff", .55, "drop")}{gauge("2700K", "luz", "#ffb648", .78, "sun")}</div>
</div>
{FOOT.format(dir="")}</div>""")

# 7. Como foi sua noite
POSTS["07-como-foi-sua-noite"] = dict(body="morning", extra="""
.sun{position:absolute;right:110px;top:150px;width:210px;height:210px;border-radius:50%;background:#f2bf7c;box-shadow:0 0 120px rgba(255,200,120,.7)}
.dunes{position:absolute;left:0;bottom:0;width:100%;height:330px}
.morning .foot{position:relative;z-index:3;color:#2a3170;opacity:.8}
.tt{font-size:110px;color:#2a3170;margin-top:90px}
.fb{padding:56px;margin-top:60px;position:relative;z-index:3}
.fb h3{font-size:58px;font-weight:800;display:flex;gap:20px;align-items:center}
.fb small{display:block;font-size:26px;color:#8b90a8;margin-top:8px}
.chips{display:flex;flex-wrap:wrap;gap:18px;margin-top:40px}
.send{margin-top:44px;text-align:right}
.send span{display:inline-block;padding:20px 50px;border-radius:99px;background:#e3e8ff;color:#5b6cf0;font-weight:800;font-size:32px}
.cap{position:relative;z-index:3;font-size:36px;font-weight:700;color:#2a3170;margin-top:56px}
""", html=f"""<div class="sun"></div>
<svg class="dunes" viewBox="0 0 1080 330" preserveAspectRatio="none"><path d="M0 150 C160 80 300 90 460 140 S760 60 1080 120 V330 H0Z" fill="#a7a3cf" opacity=".75"/><path d="M0 220 C180 170 360 250 560 205 S880 160 1080 215 V330 H0Z" fill="#d9bfb0"/></svg>
<div class="pad">
<div class="brand" style="color:#1f2540"><img src="{ICONE}" alt=""><span>Sono Perfeito</span></div>
<p class="tt"><em>De manhã,</em></p>
<div class="fb wcard">
 <h3><span style="color:#e9a64a">{ic("sun")}</span>Como foi sua noite?</h3>
 <small>Onde dormiu: Quarto</small>
 <div class="chips"><span class="chip on">Dormi bem</span><span class="chip">Frio</span><span class="chip">Calor</span><span class="chip">Ar seco</span><span class="chip">Nariz entupido</span><span class="chip">Acordei à noite</span></div>
 <div class="send"><span>Enviar</span></div>
</div>
<p class="cap">Cada resposta ajusta as próximas noites.</p>
{FOOT.format(dir="")}</div>""")

# Story 1080x1920 (deixa ~250px livres em cima e embaixo para a interface do Instagram)
STORY = dict(body="dark aurora", extra="""
.pad{padding:270px 90px 300px}
.c{margin:auto 0;text-align:center}
.c img{width:220px;border-radius:30%;box-shadow:0 0 0 2px rgba(255,255,255,.2),0 0 110px rgba(140,160,255,.65)}
.c h1{font-size:120px;margin-top:56px}
.c p{font-size:72px;margin-top:22px}
.c .t{font-size:38px;line-height:1.5;color:#c4c9e6;margin-top:56px}
.link{display:inline-block;margin-top:80px;padding:30px 56px;border-radius:99px;background:#fff;color:#1d2580;font-weight:800;font-size:40px;box-shadow:0 0 70px rgba(150,170,255,.55)}
""", html=f"""<div class="stars"></div><div class="pad"><div class="c">
<img src="{ICONE}" alt="">
<h1 class="glow">Sono Perfeito</h1>
<p><em>Respire melhor.</em> <em class="blue">Durma melhor.</em></p>
<p class="t">Temperatura, umidade e luz<br>no ritmo do seu sono.</p>
<span class="link">sonoperfeito.app</span>
</div></div>""")

# Foto de perfil 1080x1080 (o Instagram recorta em círculo)
PERFIL = dict(body="dark aurora", extra="""
.c{position:absolute;inset:0;display:grid;place-items:center;z-index:2}
.c img{width:560px;border-radius:30%;box-shadow:0 0 0 3px rgba(255,255,255,.2),0 0 160px rgba(140,160,255,.7)}
""", html=f"""<div class="c"><img src="{ICONE}" alt=""></div>""")


def escrever(nome, d, w, h):
    css = CSS.replace("__W__", f"{w}px").replace("__H__", f"{h}px")
    pagina = HEAD.format(css=css, extra=d["extra"], body=d["body"]) + d["html"] + "</body></html>"
    arq = HTML / f"{nome}.html"
    arq.write_text(pagina, encoding="utf-8")
    return arq


def render(arq, w, h):
    saida = PNG / f"{arq.stem}.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--virtual-time-budget=8000",
                    f"--window-size={w},{h}", f"--screenshot={saida}", arq.as_uri()],
                   check=True, capture_output=True)
    print("ok", saida.name)


if __name__ == "__main__":
    HTML.mkdir(exist_ok=True)
    PNG.mkdir(exist_ok=True)
    trabalhos = [(n, d, 1080, 1350) for n, d in POSTS.items()]
    trabalhos += [("story-01", STORY, 1080, 1920), ("perfil", PERFIL, 1080, 1080)]
    for nome, d, w, h in trabalhos:
        render(escrever(nome, d, w, h), w, h)
