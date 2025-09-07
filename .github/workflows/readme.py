import requests
import random
import re
from datetime import datetime, timezone

fallback_quotes = [
    # Indonesia
    "Hidup adalah perjuangan tanpa akhir. – Soekarno",
    "Bermimpilah setinggi langit, jika engkau jatuh, engkau akan jatuh di antara bintang-bintang. – Soekarno",
    "Kesuksesan hanya bisa diraih dengan kerja keras dan doa. – BJ Habibie",
    "Cintailah produk-produk Indonesia. – BJ Habibie",
    "Tidak ada hasil yang mengkhianati usaha. – Unknown",
    "Jangan menunggu kesempatan, ciptakanlah kesempatan itu sendiri. – Unknown",
    "Lebih baik menjadi lilin kecil yang memberi cahaya daripada kutuk dalam kegelapan. – Unknown",
    "Pendidikan adalah senjata paling ampuh untuk mengubah dunia. – Nelson Mandela",
    "Orang bijak belajar ketika mereka bisa. Orang bodoh belajar ketika mereka terpaksa. – Pepatah Arab",
    "Waktu adalah pedang. Jika kamu tidak menggunakannya dengan benar, ia akan memotongmu. – Pepatah Arab",

    # Internasional
    "Do what you can, with what you have, where you are. – Theodore Roosevelt",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. – Winston Churchill",
    "In the middle of every difficulty lies opportunity. – Albert Einstein",
    "Your time is limited, so don’t waste it living someone else’s life. – Steve Jobs",
    "Happiness depends upon ourselves. – Aristotle",
    "It does not matter how slowly you go as long as you do not stop. – Confucius",
    "Everything you can imagine is real. – Pablo Picasso",
    "Do one thing every day that scares you. – Eleanor Roosevelt",
    "Turn your wounds into wisdom. – Oprah Winfrey",
    "Fall seven times and stand up eight. – Japanese Proverb",
    "Act as if what you do makes a difference. It does. – William James",
    "It always seems impossible until it’s done. – Nelson Mandela",
]

def get_quote():
    try:
        res = requests.get("https://api.quotable.io/random", timeout=10)
        res.raise_for_status()
        data = res.json()
        return f"{data['content']} – {data['author']}"
    except Exception as e:
        print(f"[!] Gagal ambil dari API, pakai fallback. Error: {e}")
        return random.choice(fallback_quotes)

quote = get_quote()
today = datetime.now(timezone.utc).strftime("%d %B %Y")

with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

new_content = []
inside = False
for line in content.splitlines():
    if "<!--START_QUOTE-->" in line:
        new_content.append(line)
        new_content.append(f"📅 {today}")
        new_content.append("")
        new_content.append(f"> {quote}")
        inside = True
    elif "<!--END_QUOTE-->" in line:
        inside = False
        new_content.append(line)
    elif not inside:
        new_content.append(line)

with open("README.md", "w", encoding="utf-8") as f:
    f.write("\n".join(new_content))
