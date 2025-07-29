#!/usr/bin/env python3
"""
CLI script to generate daily phrases
Usage: python generate_phrases.py [number_of_phrases]
"""

import sys
from phrase_generator import PhraseGenerator

def main():
    # Default to 30 phrases if no argument provided
    count = 30
    
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
            if count <= 0:
                print("Number of phrases must be positive!")
                sys.exit(1)
        except ValueError:
            print("Please provide a valid number!")
            sys.exit(1)
    
    # Create generator and run
    generator = PhraseGenerator()
    generator.generate_and_save(count)

if __name__ == "__main__":
    main()