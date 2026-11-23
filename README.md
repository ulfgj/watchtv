# watchtv

Temporarily stream a specific movie or folder to your Smart TV via MiniDLNA with full subtitle support.

## Usage

```bash
# Stream a folder or movie directly
./watchtv.py -m /path/to/movies

# Stream and convert MP4 + SRT to MKV with native SRT subtitles (Smart TV compatible)
./watchtv.py -m /path/to/movies/my-movie.mp4 --to-mkv

# Stream and soft-mux SRT into MP4/MKV in-place (no duplicate file on disk)
./watchtv.py -m /path/to/movies/my-movie.mp4 --soft-mux
```

## Features
- **File or folder input (`-m`)**: Pass either a folder or a single movie file. When pointing to a single movie (`-m /path/to/movie.mp4`), MiniDLNA automatically serves its **parent directory** so the TV can browse and play it.
- **In-place soft-mux (`--soft-mux`)**: Embeds `.srt` subtitles directly into the video container without duplicating files on disk.
- **MKV conversion (`--to-mkv`)**: Packages video + `.srt` into a `[SUB] <name>.mkv` file with native SRT subtitles for TVs that lack MP4 `mov_text` support.
- **Automatic cleanup**: Runs MiniDLNA in an isolated temporary directory that cleans up its cache and logs on exit (`Ctrl+C`).

## TODOs
* [x] add support for soft-mux as an option to creating a .mkv container.
    - doesn't duplicate the file on disk

