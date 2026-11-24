# watchtv

![Version](https://img.shields.io/badge/version-0.10.0-blue.svg?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg?style=flat-square)

Lightweight macOS CLI tools to stream local movies to your TV with reliable subtitles:
- **`watchtv.py`**: Ephemeral MiniDLNA server + lossless MKV/ASS subtitle packaging for Smart TVs (e.g., Philips Saphi).
- **`casttv.py`**: Direct Google Chromecast streamer with automatic `.srt`/`.vtt` subtitles and clean `Ctrl+C` teardown.

## Prerequisites

Install the tools you need via [Homebrew](https://brew.sh) and [pip](https://pip.pypa.io):

```bash
# Required for watchtv.py (DLNA streaming & MKV/ASS packaging)
brew install minidlna ffmpeg

# Required for casttv.py (Google Chromecast casting)
pip3 install catt
```

- **`minidlna`**: Lightweight DLNA/UPnP-AV server used by `watchtv.py`.
- **`ffmpeg`**: Required for `watchtv.py --to-mkv` stream-packaging with ASS subtitle tracks.
- **`catt`**: Used by `casttv.py` to cast local videos and subtitles directly to Chromecast devices.

## Usage

### DLNA Smart TVs (`watchtv.py`)

```bash
# 1. Stream a folder or movie directly to your Smart TV
./watchtv.py -m /path/to/movies

# 2. Package MP4 + SRT into +SUB_<name>.mkv with ASS subtitles (Philips Saphi compatible)
./watchtv.py -m /path/to/movies/my-movie.mp4 --to-mkv
```

### Google Chromecast (`casttv.py`)

```bash
# 1. Scan for Chromecast devices on your Wi-Fi
./casttv.py --scan

# 2. Cast a movie (auto-detects Chromecast and matching .srt/.vtt subtitles)
./casttv.py -m /path/to/movies/my-movie.mp4

# 3. Target a specific Chromecast device by name or IP
./casttv.py -m /path/to/movies/my-movie.mp4 -d "my_chromecast"
```

## Features
- **Clean separation (`watchtv.py` vs `casttv.py`)**: `watchtv.py` stays zero-pip-dependency for DLNA TVs, while `casttv.py` handles Google Cast push streaming independently.
- **File or folder input (`-m`)**: Pass either a folder or a single movie file. When pointing to a single movie (`-m /path/to/movie.mp4`), `watchtv.py` serves its **parent directory** so the DLNA TV can browse and play it.
- **MKV conversion (`--to-mkv`)**: Packages video + `.srt` into a `+SUB_<name>.mkv` file with ASS (Advanced SubStation Alpha) subtitles. This automatically translates HTML styling (`<i>`, `<b>`) into clean subtitles without raw tags on Smart TVs (and top-sorts with `+`).
- **Automatic cleanup**: Runs MiniDLNA or Chromecast sessions ephemerally, wiping temporary caches and sending an explicit stop signal on exit (`Ctrl+C`).

## Version History

| Version | Status | Highlights |
| :--- | :---: | :--- |
| **`v0.10.0`** | 🚀 *Latest* | Decoupled Chromecast into standalone `casttv.py`; kept `watchtv.py` pure DLNA. |
| **`v0.9.0`** | ✅ | Added Google Chromecast streaming (`--cast` / `--cast-device`). |
| **`v0.8.0`** | ✅ | Automatic ASS subtitle encoding in MKV to eliminate raw HTML tags (`<i>`, `<b>`). |
| **`v0.7.0`** | ✅ | Added `+SUB_` top-sorting prefix, single-file streaming, & `--version` flag. |
| **`v0.6.0`** | ✅ | Added `--to-mkv` container packaging and single-file input. |
| **`v0.5.0`** | ✅ | Solved Smart TV subtitle discovery with `strict_dlna=no` & custom DLNA headers. |
| **`v0.1.0` – `v0.4.0`** | 🛠️ | Early CLI prototypes, ephemeral MiniDLNA temp configs, and network binding. |

*(For full details, see [CHANGELOG.md](CHANGELOG.md))*

## TODOs
- [x] research .ass files to see if markup in the .srt can be visually correct
    + i.e. parse `<i>` correctly as italic text, and tags
    + "yes, proceed with the ASS experiment" was the last prompt my wife saw on my screen before she took the kids and left...
    + also the output is `test/ass_experiment/+SUB_styled_ass.mkv`. ur not helping...
    + "_Your main branch is now on v0.8.0 with full ASS packaging and clean subtitle rendering!_" - oh come on!
