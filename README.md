# MKV Subtitle Tools

A simple CLI tool to extract, add, remove, and clean subtitles in MKV files.

## Prerequisites

- [Python 3.13+](https://www.python.org/downloads/)
- [uv](https://github.com/astral-sh/uv) package manager
- [MKVToolNix](https://mkvtoolnix.download/) installed and available in your PATH.

## Installation

1. Clone the repository.
2. Ensure `uv` is installed.
3. The project is already initialized with `uv`. To install dependencies:

   ```bash
   uv sync
   ```

## Usage

Run the script using `uv`:

```bash
uv run main.py
```

### Actions

1. **Extract subtitle from MKV**: Extracts a specific subtitle track to a `.srt` file.
2. **Add subtitle to MKV**: Merges a external subtitle file (SRT/ASS) into an MKV.
3. **Remove subtitle from MKV**: Removes a specific subtitle track from an MKV.
4. **Clean up subtitle**: Strips HTML tags (`<i>`, `<b>`, etc.) and formatting from a subtitle file.

Modified files are saved in the same directory as the original, with `-mod` added to the filename.

## License

MIT
