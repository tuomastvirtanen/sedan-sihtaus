import ctypes
import random
import time
from datetime import datetime

# --- Windows API vakioita ---
VK_SCROLL = 0x91
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# SetThreadExecutionState liput
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

def estä_lepotila():
    """ Kertoo Windowsille, että järjestelmän ja näytön on pysyttävä päällä. """
    kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED)

def salli_lepotila():
    """ Palauttaa Windowsin normaalit virransäästöasetukset. """
    kernel32.SetThreadExecutionState(ES_CONTINUOUS)

def _key_event(vk: int):
    user32.keybd_event(vk, 0, 0, 0)
    user32.keybd_event(vk, 0, 2, 0)

def is_scrolllock_on() -> bool:
    return bool(user32.GetKeyState(VK_SCROLL) & 1)

def set_scrolllock(state_on: bool):
    if is_scrolllock_on() != state_on:
        _key_event(VK_SCROLL)

def scrolllock_on_for_one_second():
    original = is_scrolllock_on()
    set_scrolllock(True)
    time.sleep(1.0)
    set_scrolllock(original)

def fmt_elapsed(seconds: float) -> str:
    seconds = int(seconds)
    h, jäännös = divmod(seconds, 3600)
    m, s = divmod(jäännös, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def ask_runtime_minutes() -> int | None:
    try:
        value = input("Anna suoritusaika minuutteina (1–180), Enter = toistaiseksi: ").strip()
        if not value: return None
        minutes = int(value)
        if 1 <= minutes <= 180: return minutes
    except ValueError: pass
    return None

def main():
    runtime_minutes = ask_runtime_minutes()
    
    # Aktivoidaan lepotilan esto heti alussa
    estä_lepotila()

    start_dt = datetime.now()
    start_mono = time.monotonic()
    end_time = (start_mono + runtime_minutes * 60) if runtime_minutes else None

    next_print = start_mono + 5 * 60
    next_toggle = start_mono + random.uniform(3 * 60, 5 * 60)

    print(f"Aloitettu: {start_dt.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Suoritusaika: {f'{runtime_minutes} min' if runtime_minutes else 'toistaiseksi'}")

    try:
        while True:
            now = time.monotonic()
            if end_time and now >= end_time:
                break

            # Varmistetaan lepotilan esto säännöllisesti (varmuuden vuoksi)
            estä_lepotila()

            next_event = min(next_print, next_toggle)
            if end_time:
                next_event = min(next_event, end_time)

            time.sleep(max(0.1, next_event - now))
            now = time.monotonic()

            if now >= next_print:
                elapsed = now - start_mono
                print(f"Aloitus: {start_dt.strftime('%H:%M:%S')} | Kulunut: {fmt_elapsed(elapsed)} | Nyt: {datetime.now().strftime('%H:%M:%S')}")
                next_print += 5 * 60

            if now >= next_toggle:
                scrolllock_on_for_one_second()
                next_toggle = now + random.uniform(3 * 60, 5 * 60)

    except KeyboardInterrupt:
        print("\nKeskeytetty Ctrl+C:lla")
    finally:
        # TÄRKEÄÄ: Palautetaan koneen normaali tila
        salli_lepotila()
        elapsed = time.monotonic() - start_mono
        print(f"Lopetettu. Kokonaisaika: {fmt_elapsed(elapsed)}")

if __name__ == "__main__":
    main()