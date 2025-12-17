import requests, time

def kol_bomb():
    print("Base — KOL Mention Bomb (Twitter mentions explode while volume still low)")
    history = {}

    while True:
        try:
            r = requests.get("https://api.dexscreener.com/latest/dex/pairs/base")
            now = time.time()

            for pair in r.json().get("pairs", []):
                addr = pair["pairAddress"]
                mentions = pair.get("socials", {}).get("twitterMentions", 0) or 0
                vol = pair.get("volume", {}).get("h5", 0) or 0

                if addr not in history:
                    history[addr] = (now, mentions, vol)
                    continue

                last_t, last_mentions, last_vol = history[addr]
                if now - last_t > 300:  # reset old
                    history[addr] = (now, mentions, vol)
                    continue

                mention_spike = mentions / last_mentions if last_mentions > 0 else mentions
                if mention_spike > 20 and vol < 50_000:  # mentions 20x, volume still quiet
                    token = pair["baseToken"]["symbol"]
                    print(f"KOL MENTION BOMB\n"
                          f"{token} Twitter mentions ×{mention_spike:.0f}\n"
                          f"Volume still ${vol:,.0f} — hype before money\n"
                          f"https://dexscreener.com/base/{addr}\n"
                          f"→ Influencers pumping — volume coming soon\n"
                          f"{'BOMB'*30}")

                history[addr] = (now, mentions, vol)

        except:
            pass
        time.sleep(7.2)

if __name__ == "__main__":
    kol_bomb()
