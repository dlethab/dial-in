data = """
2025-07-15, donut shop
2025-07-16, open world
2025-07-17, pink cloud
2025-07-18, jazz kicks
2025-07-19, calm storm
2025-07-20, nine lives
2025-07-21, rice balls
2025-07-22, fast camel
2025-07-23, brave frog
2025-07-24, spin cycle
2025-07-25, pet sitter
2025-07-26, green room
2025-07-27, late night
2025-07-28, soft smile
2025-07-29, fried fish
2025-07-30, wide awake
2025-07-31, top shelf
"""

# Process the data
for line in data.strip().splitlines():
    date, word = map(str.strip, line.split(','))
    length = len(word)
    print(f"{date}: {word} ({length} letters)", end='')
    if length != 10:
        print("  <-- Not 10 letters!")
    else:
        print()
