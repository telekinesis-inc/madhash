# MadHash

Funny, Human-Memorable, SHA-256 Fingerprints

## Idea

A human readable representation of SHA-256 fingerprints using the following structure:

`<Adjective>` `<Noun>` `<Adverb>` `<Verb>` `<Adjective>` `<Noun>`

Words are sourced from a fixed dictionary, generated from the Brown corpus, then filtered for profanity. You can check out the process in `dictionary_generator.py`

There are 2<sup>10</sup> adjectives, 2<sup>12</sup> nouns, 2<sup>9</sup> adverbs adverbs 2<sup>11</sup> verbs, totalling a space of 2<sup>64</sup> sentences. With 4 sentences we cover the whole 256 bits of SHA-256.

You can try it out [here](https://madhash.telekinesis.cloud)
