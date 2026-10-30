import random
import re
from typing import List, Set
import requests
from datetime import datetime, timedelta

class PhraseGenerator:
    def __init__(self):
        self.existing_phrases = set()
        self.word_lists = {
            'short_words': [],  # 2-4 letter words
            'medium_words': [],  # 5-7 letter words  
            'long_words': [],   # 8+ letter words
            'common_words': []  # frequently used words
        }
        self._load_existing_phrases()
        self._load_word_lists()
    
    def _load_existing_phrases(self):
        """Load existing phrases from words.txt to avoid duplicates"""
        try:
            with open('words.txt', 'r') as file:
                for line in file:
                    if ',' in line:
                        date, phrase = line.strip().split(', ')
                        self.existing_phrases.add(phrase.lower())
        except FileNotFoundError:
            print("words.txt not found, starting with empty phrase set")
    
    def _load_word_lists(self):
        """Load word lists for phrase generation"""
        # Common short words (2-4 letters) for natural phrases
        short_words = [
            'i', 'am', 'at', 'be', 'by', 'do', 'go', 'he', 'if', 'in', 'is', 'it', 'me', 'my', 'no', 'of', 'on', 'or', 'so', 'to', 'up', 'we', 'an', 'as', 'hi', 'ok', 'us', 'ad', 'ah', 'ai', 'am', 'an', 'as', 'at', 'be', 'by', 'do', 'go', 'he', 'hi', 'if', 'in', 'is', 'it', 'me', 'my', 'no', 'of', 'on', 'or', 'so', 'to', 'up', 'us', 'we', 'ah', 'ai', 'am', 'an', 'as', 'at', 'be', 'by', 'do', 'go', 'he', 'hi', 'if', 'in', 'is', 'it', 'me', 'my', 'no', 'of', 'on', 'or', 'so', 'to', 'up', 'us', 'we',
            'all', 'and', 'are', 'bad', 'big', 'but', 'can', 'day', 'did', 'end', 'for', 'get', 'had', 'has', 'her', 'him', 'his', 'how', 'its', 'let', 'man', 'new', 'now', 'old', 'one', 'our', 'out', 'put', 'say', 'see', 'she', 'the', 'too', 'two', 'use', 'was', 'way', 'who', 'you', 'boy', 'cat', 'dog', 'eat', 'fun', 'hot', 'ice', 'joy', 'key', 'law', 'map', 'net', 'oil', 'pen', 'red', 'sun', 'top', 'van', 'win', 'yes', 'zoo',
            'able', 'back', 'been', 'call', 'come', 'down', 'each', 'even', 'find', 'give', 'have', 'here', 'just', 'know', 'like', 'look', 'make', 'more', 'over', 'some', 'take', 'than', 'them', 'they', 'this', 'time', 'very', 'want', 'well', 'went', 'were', 'what', 'when', 'will', 'work', 'year', 'your', 'away', 'blue', 'book', 'cool', 'deep', 'door', 'easy', 'face', 'fast', 'fine', 'free', 'full', 'game', 'good', 'hand', 'hard', 'head', 'help', 'high', 'home', 'hope', 'idea', 'keep', 'kind', 'last', 'late', 'left', 'life', 'line', 'long', 'look', 'love', 'main', 'mind', 'much', 'name', 'near', 'need', 'next', 'nice', 'open', 'part', 'play', 'poor', 'real', 'rich', 'room', 'safe', 'same', 'seem', 'show', 'side', 'soft', 'soon', 'sort', 'stay', 'stop', 'such', 'sure', 'take', 'talk', 'tell', 'than', 'that', 'them', 'then', 'they', 'this', 'time', 'turn', 'walk', 'want', 'well', 'went', 'were', 'what', 'when', 'will', 'with', 'word', 'work', 'year', 'your'
        ]
        
        # Medium length words (5-7 letters) for natural phrases
        medium_words = [
            'about', 'after', 'again', 'along', 'among', 'around', 'before', 'behind', 'below', 'beneath', 'beside', 'between', 'beyond', 'during', 'except', 'inside', 'outside', 'through', 'toward', 'within', 'without', 'above', 'across', 'after', 'again', 'along', 'among', 'around', 'before', 'behind', 'below', 'beneath', 'beside', 'between', 'beyond', 'during', 'except', 'inside', 'outside', 'through', 'toward', 'within', 'without',
            'always', 'around', 'before', 'better', 'between', 'beyond', 'during', 'except', 'inside', 'outside', 'through', 'toward', 'within', 'without', 'across', 'after', 'again', 'along', 'among', 'around', 'before', 'behind', 'below', 'beneath', 'beside', 'between', 'beyond', 'during', 'except', 'inside', 'outside', 'through', 'toward', 'within', 'without',
            'against', 'already', 'another', 'because', 'between', 'beyond', 'during', 'except', 'inside', 'outside', 'through', 'toward', 'within', 'without', 'across', 'after', 'again', 'along', 'among', 'around', 'before', 'behind', 'below', 'beneath', 'beside', 'between', 'beyond', 'during', 'except', 'inside', 'outside', 'through', 'toward', 'within', 'without'
        ]
        
        # Longer words for single 10-letter phrases
        long_words = [
            'adventures', 'beautiful', 'challenge', 'dangerous', 'education', 'fantastic', 'generation', 'happiness', 'important', 'knowledge', 'leadership', 'management', 'necessary', 'operation', 'partnership', 'question', 'relationship', 'successful', 'technology', 'understanding', 'wonderful', 'excellent', 'fascinating', 'incredible', 'magnificent', 'outstanding', 'remarkable', 'spectacular', 'terrific', 'wonderful', 'brilliant', 'creative', 'delicious', 'energetic', 'friendly', 'graceful', 'handsome', 'intelligent', 'joyful', 'kindness', 'laughter', 'mysterious', 'peaceful', 'powerful', 'romantic', 'sensitive', 'talented', 'valuable', 'wonderful', 'zealous'
        ]
        
        self.word_lists['short_words'] = short_words
        self.word_lists['medium_words'] = medium_words
        self.word_lists['long_words'] = [w for w in long_words if len(w) == 10]
        
        # Add common phrase templates for more natural phrases
        self.phrase_templates = [
            # Adjective + Noun patterns
            ('good', 'vibes'), ('hot', 'pocket'), ('deep', 'space'), ('good', 'night'), 
            ('grape', 'soda'), ('sun', 'kissed'), ('game', 'night'), ('neon', 'light'),
            ('coffee', 'mug'), ('cool', 'beans'), ('quiet', 'room'), ('lemon', 'zest'),
            ('early', 'bird'), ('good', 'apple'), ('track', 'meet'), ('soup', 'spoon'),
            ('blind', 'date'), ('fire', 'drill'), ('trust', 'fall'), ('old', 'school'),
            ('chai', 'latte'), ('lucky', 'duck'), ('donut', 'shop'), ('open', 'world'),
            ('pink', 'cloud'), ('jazz', 'kicks'), ('calm', 'storm'), ('nine', 'lives'),
            ('rice', 'balls'), ('fast', 'camel'), ('crazy', 'frog'), ('spin', 'cycle'),
            ('pet', 'sitter'), ('green', 'room'), ('late', 'night'), ('soft', 'smile'),
            ('fried', 'fish'), ('wide', 'awake'),
            
            # Verb + Noun patterns
            ('i', 'love you'), ('i', 'eat food'), ('talk', 'a lot'), ('sip', 'slowly'),
            
            # Noun + Noun patterns
            ('paper', 'clips'), ('lime', 'twist'), ('jazz', 'hands'), ('bumble', 'bee'),
            
            # Common expressions
            ('good', 'morning'), ('good', 'evening'), ('good', 'afternoon'), ('good', 'luck'),
            ('take', 'care'), ('see', 'you'), ('nice', 'day'), ('happy', 'day'),
            ('sweet', 'dreams'), ('good', 'times'), ('best', 'wishes'), ('warm', 'welcome'),
            ('safe', 'travel'), ('easy', 'going'), ('free', 'spirit'), ('wild', 'child'),
            ('smart', 'cookie'), ('cool', 'cat'), ('hot', 'shot'), ('big', 'deal'),
            ('real', 'deal'), ('true', 'blue'), ('fair', 'play'), ('clean', 'sweep'),
            ('fresh', 'start'), ('new', 'beginning'), ('old', 'fashioned'), ('high', 'class'),
            ('low', 'key'), ('slow', 'motion'), ('fast', 'track'), ('quick', 'fix'),
            ('easy', 'money'), ('hard', 'work'), ('soft', 'touch'), ('rough', 'draft'),
            ('smooth', 'talk'), ('sharp', 'mind'), ('dull', 'moment'), ('bright', 'idea'),
            ('dark', 'horse'), ('light', 'bulb'), ('heavy', 'metal'), ('light', 'weight'),
            ('thick', 'skin'), ('thin', 'air'), ('wide', 'open'), ('narrow', 'escape'),
            ('high', 'five'), ('low', 'blow'), ('near', 'miss'), ('far', 'out'),
            ('early', 'bird'), ('late', 'bloomer'), ('soon', 'enough'), ('long', 'time'),
            ('short', 'cut'), ('full', 'house'), ('empty', 'nest'), ('open', 'book'),
            ('closed', 'mind'), ('free', 'will'), ('busy', 'bee'), ('easy', 'peasy'),
            ('hard', 'core'), ('simple', 'life'), ('complex', 'mind'), ('safe', 'space'),
            ('dangerous', 'game'), ('strong', 'will'), ('weak', 'link'), ('healthy', 'life'),
            ('sick', 'joke'), ('alive', 'and well'), ('dead', 'end'), ('real', 'talk'),
            ('fake', 'news'), ('true', 'story'), ('false', 'hope'), ('right', 'now'),
            ('wrong', 'turn'), ('same', 'old'), ('different', 'world'), ('similar', 'mind'),
            ('unique', 'style'), ('common', 'sense'), ('rare', 'find'), ('normal', 'day'),
            ('strange', 'world'), ('usual', 'suspect'), ('unusual', 'day'), ('regular', 'guy'),
            ('irregular', 'pattern'), ('perfect', 'match'), ('imperfect', 'world'), ('complete', 'set'),
            ('incomplete', 'thought'), ('finished', 'product'), ('unfinished', 'business'), ('ready', 'set'),
            ('not ready', 'yet'), ('willing', 'heart'), ('unwilling', 'participant'), ('able', 'bodied'),
            ('unable', 'to'), ('possible', 'dream'), ('impossible', 'task'), ('necessary', 'evil'),
            ('unnecessary', 'risk'), ('important', 'matter'), ('unimportant', 'detail'), ('useful', 'tool'),
            ('useless', 'information'), ('helpful', 'hint'), ('helpless', 'feeling'), ('hopeful', 'romantic'),
            ('hopeless', 'case'), ('careful', 'planning'), ('careless', 'mistake'), ('thoughtful', 'gift'),
            ('thoughtless', 'comment'), ('mindful', 'practice'), ('mindless', 'entertainment'), ('powerful', 'force'),
            ('powerless', 'feeling'), ('fearless', 'warrior'), ('fearful', 'thought'), ('colorful', 'language'),
            ('colorless', 'world'), ('tasteful', 'design'), ('tasteless', 'joke'), ('harmful', 'effect'),
            ('harmless', 'fun'), ('painful', 'truth'), ('painless', 'procedure')
        ]
    
    def generate_single_word_phrase(self) -> str:
        """Generate a single 10-letter word phrase"""
        valid_words = [word for word in self.word_lists['long_words'] 
                      if word.lower() not in self.existing_phrases]
        
        if not valid_words:
            # If no 10-letter words available, create compound words
            return self._create_compound_word()
        
        return random.choice(valid_words)
    
    def _create_compound_word(self) -> str:
        """Create a 10-letter compound word"""
        # Common compound word patterns
        compounds = [
            'playground', 'basketball', 'friendship', 'blacksmith', 'flashlight',
            'mastermind', 'calculator', 'electronic', 'definition', 'motivation',
            'commercial', 'controller', 'futuristic', 'reflection', 'endangered',
            'swimmingly', 'splendidly', 'pineapples', 'straighten', 'harmonized',
            'biochemist', 'duplicator', 'roadworthy', 'infallible', 'generation',
            'importance', 'collective', 'capitalize', 'structured', 'university',
            'plagiarize', 'bumblebees', 'squeezable', 'disqualify', 'adventures',
            'breathless', 'deliberate', 'screenshot', 'overcharge'
        ]
        
        valid_compounds = [word for word in compounds 
                          if word.lower() not in self.existing_phrases]
        
        if valid_compounds:
            return random.choice(valid_compounds)
        
        # Create new compound words
        prefixes = ['play', 'work', 'home', 'life', 'time', 'space', 'mind', 'heart', 'brain', 'hand']
        suffixes = ['ground', 'place', 'space', 'world', 'house', 'room', 'land', 'side', 'line', 'zone']
        
        for prefix in prefixes:
            for suffix in suffixes:
                compound = prefix + suffix
                if len(compound) == 10 and compound.lower() not in self.existing_phrases:
                    return compound
        
        # Fallback: create a random 10-letter word
        return self._generate_random_word(10)
    
    def _generate_random_word(self, length: int) -> str:
        """Generate a random word of specified length"""
        vowels = 'aeiou'
        consonants = 'bcdfghjklmnpqrstvwxyz'
        
        word = ''
        for i in range(length):
            if i % 2 == 0:  # Even positions get consonants
                word += random.choice(consonants)
            else:  # Odd positions get vowels
                word += random.choice(vowels)
        
        return word
    
    def generate_multi_word_phrase(self) -> str:
        """Generate a multi-word phrase that fits in 10 characters"""
        # First try phrase templates for natural, fluent phrases
        phrase = self._try_phrase_templates()
        if phrase and phrase.lower() not in self.existing_phrases:
            return phrase
        
        # Then try common phrase patterns from the existing data
        patterns = [
            # 3-4 letter word + 6-7 letter word
            (3, 7), (4, 6), (5, 5),
            # 2-3 letter word + 2-3 letter word + 4-6 letter word
            (2, 3, 5), (2, 4, 4), (3, 2, 5), (3, 3, 4),
            # 2 letter word + 2 letter word + 2 letter word + 4 letter word
            (2, 2, 2, 4)
        ]
        
        for pattern in patterns:
            phrase = self._try_pattern(pattern)
            if phrase and phrase.lower() not in self.existing_phrases:
                return phrase
        
        # Fallback: simple two-word phrase
        return self._create_simple_phrase()
    
    def _try_phrase_templates(self) -> str:
        """Try to create phrases using predefined templates"""
        # Filter templates that would fit in 10 characters
        valid_templates = []
        for template in self.phrase_templates:
            if len(template) == 2:
                phrase = f"{template[0]} {template[1]}"
                if len(phrase) == 10:
                    valid_templates.append(phrase)
            elif len(template) == 3:
                phrase = f"{template[0]} {template[1]} {template[2]}"
                if len(phrase) == 10:
                    valid_templates.append(phrase)
        
        # Try templates that aren't already used
        unused_templates = [t for t in valid_templates if t.lower() not in self.existing_phrases]
        
        if unused_templates:
            return random.choice(unused_templates)
        
        return None
    
    def _try_pattern(self, pattern: tuple) -> str:
        """Try to create a phrase with given word lengths"""
        phrase_parts = []
        total_length = 0
        
        for word_length in pattern:
            if word_length <= 4:
                word_list = self.word_lists['short_words']
            elif word_length <= 7:
                word_list = self.word_lists['medium_words']
            else:
                word_list = self.word_lists['long_words']
            
            # Filter words by exact length
            valid_words = [w for w in word_list if len(w) == word_length]
            
            if not valid_words:
                return None
            
            word = random.choice(valid_words)
            phrase_parts.append(word)
            total_length += len(word)
        
        # Add spaces between words
        phrase = ' '.join(phrase_parts)
        
        if len(phrase) == 10:
            return phrase
        
        return None
    
    def _create_simple_phrase(self) -> str:
        """Create a simple two-word phrase"""
        # Common adjective-noun combinations
        adjectives = ['good', 'bad', 'big', 'hot', 'old', 'new', 'red', 'blue', 'green', 'black', 'white', 'pink', 'gold', 'deep', 'soft', 'hard', 'fast', 'slow', 'loud', 'quiet', 'bright', 'dark', 'warm', 'cool', 'sweet', 'sour', 'fresh', 'clean', 'dirty', 'happy', 'sad', 'angry', 'calm', 'wild', 'brave', 'smart', 'funny', 'serious', 'lucky', 'rich', 'poor', 'young', 'wise', 'kind', 'mean', 'nice', 'rude', 'polite', 'shy', 'bold', 'gentle', 'rough', 'smooth', 'sharp', 'dull', 'heavy', 'light', 'thick', 'thin', 'wide', 'narrow', 'high', 'low', 'near', 'far', 'early', 'late', 'soon', 'long', 'short', 'full', 'empty', 'open', 'closed', 'free', 'busy', 'easy', 'hard', 'simple', 'complex', 'safe', 'dangerous', 'strong', 'weak', 'healthy', 'sick', 'alive', 'dead', 'real', 'fake', 'true', 'false', 'right', 'wrong', 'same', 'different', 'similar', 'unique', 'common', 'rare', 'normal', 'strange', 'usual', 'unusual', 'regular', 'irregular', 'perfect', 'imperfect', 'complete', 'incomplete', 'finished', 'unfinished', 'ready', 'not ready', 'willing', 'unwilling', 'able', 'unable', 'possible', 'impossible', 'necessary', 'unnecessary', 'important', 'unimportant', 'useful', 'useless', 'helpful', 'helpless', 'hopeful', 'hopeless', 'careful', 'careless', 'thoughtful', 'thoughtless', 'mindful', 'mindless', 'powerful', 'powerless', 'fearless', 'fearful', 'colorful', 'colorless', 'tasteful', 'tasteless', 'harmful', 'harmless', 'painful', 'painless', 'careful', 'careless', 'thoughtful', 'thoughtless', 'mindful', 'mindless', 'powerful', 'powerless', 'fearless', 'fearful', 'colorful', 'colorless', 'tasteful', 'tasteless', 'harmful', 'harmless', 'painful', 'painless']
        
        nouns = ['cat', 'dog', 'bird', 'fish', 'tree', 'flower', 'book', 'car', 'house', 'door', 'window', 'table', 'chair', 'bed', 'food', 'water', 'milk', 'bread', 'rice', 'meat', 'fruit', 'vegetable', 'apple', 'banana', 'orange', 'grape', 'strawberry', 'blueberry', 'raspberry', 'blackberry', 'cherry', 'peach', 'pear', 'plum', 'apricot', 'mango', 'pineapple', 'coconut', 'lemon', 'lime', 'grapefruit', 'tangerine', 'clementine', 'mandarin', 'kumquat', 'pomegranate', 'fig', 'date', 'prune', 'raisin', 'currant', 'cranberry', 'gooseberry', 'elderberry', 'mulberry', 'boysenberry', 'loganberry', 'tayberry', 'wineberry', 'cloudberry', 'salmonberry', 'thimbleberry', 'dewberry', 'huckleberry', 'lingonberry', 'bilberry', 'whortleberry', 'bearberry', 'cowberry', 'foxberry', 'partridgeberry', 'checkerberry', 'teaberry', 'wintergreen', 'sparkleberry', 'farkleberry', 'squawberry', 'buffaloberry', 'silverberry', 'autumnberry', 'russianberry', 'honeyberry', 'jostaberry', 'tayberry', 'wineberry', 'cloudberry', 'salmonberry', 'thimbleberry', 'dewberry', 'huckleberry', 'lingonberry', 'bilberry', 'whortleberry', 'bearberry', 'cowberry', 'foxberry', 'partridgeberry', 'checkerberry', 'teaberry', 'wintergreen', 'sparkleberry', 'farkleberry', 'squawberry', 'buffaloberry', 'silverberry', 'autumnberry', 'russianberry', 'honeyberry', 'jostaberry']
        
        for adj in adjectives:
            for noun in nouns:
                phrase = f"{adj} {noun}"
                if len(phrase) == 10 and phrase.lower() not in self.existing_phrases:
                    return phrase
        
        # If no perfect match, create a random phrase
        return self._generate_random_phrase()
    
    def _generate_random_phrase(self) -> str:
        """Generate a random phrase that fits 10 characters"""
        attempts = 0
        while attempts < 1000:
            # Favor multi-word phrases for more natural, fluent results
            if random.random() < 0.2:  # 20% chance for single word
                phrase = self.generate_single_word_phrase()
            else:
                phrase = self.generate_multi_word_phrase()
            
            if phrase and len(phrase) == 10 and phrase.lower() not in self.existing_phrases:
                return phrase
            
            attempts += 1
        
        # Last resort: create a simple phrase
        short_words = [w for w in self.word_lists['short_words'] if len(w) <= 4]
        if len(short_words) >= 2:
            word1 = random.choice(short_words)
            remaining_length = 9 - len(word1)  # 9 for space + second word
            word2_candidates = [w for w in short_words if len(w) == remaining_length]
            if word2_candidates:
                return f"{word1} {random.choice(word2_candidates)}"
        
        return "hello world"  # Fallback
    
    def generate_phrases(self, count: int = 10) -> List[str]:
        """Generate multiple unique phrases"""
        phrases = []
        attempts = 0
        max_attempts = count * 100
        
        while len(phrases) < count and attempts < max_attempts:
            phrase = self._generate_random_phrase()
            if phrase and phrase.lower() not in self.existing_phrases and phrase not in phrases:
                phrases.append(phrase)
            attempts += 1
        
        return phrases
    
    def validate_phrase(self, phrase: str) -> bool:
        """Validate if a phrase meets the requirements"""
        if not phrase or len(phrase) != 10:
            return False
        
        # Check for punctuation
        if re.search(r'[^\w\s]', phrase):
            return False
        
        # Check if it's fluent English (basic check)
        words = phrase.split()
        if len(words) == 1:
            # Single word should be a valid English word
            return len(phrase) == 10
        else:
            # Multi-word phrase should have valid words
            return all(len(word) > 0 for word in words)
    
    def add_phrase_to_file(self, phrase: str, date: str = None):
        """Add a new phrase to words.txt"""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        if self.validate_phrase(phrase):
            with open('words.txt', 'a') as file:
                file.write(f"{date}, {phrase}\n")
            self.existing_phrases.add(phrase.lower())
            return True
        return False

def main():
    """Main function to demonstrate the phrase generator"""
    generator = PhraseGenerator()
    
    print("Generated phrases:")
    phrases = generator.generate_phrases(20)
    
    for i, phrase in enumerate(phrases, 1):
        print(f"{i:2d}. '{phrase}' ({len(phrase)} chars)")
    
    print(f"\nTotal phrases generated: {len(phrases)}")
    print(f"Existing phrases loaded: {len(generator.existing_phrases)}")

if __name__ == "__main__":
    main() 