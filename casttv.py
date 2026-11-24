#!/usr/bin/env python3
import argparse
import re
import subprocess
import sys
import time
from pathlib import Path

__version__ = "0.1.0"

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".m4v", ".webm", ".avi"}
SUBTITLE_EXTENSIONS = (".srt", ".vtt")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Cast local video files and subtitles directly to a Google Chromecast."
    )
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--media",
        "-m",
        type=str,
        default=None,
        help="Path to a movie file or a folder containing movies.",
    )
    parser.add_argument(
        "--device",
        "--cast-device",
        "-d",
        dest="device",
        type=str,
        default=None,
        help="Target Chromecast device name or IP (default: auto-detect).",
    )
    parser.add_argument(
        "--subtitles",
        "-s",
        type=str,
        default=None,
        help="Optional subtitle file (.srt or .vtt). Auto-detects matching file if omitted.",
    )
    parser.add_argument(
        "--scan",
        action="store_true",
        help="Discover available Chromecast devices on the local network and exit.",
    )
    return parser.parse_args()


def ensure_catt_installed() -> None:
    """Exit with installation instructions if 'catt' is unavailable."""
    try:
        import catt  # noqa: F401
    except ImportError:
        print("Error: 'catt' is not installed. Install it with: pip3 install catt", file=sys.stderr)
        sys.exit(1)


def _run_dns_sd(args: list[str], wait_seconds: float) -> str:
    """Run macOS dns-sd briefly and return captured stdout."""
    proc = subprocess.Popen(
        ["dns-sd", *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    time.sleep(wait_seconds)
    proc.terminate()
    out, _ = proc.communicate()
    return out


def discover_cast_devices() -> list[dict[str, str]]:
    """Discover Chromecast devices on the local network via mDNS (dns-sd)."""
    devices: list[dict[str, str]] = []
    seen_instances: set[str] = set()

    try:
        browse_out = _run_dns_sd(["-B", "_googlecast._tcp", "."], wait_seconds=1.2)
        for line in browse_out.splitlines():
            if "_googlecast._tcp." not in line:
                continue
            instance = line.split("_googlecast._tcp.")[-1].strip()
            if not instance or instance in seen_instances:
                continue
            seen_instances.add(instance)

            lookup_out = _run_dns_sd(
                ["-L", instance, "_googlecast._tcp", "local."],
                wait_seconds=0.8,
            )
            friendly_name = instance
            model = "Chromecast"
            host_port = ""

            for l_line in lookup_out.splitlines():
                if "can be reached at " in l_line:
                    host_port = l_line.split("can be reached at ")[-1].split(" ")[0].strip()
                fn_match = re.search(r"\bfn=((?:\\.|[^ ])+)", l_line)
                if fn_match:
                    friendly_name = fn_match.group(1).replace(r"\ ", " ")
                md_match = re.search(r"\bmd=((?:\\.|[^ ])+)", l_line)
                if md_match:
                    model = md_match.group(1).replace(r"\ ", " ")

            devices.append(
                {
                    "name": friendly_name,
                    "model": model,
                    "host": host_port,
                    "instance": instance,
                }
            )
    except FileNotFoundError:
        # dns-sd is macOS-specific; fall back cleanly if unavailable
        return []
    except Exception:
        return devices

    return devices


def resolve_video_path(raw_media: str) -> Path:
    """Resolve input path to a single playable video file."""
    input_path = Path(raw_media).expanduser().resolve()
    if not input_path.exists():
        print(f"Error: '{input_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    if input_path.is_file():
        return input_path

    video_files = sorted(
        f for f in input_path.rglob("*") if f.is_file() and f.suffix.lower() in VIDEO_EXTENSIONS
    )
    if not video_files:
        print(f"Error: No video files found in '{input_path}'.", file=sys.stderr)
        sys.exit(1)

    selected = video_files[0]
    if len(video_files) > 1:
        print(f"Multiple files in folder. Selecting: {selected.name}")
    return selected


def resolve_subtitle_path(video_path: Path, explicit_sub: str | None) -> Path | None:
    """Resolve explicit subtitle file or auto-detect matching .srt/.vtt sidecar."""
    if explicit_sub:
        sub_path = Path(explicit_sub).expanduser().resolve()
        if not sub_path.exists() or not sub_path.is_file():
            print(f"Error: Subtitle file '{sub_path}' does not exist.", file=sys.stderr)
            sys.exit(1)
        return sub_path

    for ext in SUBTITLE_EXTENSIONS:
        candidate = video_path.with_suffix(ext)
        if candidate.exists():
            return candidate
    return None


def send_chromecast_stop(python_bin: str, target_device: str | None) -> None:
    """Send an explicit stop signal so the Chromecast receiver exits cleanly instead of buffering."""
    stop_cmd = [python_bin, "-m", "catt.cli"]
    if target_device:
        stop_cmd.extend(["-d", target_device])
    stop_cmd.append("stop")
    try:
        subprocess.run(stop_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
    except Exception:
        pass


def cast_media(video_path: Path, sub_file: Path | None, device: str | None = None) -> None:
    """Cast a video file and optional subtitles to a Google Chromecast using catt."""
    python_bin = sys.executable

    target_device = device
    if not target_device:
        discovered = discover_cast_devices()
        if discovered:
            target_device = discovered[0]["name"]

    cmd = [python_bin, "-m", "catt.cli"]
    if target_device:
        cmd.extend(["-d", target_device])

    cmd.append("cast")
    if sub_file:
        print(f"💬 Subtitle track: {sub_file.name}")
        cmd.extend(["-s", str(sub_file)])

    cmd.append(str(video_path))

    target_desc = f"device '{target_device}'" if target_device else "Chromecast"
    print(f"🎬 Casting '{video_path.name}' to {target_desc}...")
    print("📺 Playback started! Press Ctrl+C to stop casting.\n")

    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n🛑 Interrupt received! Stopping Chromecast receiver...")
    finally:
        send_chromecast_stop(python_bin, target_device)
        print("✅ Chromecast session stopped.")


def main() -> None:
    args = parse_args()

    if args.scan:
        print("🔍 Scanning local network for Chromecast devices...")
        devices = discover_cast_devices()
        if not devices:
            print("No Chromecast devices found via mDNS.")
            sys.exit(1)
        for idx, dev in enumerate(devices, start=1):
            host_info = f" ({dev['host']})" if dev["host"] else ""
            print(f"[{idx}] {dev['name']} - {dev['model']}{host_info}")
        return

    if not args.media:
        print("Error: --media / -m is required unless --scan is used.", file=sys.stderr)
        sys.exit(1)

    ensure_catt_installed()
    target_video = resolve_video_path(args.media)
    sub_file = resolve_subtitle_path(target_video, args.subtitles)
    cast_media(target_video, sub_file, device=args.device)


if __name__ == "__main__":
    main()
