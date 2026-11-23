# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.7.0] - 2026-11-23

### Added
- `--soft-mux` flag to embed `.srt` subtitles directly into the video container in-place without duplicating disk space.
- Changed MKV prefix to `+SUB_` so subtitle-enabled files sort at the very top of TV media browsers (before numbers and letters).
- Mutually exclusive safeguard preventing `--to-mkv` and `--soft-mux` from running simultaneously.
- `--version` / `-v` CLI flag.

## [0.6.0] - 2026-11-23

### Added
- `--to-mkv` flag to package MP4 + `.srt` into an MKV container with native SubRip (SRT) subtitles for Smart TVs lacking MP4 `mov_text` support.
- `[SUB]` prefix added to generated MKV files for quick identification without waiting for TV list text to scroll.
- Single-file media support: passing `-m /path/to/movie.mp4` processes that movie and streams its parent folder.
- Project `README.md` and initial git repository setup.

## [0.5.0] - 2026-11-23

### Fixed
- Fixed subtitles not advertising to Philips Saphi TV: switched from `strict_dlna=yes` to `strict_dlna=no` so MiniDLNA advertises vendor subtitle tags (`sec:CaptionInfo`, `smi`, and UPnP `<res>` subtitle headers).
- Cleaned up invalid DLNA configuration directives and added `notify_interval=60`.

## [0.1.0] - [0.4.0] - Pre-Release Prototypes

### Added
- Initial standalone streaming script using `minidlnad`.
- Ephemeral configuration and database isolation using Python `tempfile`.
- Automatic network interface binding (`en0` default for macOS).
- Foreground debug mode with automatic process termination and cleanup on `Ctrl+C`.
