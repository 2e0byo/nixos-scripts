from json import loads
from pathlib import Path
from random import choices
from subprocess import run
from time import sleep

from filelock import FileLock

cmdbase = ["hyprctl", "hyprpaper"]
lock = FileLock("/tmp/hyprpaper.lock")


def load_backgrounds(mapping: dict[str, Path]):
    with lock:
        mapping: dict[str, str] = {k: str(v) for k, v in mapping.items()}
        for bg in mapping.values():
            run(cmdbase + ["preload", bg])
        for monitor, bg in mapping.items():
            run(cmdbase + ["wallpaper", f"{monitor},{bg}"])
        run(cmdbase + ["unload", "all"])
        sleep(0.5)


if __name__ == "__main__":
    imgs = Path("~/backgrounds").expanduser().resolve()
    monitors = set(
        x["name"]
        for x in loads(
            run(["hyprctl", "-j", "monitors"], capture_output=True).stdout
            )
    )
    extns = {".jpg", ".jpeg", ".png"}
    available = [x for x in imgs.glob("*") if x.suffix.lower() in extns]
    backgrounds = dict(zip(monitors, choices(available, k=len(monitors))))
    load_backgrounds(backgrounds)
