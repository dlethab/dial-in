# Daily Phrase Generator Agent

An agent that generates exactly 10-character phrases (including spaces) for daily word games. The phrases are common English words and phrases without punctuation.

## Features

- Generates exactly 10-character phrases including spaces
- No punctuation allowed (only letters, numbers, and spaces)
- Avoids duplicates by tracking previously used phrases
- Continues date sequence from the last entry in `words.txt`
- Generates fluent English phrases and common words
- Includes single words, two-word phrases, and three-word phrases

## Usage

### Basic Usage
Generate 30 phrases (default):
```bash
python3 phrase_generator.py
```

### Custom Number of Phrases
Generate a specific number of phrases:
```bash
python3 generate_phrases.py [number]
```

Examples:
```bash
python3 generate_phrases.py 50    # Generate 50 phrases
python3 generate_phrases.py 10    # Generate 10 phrases
```

## Output Format

Phrases are automatically appended to `words.txt` in the format:
```
YYYY-MM-DD, phrase here
```

Example:
```
2025-08-01, voice mail
2025-08-02, book store
2025-08-03, pool party
```

## Requirements

- Python 3.x
- No external dependencies (uses only standard library)

## How It Works

1. **Reads existing phrases** from `words.txt` to avoid duplicates
2. **Finds the last date** in the file to continue the sequence
3. **Validates phrases** to ensure they're exactly 10 characters and contain no punctuation
4. **Shuffles available phrases** for randomness
5. **Generates the requested number** of new phrases with consecutive dates
6. **Appends to file** in the correct format

## Phrase Categories

The generator includes three types of phrases:

### Single 10-letter Words
Examples: `adventures`, `basketball`, `friendship`, `playground`

### Two-word Phrases (with space = 10 chars)
Examples: `good vibes`, `jazz hands`, `deep space`, `cool beans`

### Three-word Phrases (with spaces = 10 chars)
Examples: `i love you`, `go to bed`, `you rock`

## Notes

- The agent will warn you if there aren't enough unique phrases available
- All phrases are common, fluent English
- The date format is YYYY-MM-DD
- Phrases are randomly selected from the available pool
- The generator automatically handles date continuation from the existing file

