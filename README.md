# Chunkup

Given an audio file, and a tab delimited file, split up audio file into smaller chunks.

# Requirements & Caveats

- Imports pysox, therefore has the same dependencies as pysox, namely:

> [Required prerequisite are the development libraries of sox at version 14.3.x, i.e. the header files and libraries to link against. Specifically you need sox.h in your include path and libsox.so and libsox.a in your link path. Pysox will not compile against any sox version prior to 14.3.0.](https://pypi.python.org/pypi/pysox/0.3.6.alpha)

- chunkup will *only* chunk up audio. Any other effects (resampling etc) should be applied to the audio file before running chunkup.
- At the moment, chunkup will operate fairly blindly. If you give it start and end times for a chunk that actually lie outside of the provided audio file, it'll return a bunch of sox errors that look like:

```
    trim: End position is after expected end of audio.
    trim: Last 1 position(s) not reached.
```

# Usage

This usage example pulls down [Episode #20: I Want to Break Free](http://gimletmedia.com/episode/20-i-want-to-break-free/) of Reply All. The mp3 is 41.5M.

    curl -L -o examples/reply_all_podcast.mp3 http://bit.ly/chunkup 
    mkdir chunks

    python chunkup.py examples/reply_all_podcast.mp3 examples/replyallcreak.txt chunks/

## Chunk naming

`chunks/` now contains 104 chunks of speech I annotated, largely to separate out the three speakers in the first segment. The default naming conventions of chunks are:

    [n]-[basename]-[col1]-[col3].wav

Where `[n]` is the numeric index of the chunk, `[basename]` is the base name of the original soundfile, `[col1]` is the value from column 1 in `replyallcreak.txt` (in this case, speaker ID), and `[col3]` is the value from column 3 in `replyallcreak.txt` (in this case, the onset time of the chunk in ss.ms). Available variables for naming chunks are:

| naming variable | description |
| ------- | ------- |
| `[n]` | chunk number |
| `[basename]` | base name of original audio file |
| `[col0-9]` | value from any the given column in the chunk file|

## Configuration

You can change the chunk naming convention either at the command line usig the `-n` or `--naming` flag.

    python chunkup.py -n [col1]-[n].wav examples/reply_all_podcast.mp3 examples/replyallcreak.txt chunks/

Other config options include

| option | description |
| -------- | ----------- |
| `-s`, `--start`| Column index (starting with 1) for the start time, in ss.ms format |
| `-e`, `--end` | Column index (starting with 1) for the end time, in ss.ms format |
| `--header` | Include if chunk file has a header |

All config options can be defined in a config file and passed to chunkup.py with the prefix `+`. A sample config file for this data would be:

    --naming
    [n]-[basename]-[col1]-[col3].wav
    --start
    3
    --end
    4

If saved to config.txt, it could be passed to chunkup.py like so:

    python chunkup.py +config.txt examples/reply_all_podcast.mp3 examples/replyallcreak.txt chunks/

## Compiling

If you'd like to use chunkup as a standalone commandline tool, you can compile it using `pyinstaller`. 

    # install pyinstaller if you haven't already
    pip install pyinstaller
    pyinstaller chunkup.py

The compiled program is now in `./dist/chunkup/`. If you add that directory to your path, you'll be able to use it like so:

    chunkup examples/reply_all_podcast.mp3 examples/replyallcreak.txt chunks/