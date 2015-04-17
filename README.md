# Chunkup

Given an audio file, and a tab delimited file, split up audio file into smaller chunks.

# Requirements & Caveats

- Imports pysox, therefore has the same dependencies as pysox, namely:

> [Required prerequisite are the development libraries of sox at version 14.3.x, i.e. the header files and libraries to link against. Specifically you need sox.h in your include path and libsox.so and libsox.a in your link path. Pysox will not compile against any sox version prior to 14.3.0.](https://pypi.python.org/pypi/pysox/0.3.6.alpha)

- chunkup will *only* chunk up audio. Any other effects (resampling etc) should be applied to the audio file before running chunkup.
- At the moment, chunkup will operate fairly blindly. If you give it start and end times for a chunk that actually lie outside of the provided audio file, it'll return a bunch of sox errors that look like:

    trim: End position is after expected end of audio.
    trim: Last 1 position(s) not reached.

