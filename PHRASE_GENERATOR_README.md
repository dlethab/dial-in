# Phrase Generator for Dialin Game

This tool generates 10-character phrases (including spaces) for the Dialin word guessing game. The phrases are designed to be fluent English expressions that make sense when read.

## Features

- **10-character limit**: All phrases fit exactly in a 10-character slot
- **No punctuation**: Phrases contain only letters and spaces
- **Fluent English**: Phrases are natural, meaningful expressions
- **Duplicate prevention**: Avoids generating phrases already in `words.txt`
- **Multiple formats**: Generates both single words and multi-word phrases
- **Future date support**: Can add phrases with future dates for scheduling

## Files

- `phrase_generator.py` - Core phrase generation logic
- `generate_phrases.py` - Command-line interface
- `auto_phrase_scheduler.py` - Automated scheduler that monitors word supply
- `setup_auto_scheduler.py` - Setup script for automatic scheduling
- `words.txt` - Existing phrases database

## Usage

### Basic Usage

Generate 10 phrases (default):
```bash
python3 generate_phrases.py
```

Generate a specific number of phrases:
```bash
python3 generate_phrases.py -n 20
```

### Preview Mode

Preview phrases without adding to file:
```bash
python3 generate_phrases.py --preview
```

### Add to File

Add generated phrases to `words.txt` with current date:
```bash
python3 generate_phrases.py --add-to-file
```

Add phrases with future dates (starting from tomorrow):
```bash
python3 generate_phrases.py --future-dates --add-to-file
```

Add phrases with custom start date:
```bash
python3 generate_phrases.py --start-date 2025-08-01 --add-to-file
```

### Validation

Validate a specific phrase:
```bash
python3 generate_phrases.py --validate "good vibes"
```

### Help

Show all available options:
```bash
python3 generate_phrases.py --help
```

## Phrase Types

The generator creates several types of phrases:

### Multi-word Phrases (80% of output)
- **Adjective + Noun**: "good vibes", "hot pocket", "deep space"
- **Common expressions**: "good times", "safe space", "easy going"
- **Idiomatic phrases**: "wild child", "dark horse", "thick skin"

### Single Words (20% of output)
- **10-letter words**: "management", "technology", "leadership"
- **Compound words**: "playground", "basketball", "friendship"

## Examples

### Generated Phrases
```
'good vibes' (10 chars)
'hot pocket' (10 chars)
'deep space' (10 chars)
'management' (10 chars)
'technology' (10 chars)
'easy going' (10 chars)
'safe space' (10 chars)
'wild child' (10 chars)
'light bulb' (10 chars)
'fast track' (10 chars)
```

### Validation Examples
```bash
$ python3 generate_phrases.py --validate "good vibes"
Phrase: 'good vibes'
Length: 10 characters
Valid: Yes
Already exists: Yes

$ python3 generate_phrases.py --validate "hello world"
Phrase: 'hello world'
Length: 11 characters
Valid: No
```

## Integration with Flask App

The phrase generator is designed to work with the existing Flask app (`app.py`). The generated phrases in `words.txt` will automatically be used by the game.

## Requirements

- Python 3.6+
- `schedule` library (for auto-scheduler): `pip3 install schedule`

## Auto-Scheduler

The auto-scheduler automatically monitors your word supply and generates new phrases when you're running low.

### Quick Setup

```bash
# Run the setup script (macOS/Linux)
python3 setup_auto_scheduler.py
```

### Manual Setup

```bash
# Check current phrase supply
python3 auto_phrase_scheduler.py --check-now

# Start scheduler manually (runs continuously)
python3 auto_phrase_scheduler.py

# Custom settings
python3 auto_phrase_scheduler.py --min-days 14 --generate 50 --interval 12
```

### Configuration Options

- `--min-days 7` - Generate phrases when less than 7 days ahead (default)
- `--generate 30` - Generate 30 phrases at a time (default)
- `--interval 24` - Check every 24 hours (default)

## Tips

1. **Use preview mode first** to see what phrases will be generated before adding them to the file
2. **Generate in batches** of 20-30 phrases for better variety
3. **Use future dates** to schedule phrases ahead of time
4. **Validate custom phrases** before manually adding them to ensure they meet the requirements
5. **Set up auto-scheduler** to never run out of phrases automatically

## Customization

You can modify `phrase_generator.py` to:
- Add more word lists
- Change phrase templates
- Adjust the ratio of single words vs multi-word phrases
- Add new phrase patterns

The generator automatically learns from existing phrases in `words.txt` to avoid duplicates. 