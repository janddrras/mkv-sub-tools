# MKV Subtitle Tools

A powerful CLI utility for managing and cleaning subtitle tracks within MKV containers. This tool streamlines common tasks like extraction, addition, and formatting cleanup.

## Capabilities

- **Automated Embedded Cleaning**: Scan an MKV file, extract all subtitle tracks, strip them of formatting tags (HTML/SSA), and merge them back—all in one step.
- **Track Extraction**: Selectively extract any subtitle track to a standard `.srt` file.
- **Track Removal**: Easily remove unwanted subtitle tracks from an MKV file.
- **External Addition**: Merge external SRT or ASS files into existing MKVs with optional language tagging.
- **Standalone Subtitle Cleaning**: Process independent subtitle files to remove annoying tags like `<i>`, `<b>`, or complex SSA alignment/style overrides.
- **Non-Destructive**: All modifications create a new file with `-mod` suffix, preserving your original media.

## Prerequisites

- [Python 3.13+](https://www.python.org/downloads/)
- [uv](https://github.com/astral-sh/uv) package manager
- [MKVToolNix](https://mkvtoolnix.download/) installed and available in your PATH (`mkvmerge`, `mkvextract`, `mkvinfo`).

## Installation

1. Clone the repository.
2. The project uses `uv` for dependency management. Install dependencies with:

   ```bash
   uv sync
   ```

## Usage

Run the interactive CLI:

```bash
uv run main.py
```

### Menu Options

1. **Extract subtitle from MKV**: Choose a track to export as a standalone file.
2. **Add subtitle to MKV**: Merge an external subtitle file into an MKV.
3. **Remove subtitle from MKV**: Select a track to permanently remove.
4. **Clean up external subtitle file**: Strip tags from a standalone `.srt` or `.ass` file.
5. **Clean ALL embedded subtitles in MKV (Automated)**: Processes every subtitle track inside the MKV to remove formatting and creates a new cleaned version of the MKV.

## How it Works

- **Extraction**: Uses `mkvextract`.
- **Merging**: Uses `mkvmerge`.
- **Cleaning**: Powered by `pysubs2`, utilizing its plaintext parsing to reliably strip all formatting while preserving timing.

## License

MIT
