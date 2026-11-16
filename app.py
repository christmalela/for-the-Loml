from datetime import datetime
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

HTML_PAGE = """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>Pour Karolina 🌹</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      min-height: 100dvh;
      background: radial-gradient(circle at top, #2d0f1d 0%, #0d060a 100%);
      color: #fff5f8;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 20px;
      overflow: hidden;
      text-align: center;
    }
    canvas { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
    .card {
      position: relative;
      z-index: 1;
      max-width: 460px;
      width: 100%;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 143, 177, 0.22);
      backdrop-filter: blur(18px);
      -webkit-backdrop-filter: blur(18px);
      border-radius: 28px;
      padding: 32px 24px;
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.65);
    }
    .top-tag {
      font-size: 0.8rem;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      color: #ff9ebb;
      margin-bottom: 10px;
      font-weight: 600;
    }
    .badge {
      display: inline-block;
      font-size: 0.78rem;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: #ffd1dc;
      background: rgba(255, 77, 121, 0.18);
      border: 1px solid rgba(255, 117, 151, 0.35);
      padding: 6px 14px;
      border-radius: 999px;
      margin-bottom: 20px;
      transition: opacity 0.35s ease;
    }
    .message-box {
      min-height: 145px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 16px;
    }
    h1 {
      font-size: clamp(1.22rem, 4.6vw, 1.52rem);
      font-weight: 700;
      line-height: 1.45;
      transition: opacity 0.35s ease, transform 0.35s ease;
    }
    .fade-out { opacity: 0; transform: translateY(8px); }
    .subtext {
      font-size: 0.92rem;
      color: rgba(255, 245, 248, 0.72);
      line-height: 1.5;
      margin-bottom: 24px;
    }
    .actions { display: flex; flex-direction: column; gap: 12px; }
    button {
      width: 100%;
      padding: 15px 20px;
      border-radius: 16px;
      border: none;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      transition: transform 0.18s ease, box-shadow 0.2s ease, background 0.2s ease;
    }
    button:active { transform: scale(0.97); }
    .btn-primary {
      background: linear-gradient(135deg, #ff4d79 0%, #c9184a 100%);
      color: #ffffff;
      box-shadow: 0 10px 28px rgba(255, 77, 121, 0.35);
    }
    .btn-secondary {
      background: rgba(255, 255, 255, 0.08);
      color: #fff5f8;
      border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .modal {
      position: fixed;
      inset: 0;
      background: rgba(13, 6, 10, 0.95);
      backdrop-filter: blur(14px);
      z-index: 10;
      display: none;
      flex-direction: column;
      padding: 24px;
      overflow-y: auto;
    }
    .modal.open { display: flex; }
    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      max-width: 520px;
      width: 100%;
      margin: 0 auto 20px;
    }
    .grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 10px;
      max-width: 520px;
      width: 100%;
      margin: 0 auto 24px;
    }
    .lang-item {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 143, 177, 0.18);
      border-radius: 14px;
      padding: 14px 16px;
      text-align: left;
      line-height: 1.4;
      font-size: 0.95rem;
    }
    .lang-item small {
      display: block;
      color: #ff8fab;
      font-size: 0.75rem;
      font-weight: 600;
      margin-bottom: 4px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }
  </style>
</head>
<body>
  <canvas id="fx"></canvas>

  <main class="card">
    <div class="top-tag">✨ For Karolina · 2026 ✨</div>
    <div class="badge" id="lang-label">Français</div>
    <div class="message-box">
      <h1 id="love-text">Karolina, je t'aime beaucoup. Tu es ma plus belle rencontre de 2026, tu es belle, intelligente et très forte.</h1>
    </div>
    <p class="subtext" id="subtext">
      In every language in the world, you are extraordinary.
    </p>
    <div class="actions">
      <button class="btn-primary" id="love-btn">Send a shower of roses 🌹</button>
      <button class="btn-secondary" id="all-btn">Read in all languages (incl. Lingala)</button>
    </div>
  </main>

  <div class="modal" id="modal">
    <div class="modal-header">
      <strong>For Karolina — In All Languages 🌹</strong>
      <button class="btn-secondary" style="width:auto;padding:8px 14px;" id="close-btn">Close</button>
    </div>
    <div class="grid" id="lang-grid"></div>
  </div>

  <script>
    const translations = [
      {
        lang: "Français",
        text: "Karolina, je t'aime beaucoup. Tu es ma plus belle rencontre de 2026, tu es belle, intelligente et très forte."
      },
      {
        lang: "Lingala",
        text: "Karolina, nalingi yo mingi. Ozali bokutani na ngai ya kitoko koleka na 2026, ozali kitoko, ya mayele mpe ya makasi mingi."
      },
      {
        lang: "Polski",
        text: "Karolina, bardzo Cię kocham. Jesteś moim najpiękniejszym spotkaniem 2026 roku, jesteś piękna, inteligentna i bardzo silna."
      },
      {
        lang: "English",
        text: "Karolina, I love you so much. You are my most beautiful encounter of 2026, you are beautiful, intelligent, and so strong."
      },
      {
        lang: "Español",
        text: "Karolina, te quiero mucho. Eres mi encuentro más hermoso de 2026, eres bella, inteligente y muy fuerte."
      },
      {
        lang: "Italiano",
        text: "Karolina, ti amo tantissimo. Sei il mio incontro più bello del 2026, sei bellissima, intelligente e molto forte."
      },
      {
        lang: "Português",
        text: "Karolina, eu te amo muito. Você é o meu encontro mais lindo de 2026, você é linda, inteligente e muito forte."
      },
      {
        lang: "Deutsch",
        text: "Karolina, ich liebe dich sehr. Du bist meine schönste Begegnung 2026, du bist wunderschön, intelligent und sehr stark."
      },
      {
        lang: "العربية",
        text: "كارولينا، أحبك كثيراً. أنتِ أجمل لقاء لي في عام 2026، أنتِ جميلة وذكية وقوية جداً."
      },
      {
        lang: "日本語",
        text: "カロリナ、とても愛しています。あなたは2026年で最も素晴らしい出会いで、美しくて賢くてとても強い人です。"
      },
      {
        lang: "한국어",
        text: "카롤리나, 정말 많이 사랑해. 넌 2026년 나의 가장 아름다운 만남이고, 아름답고 똑똑하며 정말 강한 사람이야."
      },
      {
        lang: "中文",
        text: "卡罗琳娜，我非常爱你。你是我2026年最美好的相遇，你美丽、聪明又非常坚强。"
      },
      {
        lang: "Русский",
        text: "Каролина, я тебя очень люблю. Ты моя самая прекрасная встреча 2026 года, ты красивая, умная и очень сильная."
      },
      {
        lang: "Türkçe",
        text: "Karolina, seni çok seviyorum. 2026'daki en güzel karşılaşmamsın; çok güzel, zeki ve çok güçlüsün."
      },
      {
        lang: "Nederlands",
        text: "Karolina, ik hou heel veel van je. Je bent mijn mooiste ontmoeting van 2026, je bent mooi, intelligent en heel sterk."
      },
      {
        lang: "Ελληνικά",
        text: "Καρολίνα, σ' αγαπώ πολύ. Είσαι η πιο όμορφη συνάντησή μου το 2026, είσαι όμορφη, έξυπνη και πολύ δυνατή."
      },
      {
        lang: "Svenska",
        text: "Karolina, jag älskar dig så mycket. Du är mitt vackraste möte 2026, du är vacker, intelligent och väldigt stark."
      },
      {
        lang: "Kiswahili",
        text: "Karolina, nakupenda sana. Wewe ni mkutano wangu mzuri zaidi wa 2026, wewe ni mrembo, mwenye akili na mwenye nguvu sana."
      }
    ];

    let index = 0;
    const langEl = document.getElementById("lang-label");
    const textEl = document.getElementById("love-text");

    setInterval(() => {
      langEl.classList.add("fade-out");
      textEl.classList.add("fade-out");
      setTimeout(() => {
        index = (index + 1) % translations.length;
        langEl.textContent = translations[index].lang;
        textEl.textContent = translations[index].text;
        langEl.classList.remove("fade-out");
        textEl.classList.remove("fade-out");
      }, 350);
    }, 3400);

    const grid = document.getElementById("lang-grid");
    translations.forEach(item => {
      const div = document.createElement("div");
      div.className = "lang-item";
      div.innerHTML = `<small>${item.lang}</small><div>${item.text}</div>`;
      grid.appendChild(div);
    });

    document.getElementById("all-btn").onclick = () => document.getElementById("modal").classList.add("open");
    document.getElementById("close-btn").onclick = () => document.getElementById("modal").classList.remove("open");

    // Particules lumineuses + Pluie de roses
    const canvas = document.getElementById("fx");
    const ctx = canvas.getContext("2d");
    let particles = [];

    function resize() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    window.addEventListener("resize", resize);
    resize();

    for (let i = 0; i < 45; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 2.2 + 1,
        vy: -(Math.random() * 0.5 + 0.2),
        vx: (Math.random() - 0.5) * 0.3
      });
    }

    function burstRoses() {
      for (let i = 0; i < 80; i++) {
        particles.push({
          x: Math.random() * canvas.width,
          y: -Math.random() * 350 - 20,
          r: Math.random() * 16 + 16,
          vy: Math.random() * 2.4 + 1.4,
          vx: (Math.random() - 0.5) * 1.2,
          isRose: true
        });
      }
    }

    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      particles.forEach(p => {
        p.y += p.vy;
        p.x += p.vx || 0;
        if (p.isRose) {
          if (p.y > canvas.height + 30) {
            p.y = -30;
            p.x = Math.random() * canvas.width;
          }
          ctx.font = `${p.r}px serif`;
          ctx.fillText("🌹", p.x, p.y);
        } else {
          if (p.y < -30) {
            p.y = canvas.height + 20;
            p.x = Math.random() * canvas.width;
          }
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
          ctx.fillStyle = "rgba(255, 117, 151, 0.38)";
          ctx.fill();
        }
      });
      requestAnimationFrame(animate);
    }
    animate();

    document.getElementById("love-btn").onclick = async function () {
      this.textContent = "Roses sent for Karolina 🌹✨";
      document.getElementById("subtext").textContent = "You deserve all the roses in the world, Karolina.";
      burstRoses();
      try {
        await fetch("/api/roses", { method: "POST" });
      } catch (e) {}
    };
  </script>
</body>
</html>"""


def enregistrer_evenement(message: str):
  horodatage = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
  print(f"[{horodatage}] {message}", flush=True)


@app.route("/")
def accueil():
  appareil = request.headers.get("User-Agent", "Inconnu")
  source = "Instagram DM" if "Instagram" in appareil else "Navigateur"
  enregistrer_evenement(f"👀 Karolina a ouvert le lien via {source}")
  return render_template_string(HTML_PAGE)


@app.route("/api/roses", methods=["POST"])
def roses():
  enregistrer_evenement(
      "🌹 SUCCÈS : Karolina a déclenché la pluie de roses !"
  )
  return jsonify({"status": "ok"})


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5002)
