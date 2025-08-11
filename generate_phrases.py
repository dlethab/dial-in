#!/usr/bin/env python3
"""
Phrase Generator CLI
A simple command-line interface for generating 10-character phrases for the dialin game.
"""

import argparse
import sys
from datetime import datetime, timedelta
from phrase_generator import PhraseGenerator

def main():
    parser = argparse.ArgumentParser(
        description="Generate 10-character phrases for the dialin game",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_phrases.py                    # Generate 10 phrases
  python generate_phrases.py -n 20             # Generate 20 phrases
  python generate_phrases.py --add-to-file     # Add generated phrases to words.txt
  python generate_phrases.py --validate "hello world"  # Validate a phrase
  python generate_phrases.py --future-dates    # Generate phrases with future dates
        """
    )
    
    parser.add_argument(
        '-n', '--count',
        type=int,
        default=10,
        help='Number of phrases to generate (default: 10)'
    )
    
    parser.add_argument(
        '--add-to-file',
        action='store_true',
        help='Add generated phrases to words.txt with dates'
    )
    
    parser.add_argument(
        '--validate',
        type=str,
        help='Validate a specific phrase'
    )
    
    parser.add_argument(
        '--future-dates',
        action='store_true',
        help='Generate phrases with future dates (starting from tomorrow)'
    )
    
    parser.add_argument(
        '--start-date',
        type=str,
        help='Start date for future phrases (YYYY-MM-DD format)'
    )
    
    parser.add_argument(
        '--preview',
        action='store_true',
        help='Preview phrases without adding to file'
    )
    
    args = parser.parse_args()
    
    generator = PhraseGenerator()
    
    # Validate a specific phrase
    if args.validate:
        phrase = args.validate
        is_valid = generator.validate_phrase(phrase)
        print(f"Phrase: '{phrase}'")
        print(f"Length: {len(phrase)} characters")
        print(f"Valid: {'Yes' if is_valid else 'No'}")
        if is_valid:
            print(f"Already exists: {'Yes' if phrase.lower() in generator.existing_phrases else 'No'}")
        return
    
    # Generate phrases
    print(f"Generating {args.count} phrases...")
    phrases = generator.generate_phrases(args.count)
    
    if not phrases:
        print("No phrases could be generated. Try increasing the count or check existing phrases.")
        return
    
    # Display generated phrases
    print(f"\nGenerated {len(phrases)} phrases:")
    print("-" * 50)
    
    for i, phrase in enumerate(phrases, 1):
        print(f"{i:2d}. '{phrase}' ({len(phrase)} chars)")
    
    # Add to file if requested
    if args.add_to_file:
        print(f"\nAdding phrases to words.txt...")
        
        if args.future_dates or args.start_date:
            # Generate future dates
            if args.start_date:
                try:
                    start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
                except ValueError:
                    print("Error: Invalid start date format. Use YYYY-MM-DD")
                    return
            else:
                start_date = datetime.now() + timedelta(days=1)
            
            added_count = 0
            for i, phrase in enumerate(phrases):
                date = start_date + timedelta(days=i)
                date_str = date.strftime('%Y-%m-%d')
                
                if generator.add_phrase_to_file(phrase, date_str):
                    print(f"Added: {date_str}, {phrase}")
                    added_count += 1
                else:
                    print(f"Failed to add: {phrase}")
            
            print(f"\nSuccessfully added {added_count} phrases to words.txt")
        else:
            # Add with current date
            added_count = 0
            for phrase in phrases:
                if generator.add_phrase_to_file(phrase):
                    print(f"Added: {phrase}")
                    added_count += 1
                else:
                    print(f"Failed to add: {phrase}")
            
            print(f"\nSuccessfully added {added_count} phrases to words.txt")
    
    elif args.preview:
        print(f"\nPreview mode - phrases not added to file")
        print("Use --add-to-file to save them")
    
    else:
        print(f"\nPhrases generated successfully!")
        print("Use --add-to-file to save them to words.txt")
        print("Use --future-dates to add them with future dates")

if __name__ == "__main__":
    main() 