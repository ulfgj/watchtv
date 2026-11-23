# watchtv

![Version](https://img.shields.io/badge/version-0.7.0-blue.svg?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg?style=flat-square)

Temporarily stream a specific movie or folder to your Smart TV via MiniDLNA with full subtitle support.

## Prerequisites

Install the required tools via [Homebrew](https://brew.sh):

```bash
brew install minidlna ffmpeg
```

- **`minidlna`**: Lightweight DLNA/UPnP-AV server that streams media to your TV.
- **`ffmpeg`**: Required for `--to-mkv` stream-packaging with native subtitle tracks.

## Usage

```bash
# Stream a folder or movie directly
./watchtv.py -m /path/to/movies

# Stream and convert MP4 + SRT to MKV with native SRT subtitles (Smart TV compatible)
./watchtv.py -m /path/to/movies/my-movie.mp4 --to-mkv
```

## Features
- **File or folder input (`-m`)**: Pass either a folder or a single movie file. When pointing to a single movie (`-m /path/to/movie.mp4`), MiniDLNA automatically serves its **parent directory** so the TV can browse and play it.
- **MKV conversion (`--to-mkv`)**: Packages video + `.srt` into a `+SUB_<name>.mkv` file with native SRT subtitles for TVs that lack MP4 `mov_text` support (the `+` prefix ensures it sorts at the top of the TV file list).
- **Automatic cleanup**: Runs MiniDLNA in an isolated temporary directory that cleans up its cache and logs on exit (`Ctrl+C`).

## Version History

| Version | Status | Highlights |
| :--- | :---: | :--- |
| **`v0.7.0`** | 🚀 *Latest* | Streamlined `--to-mkv` packaging, added `+SUB_` top-sorting prefix, & `--version` flag. |
| **`v0.6.0`** | ✅ | Added `--to-mkv` container packaging and single-file input. |
| **`v0.5.0`** | ✅ | Solved Smart TV subtitle discovery with `strict_dlna=no` & custom DLNA headers. |
| **`v0.1.0` – `v0.4.0`** | 🛠️ | Early CLI prototypes, ephemeral MiniDLNA temp configs, and network binding. |

*(For full details, see [CHANGELOG.md](CHANGELOG.md))*

## TODOs
- [ ] 



