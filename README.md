# watchtv

![Version](https://img.shields.io/badge/version-0.9.0-blue.svg?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg?style=flat-square)

Temporarily stream a specific movie or folder to your Smart TV via MiniDLNA or Google Chromecast with full subtitle support.

## Prerequisites

Install the required tools via [Homebrew](https://brew.sh) and [pip](https://pip.pypa.io):

```bash
# Required for DLNA streaming & video packaging
brew install minidlna ffmpeg

# Required for Chromecast casting
pip3 install catt
```

- **`minidlna`**: Lightweight DLNA/UPnP-AV server that streams media to your TV.
- **`ffmpeg`**: Required for `--to-mkv` stream-packaging with native subtitle tracks.
- **`catt`**: Casts local videos and subtitles directly to Google Chromecast devices.

## Usage

```bash
# 1. DLNA: Stream a folder or movie directly to your Smart TV
./watchtv.py -m /path/to/movies

# 2. DLNA: Stream and package MP4 + SRT into MKV with ASS subtitles (Philips Saphi compatible)
./watchtv.py -m /path/to/movies/my-movie.mp4 --to-mkv

# 3. Chromecast: Cast a movie and subtitles directly to your Google Chromecast
./watchtv.py -m /path/to/movies/my-movie.mp4 --cast

# 4. Chromecast: Target a specific Chromecast device by name or IP
./watchtv.py -m /path/to/movies/my-movie.mp4 --cast -d "my_chromecast"
```

## Features
- **Chromecast Streaming (`--cast`)**: Cast directly to any Google Chromecast on your local Wi-Fi with automatic `.srt` to WebVTT subtitle conversion.
- **File or folder input (`-m`)**: Pass either a folder or a single movie file. When pointing to a single movie (`-m /path/to/movie.mp4`), MiniDLNA automatically serves its **parent directory** so the TV can browse and play it.
- **MKV conversion (`--to-mkv`)**: Packages video + `.srt` into a `+SUB_<name>.mkv` file with ASS (Advanced SubStation Alpha) subtitles. This automatically translates HTML styling (`<i>`, `<b>`) into clean subtitles without raw tags on Smart TVs (and top-sorts with `+`).
- **Automatic cleanup**: Runs MiniDLNA or Cast sessions ephemerally, cleaning up all caches and stopping streaming on exit (`Ctrl+C`).

## Version History

| Version | Status | Highlights |
| :--- | :---: | :--- |
| **`v0.9.0`** | 🚀 *Latest* | Added Google Chromecast streaming via `--cast` and `--cast-device` flags. |
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
