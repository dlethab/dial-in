#!/usr/bin/env python3
"""
Daily Phrase Generator Agent

Generates exactly 10-character phrases (including spaces) for daily word games.
Phrases must be common English words/phrases without punctuation.
"""

import random
from datetime import datetime, timedelta
from typing import List, Tuple
import re

class PhraseGenerator:
    def __init__(self):
        # Collection of exactly 10-character phrases and words
        self.ten_char_words = [
            # Single 10-letter words
            "accomplish", "accelerate", "accessible", "accumulate", "advantages", 
            "adventures", "amplifiers", "antibodies", "appreciate", "atmosphere",
            "background", "basketball", "beachfront", "beneficial", "birthplace",
            "blacksmith", "boundaries", "breadcrumb", "breakfast", "breathless",
            "calculator", "candidates", "capitalize", "categories", "celebrated",
            "chalkboard", "changeable", "characters", "checkpoint", "cigarettes",
            "clockworks", "collective", "commercial", "commission", "committees",
            "comparable", "complement", "complaints", "components", "computers",
            "conclusion", "conditions", "conference", "confidence", "configured",
            "connecting", "constitute", "consultant", "controller", "correspond",
            "creativity", "curiosity", "curriculum", "customers", "dashboard",
            "decoration", "definition", "deliberate", "democratic", "department",
            "dependence", "depression", "directions", "directory", "discipline",
            "discovered", "discussion", "distribute", "documents", "dragonfly",
            "duplicator", "economical", "economies", "electronic", "emphasized",
            "endangered", "engagement", "enterprises", "equivalent", "especially",
            "everywhere", "exaggerate", "excellence", "executable", "experience",
            "experiment", "expression", "facilities", "federation", "fireplace",
            "flashlight", "foundation", "friendship", "futuristic", "generation",
            "goldsmith", "government", "greenhouse", "guidelines", "halloween",
            "harmonized", "helicopter", "hemisphere", "highlight", "housework",
            "importance", "impression", "incredible", "infallible", "ingredient",
            "initiative", "innovation", "inspection", "instrument", "integrated",
            "inventory", "investment", "jellyfish", "journalism", "keyboards",
            "knowledge", "laboratory", "landscape", "leadership", "literally",
            "machinery", "magnificent", "management", "manuscript", "mastermind",
            "mechanical", "membership", "messenger", "meteorite", "microphone",
            "motivation", "multimedia", "mysterious", "navigation", "necessary",
            "networking", "newspaper", "operations", "optimistic", "organizing",
            "overcharge", "paperwork", "parameters", "partnership", "percentage",
            "permission", "photograph", "playground", "population", "preference",
            "prescribed", "principles", "procedures", "production", "profession",
            "programmer", "properties", "protection", "psychology", "publishing",
            "punishment", "purchasing", "questions", "raindrops", "reflection",
            "registered", "regulation", "remarkable", "reputation", "resolution",
            "restaurant", "revolution", "roadworthy", "satellite", "screenshot",
            "searching", "secretary", "securities", "significant", "similarity",
            "simplicity", "somewhere", "specialist", "splendidly", "statistics",
            "storytell", "strengthen", "structured", "substitute", "successful",
            "suggestion", "supervisor", "swimmingly", "technology", "television",
            "temperance", "themselves", "tournament", "traditions", "transport",
            "treatments", "ultimately", "understand", "university", "uplifting",
            "vacations", "vegetables", "waterfall", "wavelength", "wheelchair",
            "wilderness", "workplace", "yesterday", "zealously"
        ]
        
        self.two_word_phrases = [
            # 2-word phrases (total 10 chars including space)
            "air force", "apple pie", "art class", "back door", "back yard",
            "bad habit", "bank loan", "beach day", "bear hug", "best bet",
            "best deal", "best friend", "bike ride", "bird cage", "blind date",
            "blue jean", "blue moon", "blue ocean", "boat ride", "book club",
            "book fair", "book mark", "book store", "box office", "bread box",
            "bug spray", "bus fare", "bus stop", "cake mix", "calm down",
            "calm seas", "calm storm", "camp fire", "car door", "car keys",
            "car loan", "car park", "car pool", "car race", "car show",
            "card game", "cash back", "cat food", "chair leg", "chai latte",
            "city hall", "city life", "city park", "class act", "clean air",
            "clock face", "code name", "coffee mug", "coin flip", "cold cuts",
            "cool beans", "cool down", "cost less", "cover art", "crazy frog",
            "cry babies", "dance club", "dance floor", "dark room", "data base",
            "day care", "day dream", "deep dish", "deep dive", "deep love",
            "deep sea", "deep space", "desk lamp", "dog food", "dog park",
            "dog walk", "door bell", "door frame", "door knob", "door step",
            "donut shop", "drag race", "drag racer", "dry clean", "dry ice",
            "ear plug", "early bird", "egg roll", "error word", "eye candy",
            "face mask", "fair play", "fair trade", "fall down", "fan club",
            "fast bike", "fast camel", "fast car", "fast food", "fast lane",
            "file name", "fire ant", "fire bell", "fire dept", "fire drill",
            "fire exit", "fire lane", "fire sale", "fish bowl", "fish cake",
            "fish hook", "fish tank", "flash drive", "flat tire", "fly away",
            "folk art", "food bank", "food cart", "food fair", "foot bath",
            "free gift", "free ride", "free time", "fresh air", "fried fish",
            "fried rice", "front door", "front end", "front row", "full moon",
            "fun fact", "funny joke", "game night", "game plan", "game room",
            "game show", "gas mask", "gift bag", "gift box", "gift card",
            "gift shop", "girl band", "glass box", "go ahead", "go fast",
            "go fish", "go home", "goal line", "gold band", "gold chain",
            "gold coin", "gold fish", "gold leaf", "gold mine", "gold ring",
            "good apple", "good book", "good deal", "good food", "good game",
            "good idea", "good joke", "good life", "good luck", "good mood",
            "good news", "good night", "good point", "good show", "good song",
            "good time", "good vibes", "good will", "good work", "grape soda",
            "grass fed", "green bean", "green card", "green room", "green tea",
            "grey area", "guest room", "hair band", "hair clip", "hair cut",
            "hair loss", "half moon", "half time", "ham radio", "hand bag",
            "hand book", "hand made", "hand over", "hand pick", "hand soap",
            "hard copy", "hard disk", "hard fact", "hard luck", "hard rock",
            "head band", "head cold", "head lamp", "head line", "head shot",
            "help desk", "help line", "help menu", "high five", "high gear",
            "high jump", "high noon", "high road", "high tech", "high tide",
            "hill side", "home base", "home brew", "home game", "home loan",
            "home made", "home page", "home run", "home team", "home town",
            "hot air", "hot cocoa", "hot dog", "hot drink", "hot meal",
            "hot plate", "hot pocket", "hot sauce", "hot spot", "hot stove",
            "hot tub", "hot water", "house cat", "house key", "house keys",
            "ice cold", "ice cream", "ice cube", "ice pack", "ice pick",
            "ice rink", "ice skate", "idea bank", "ink pad", "ink pen",
            "iron bar", "iron gate", "iron ore", "jazz band", "jazz club",
            "jazz hands", "jazz kicks", "jazz song", "job fair", "job hunt",
            "joke book", "jump rope", "jump shot", "jump suit", "jury duty",
            "key board", "key card", "key chain", "key hole", "key lime",
            "key note", "key ring", "kick ball", "kick box", "kick start",
            "kind word", "lake side", "lamp post", "land fill", "land lord",
            "land mark", "land mine", "land use", "last call", "last dance",
            "last game", "last name", "last shot", "last week", "late night",
            "law book", "law firm", "lawn care", "lead role", "leaf pile",
            "left hand", "left lane", "left turn", "lemon cake", "lemon drop",
            "lemon pie", "lemon tree", "lemon zest", "life boat", "life line",
            "life long", "life ring", "life size", "life span", "light box",
            "light ray", "lime juice", "lime tree", "lime twist", "line art",
            "line cook", "line cut", "line drive", "line item", "line up",
            "live band", "live chat", "live feed", "live show", "live wire",
            "loan desk", "long arm", "long boat", "long day", "long face",
            "long game", "long hair", "long haul", "long jump", "long list",
            "long lost", "long odds", "long road", "long run", "long shot",
            "long term", "long time", "long walk", "long way", "look back",
            "look down", "look here", "look out", "look up", "love bird",
            "love boat", "love game", "love note", "love seat", "love song",
            "lucky day", "lucky dog", "lucky duck", "lunch box", "lunch date",
            "lunch hour", "lunch meat", "lunch room", "lunch time", "magic act",
            "magic eye", "magic hat", "magic pen", "magic show", "mail bag",
            "mail box", "mail cart", "mail list", "mail room", "mail slot",
            "main dish", "main door", "main drag", "main idea", "main line",
            "main page", "main road", "main room", "main sail", "main stem",
            "map book", "map case", "map out", "mask off", "meal deal",
            "meal plan", "meal prep", "meal time", "meat ball", "meat hook",
            "meat loaf", "meet up", "milk farm", "milk jug", "milk shake",
            "mind game", "mind map", "mix tape", "moon beam", "moon cake",
            "moon glow", "moon light", "moon rock", "moon shot", "moon walk",
            "move fast", "move on", "move out", "movie fan", "movie star",
            "music box", "name tag", "navy blue", "near miss", "neon light",
            "neon sign", "nest egg", "net gain", "net loss", "new baby",
            "new book", "new breed", "new car", "new deal", "new door",
            "new face", "new game", "new hand", "new home", "new hope",
            "new idea", "new item", "new job", "new leaf", "new life",
            "new look", "new moon", "new move", "new name", "new path",
            "new plan", "new play", "new rule", "new sale", "new shoe",
            "new shoes", "new show", "new song", "new spot", "new star",
            "new step", "new story", "new talk", "new team", "new time",
            "new town", "new tree", "new wave", "new way", "new week",
            "new wine", "new word", "new work", "new year", "news feed",
            "news item", "news line", "news room", "nice day", "nice gift",
            "nice guy", "nice hat", "nice home", "nice idea", "nice job",
            "nice lake", "nice life", "nice look", "nice meal", "nice move",
            "nice park", "nice plan", "nice play", "nice ride", "nice room",
            "nice shot", "nice show", "nice talk", "nice team", "nice time",
            "nice town", "nice try", "nice view", "nice walk", "nice way",
            "nice work", "night cap", "night club", "night fly", "night gown",
            "night job", "night life", "night mare", "night owl", "night sea",
            "night sky", "night stand", "night time", "nine iron", "nine lives",
            "no doubt", "no entry", "no exit", "no fear", "no luck",
            "no mercy", "no name", "no place", "no rush", "no time",
            "no way", "noon day", "nose art", "nose cone", "note book",
            "note card", "note pad", "nut case", "oak tree", "odd ball",
            "oil drum", "oil field", "oil paint", "old bag", "old car",
            "old coin", "old days", "old dog", "old face", "old folk",
            "old game", "old guard", "old hand", "old hat", "old home",
            "old joke", "old lady", "old line", "old look", "old maid",
            "old mail", "old man", "old news", "old path", "old play",
            "old road", "old rule", "old salt", "old saw", "old school",
            "old shoe", "old song", "old soul", "old step", "old tale",
            "old team", "old time", "old town", "old tree", "old view",
            "old way", "old wine", "old work", "one day", "one game",
            "one hand", "one hour", "one idea", "one item", "one last",
            "one life", "one line", "one look", "one love", "one meal",
            "one mile", "one more", "one move", "one name", "one page",
            "one part", "one play", "one point", "one room", "one shot",
            "one show", "one side", "one song", "one star", "one step",
            "one stop", "one story", "one take", "one team", "one time",
            "one town", "one tree", "one turn", "one type", "one view",
            "one vote", "one walk", "one way", "one week", "one word",
            "one work", "one year", "open air", "open book", "open call",
            "open car", "open door", "open end", "open eye", "open face",
            "open fire", "open game", "open hand", "open home", "open hour",
            "open line", "open loop", "open mind", "open page", "open plan",
            "open play", "open road", "open room", "open sea", "open shop",
            "open side", "open sky", "open space", "open talk", "open time",
            "open view", "open way", "open wire", "open work", "open world",
            "over arm", "over easy", "over flow", "over head", "over heat",
            "over jump", "over kill", "over land", "over load", "over look",
            "over play", "over ride", "over rule", "over sea", "over shot",
            "over size", "over stay", "over step", "over take", "over time",
            "over turn", "over use", "over work", "pack ice", "pack up",
            "page one", "page two", "pain free", "pan cake", "paper bag",
            "paper boy", "paper cup", "paper cut", "paper jam", "paper map",
            "park bench", "park land", "part one", "part two", "pass by",
            "pass out", "pass word", "past due", "past life", "past time",
            "pay back", "pay bill", "pay day", "pay off", "pay out",
            "pay roll", "peace out", "peak hour", "peak time", "pen pal",
            "pet care", "pet fish", "pet food", "pet name", "pet rock",
            "pet shop", "pet show", "pet sitter", "phone app", "phone bag",
            "phone book", "phone box", "phone call", "phone line", "phone tag",
            "photo op", "pick up", "pie chart", "pink cloud", "pizza box",
            "plan out", "play ball", "play book", "play boy", "play date",
            "play fair", "play game", "play hard", "play land", "play list",
            "play mate", "play pen", "play room", "play time", "pool ball",
            "pool deck", "pool hall", "pool party", "pool side", "pool time",
            "post box", "post card", "post date", "post game", "post hole",
            "post man", "post mark", "post note", "post time", "price cut",
            "price tag", "prize win", "pub quiz", "pull down", "pull out",
            "pull over", "pull up", "pump gas", "push back", "push down",
            "push out", "push over", "push up", "put away", "put back",
            "put down", "put on", "put out", "put up", "quiz bowl",
            "quiz game", "quiz show", "quiz time", "race car", "race day",
            "race fan", "race game", "race meet", "race pace", "race team",
            "race time", "race track", "race way", "radio ad", "radio fan",
            "radio hit", "radio show", "radio talk", "rain boot", "rain boots",
            "rain bow", "rain coat", "rain dance", "rain day", "rain drop",
            "rain fall", "rain gear", "rain hat", "rain make", "rain out",
            "rain storm", "rain time", "rain wear", "rain wind", "rain work",
            "read me", "read on", "read out", "red barn", "red bean",
            "red bell", "red bike", "red bird", "red book", "red box",
            "red brick", "red bug", "red cake", "red cap", "red car",
            "red card", "red cent", "red clay", "red coat", "red cone",
            "red deer", "red dirt", "red door", "red dot", "red drum",
            "red duck", "red dye", "red eye", "red face", "red fern",
            "red fire", "red fish", "red flag", "red fox", "red frog",
            "red gate", "red gold", "red hand", "red hat", "red head",
            "red heat", "red hill", "red hook", "red horn", "red horse",
            "red ice", "red ink", "red iron", "red jade", "red jam",
            "red lake", "red lamp", "red leaf", "red lens", "red line",
            "red lion", "red list", "red lock", "red look", "red mask",
            "red meat", "red mile", "red mint", "red moon", "red nose",
            "red onion", "red owl", "red page", "red pear", "red pen",
            "red pill", "red pine", "red pipe", "red pool", "red rock",
            "red room", "red rope", "red rose", "red sage", "red sand",
            "red sea", "red seed", "red ship", "red shop", "red sign",
            "red sky", "red slip", "red snow", "red sock", "red soil",
            "red soup", "red spot", "red star", "red stem", "red tape",
            "red tea", "red tent", "red tide", "red tile", "red tone",
            "red tool", "red top", "red tree", "red vest", "red wall",
            "red wave", "red wine", "red wing", "red wood", "red wool",
            "red work", "red yard", "rice ball", "rice balls", "ride home",
            "ride on", "ride out", "right arm", "right eye", "right hand",
            "right way", "ring back", "ring tone", "river bed", "road bike",
            "road crew", "road kill", "road map", "road rage", "road race",
            "road side", "road sign", "road test", "road trip", "road way",
            "road work", "rock band", "rock beat", "rock face", "rock fall",
            "rock hard", "rock hill", "rock salt", "rock song", "rock star",
            "rock wall", "roll back", "roll call", "roll out", "roll over",
            "roll up", "room key", "room mate", "room size", "room temp",
            "rope burn", "rope walk", "rose bush", "rose gold", "rose wine",
            "round off", "round one", "round out", "round trip", "round two",
            "run away", "run back", "run down", "run fast", "run home",
            "run off", "run out", "run over", "run time", "run up",
            "safe bet", "safe box", "safe door", "safe game", "safe hand",
            "safe home", "safe house", "safe line", "safe play", "safe ride",
            "safe room", "safe shot", "safe side", "safe talk", "safe time",
            "safe trip", "safe way", "safe word", "safe work", "safe zone",
            "salt air", "salt free", "salt lake", "salt mine", "salt rock",
            "salt sea", "salt water", "sand bag", "sand bar", "sand box",
            "sand cake", "sand cast", "sand dune", "sand hill", "sand lot",
            "sand pit", "sand stone", "sand time", "sand trap", "sand walk",
            "save face", "save game", "save me", "save time", "say hello",
            "say hi", "say no", "say yes", "school bag", "school boy",
            "school bus", "school day", "school fee", "sea bird", "sea boat",
            "sea dog", "sea foam", "sea food", "sea gate", "sea gull",
            "sea horse", "sea ice", "sea lane", "sea level", "sea life",
            "sea lion", "sea log", "sea mail", "sea mile", "sea port",
            "sea rock", "sea room", "sea salt", "sea side", "sea song",
            "sea star", "sea wall", "sea water", "sea wave", "sea weed",
            "sea wind", "seat belt", "sell out", "send off", "set back",
            "set down", "set free", "set off", "set out", "set sail",
            "set up", "ship date", "ship deck", "ship load", "ship mate",
            "ship out", "ship yard", "shoe box", "shoe horn", "shoe lace",
            "shoe shop", "shoe size", "shop talk", "short cut", "short run",
            "show boat", "show case", "show down", "show girl", "show off",
            "show room", "show time", "shut down", "shut off", "shut out",
            "shut up", "side arm", "side bar", "side bet", "side bone",
            "side car", "side dish", "side door", "side eye", "side kick",
            "side line", "side load", "side note", "side road", "side room",
            "side show", "side step", "side track", "side view", "side walk",
            "side wall", "side way", "side wind", "silk road", "silk scarf",
            "silk tie", "sing out", "sing song", "sip slowly", "sit back",
            "sit down", "sit in", "sit out", "sit up", "six pack",
            "size up", "skill set", "skip out", "sky blue", "sky dive",
            "sky high", "sky hook", "sky light", "sky line", "sky view",
            "sky walk", "sky way", "slip away", "slip by", "slip off",
            "slip on", "slip out", "slip up", "slow boat", "slow burn",
            "slow down", "slow lane", "slow leak", "slow move", "slow news",
            "slow pace", "slow play", "slow ride", "slow song", "slow time",
            "slow walk", "slow wave", "small bet", "small box", "small car",
            "small fry", "small hit", "small town", "snap back", "snap out",
            "snap shot", "snap up", "snow ball", "snow bank", "snow bird",
            "snow boot", "snow cone", "snow day", "snow fall", "snow flake",
            "snow fort", "snow hat", "snow hill", "snow job", "snow line",
            "snow man", "snow pack", "snow pea", "snow pile", "snow shoe",
            "snow ski", "snow suit", "snow tire", "snow top", "snow walk",
            "soap box", "soap film", "soap foam", "soap opera", "soap suds",
            "soft ball", "soft core", "soft drink", "soft hit", "soft rock",
            "soft sell", "soft skin", "soft smile", "soft spot", "soft talk",
            "soft top", "soft toy", "soft wave", "song bird", "song book",
            "song fest", "song hit", "song list", "song play", "song time",
            "soup bowl", "soup can", "soup cup", "soup dish", "soup line",
            "soup mix", "soup pot", "soup spoon", "sour ball", "sour cream",
            "sour face", "sour grape", "sour milk", "sour note", "space age",
            "space bar", "space jam", "space lab", "space man", "space out",
            "space race", "space ship", "space suit", "space time", "space walk",
            "speak out", "speak up", "speed bag", "speed boat", "speed bump",
            "speed dial", "speed gun", "speed limit", "speed run", "speed test",
            "speed trap", "speed up", "spell out", "spin bike", "spin class",
            "spin cycle", "spin dry", "spin off", "spin out", "spin top",
            "split end", "split lip", "split off", "split pea", "split up",
            "spot check", "spot light", "spot on", "spot test", "spring back",
            "spring day", "spring fed", "spring mix", "spring roll", "spring time",
            "square box", "square cut", "square deal", "square foot", "square off",
            "square one", "square peg", "square root", "square up", "stand back",
            "stand by", "stand down", "stand fast", "stand in", "stand off",
            "stand out", "stand up", "star fish", "star fruit", "star gate",
            "star light", "star map", "star sign", "star trek", "star wars",
            "start off", "start out", "start over", "start up", "stay back",
            "stay calm", "stay cool", "stay down", "stay here", "stay home",
            "stay in", "stay low", "stay out", "stay over", "stay put",
            "stay safe", "stay up", "stay warm", "steam bath", "steam boat",
            "steam box", "steam car", "steam heat", "steam iron", "steam room",
            "step back", "step by", "step down", "step in", "step off",
            "step on", "step out", "step over", "step up", "stick around",
            "stick by", "stick out", "stick shift", "stick to", "stick up",
            "stop by", "stop gap", "stop in", "stop off", "stop out",
            "stop over", "stop sign", "stop time", "storm door", "storm out",
            "story book", "story line", "story tell", "story time", "sub way",
            "suit case", "sum up", "sun beam", "sun block", "sun burn",
            "sun dial", "sun down", "sun dry", "sun fish", "sun flower",
            "sun glass", "sun hat", "sun kissed", "sun lamp", "sun light",
            "sun room", "sun screen", "sun set", "sun shine", "sun spot",
            "sun tan", "sun up", "sunny day", "sunny side", "surf board",
            "surf club", "surf shop", "surf side", "surf time", "surf wave",
            "sweet bee", "sweet corn", "sweet deal", "sweet home", "sweet pea",
            "sweet roll", "sweet shop", "sweet talk", "sweet tea", "sweet tooth",
            "swim cap", "swim club", "swim meet", "swim suit", "swim team",
            "swim time", "swing by", "swing dance", "swing out", "swing set",
            "switch off", "switch on", "switch out", "switch up", "table fan",
            "table leg", "table saw", "table top", "take away", "take back",
            "take care", "take down", "take five", "take home", "take in",
            "take note", "take off", "take on", "take out", "take over",
            "take part", "take turn", "take up", "talk back", "talk down",
            "talk fast", "talk loud", "talk low", "talk out", "talk over",
            "talk show", "talk soft", "talk time", "talk up", "talk a lot",
            "tall tale", "tall tree", "tan line", "tape deck", "tape loop",
            "tape measure", "tea bag", "tea box", "tea cake", "tea cup",
            "tea house", "tea leaf", "tea party", "tea pot", "tea room",
            "tea set", "tea shop", "tea time", "tea tree", "team lead",
            "team mate", "team play", "team work", "tear drop", "tear gas",
            "tell all", "tell me", "tell off", "tell on", "tell tale",
            "ten cent", "ten fold", "ten foot", "ten mile", "ten spot",
            "ten yard", "test case", "test drive", "test out", "test run",
            "test site", "text book", "text box", "text file", "text line",
            "text me", "text page", "thank you", "the best", "the deal",
            "the end", "the fact", "the game", "the idea", "the joke",
            "the look", "the move", "the news", "the one", "the plan",
            "the play", "the point", "the real", "the ride", "the room",
            "the rule", "the same", "the show", "the side", "the song",
            "the spot", "the star", "the step", "the talk", "the team",
            "the time", "the town", "the tree", "the turn", "the view",
            "the walk", "the wall", "the wave", "the way", "the week",
            "the wind", "the word", "the work", "the yard", "think big",
            "think fast", "think hard", "think out", "think over", "think up",
            "three day", "three way", "throw away", "throw back", "throw down",
            "throw in", "throw off", "throw out", "throw up", "thumb down",
            "thumb drive", "thumb nail", "thumb tack", "thumb up", "tick off",
            "tide pool", "tie back", "tie down", "tie game", "tie in",
            "tie off", "tie on", "tie up", "tight end", "tight fit",
            "tight rope", "tight spot", "time bomb", "time card", "time fly",
            "time off", "time out", "time slot", "time span", "time zone",
            "tip off", "tip over", "tip toe", "tip top", "tire out",
            "toast rack", "today only", "toe nail", "tone down", "tone up",
            "tool bag", "tool bar", "tool belt", "tool box", "tool kit",
            "tool room", "tool shed", "top bar", "top box", "top card",
            "top coat", "top dog", "top down", "top end", "top gear",
            "top gun", "top hat", "top hit", "top job", "top line",
            "top notch", "top off", "top pick", "top rank", "top rate",
            "top rope", "top row", "top seal", "top shelf", "top side",
            "top soil", "top song", "top spot", "top step", "top team",
            "top ten", "top tier", "top time", "top view", "top vote",
            "top wall", "top water", "top wave", "toy box", "toy car",
            "toy dog", "toy gun", "toy shop", "toy store", "track down",
            "track meet", "track out", "track pad", "track run", "track star",
            "track suit", "track team", "trade fair", "trade in", "trade off",
            "trade show", "trade up", "train car", "train fare", "train ride",
            "train set", "train stop", "trash bag", "trash can", "tree farm",
            "tree fort", "tree frog", "tree line", "tree ring", "tree top",
            "trip out", "trip over", "trip up", "truck bed", "truck cab",
            "truck farm", "truck load", "truck stop", "true blue", "true fact",
            "true life", "true love", "true name", "true self", "true story",
            "true test", "true tone", "trust fall", "try again", "try hard",
            "try out", "tune in", "tune out", "tune up", "turn back",
            "turn down", "turn in", "turn left", "turn off", "turn on",
            "turn out", "turn over", "turn right", "turn up", "two cents",
            "two door", "two face", "two fold", "two hand", "two lane",
            "two part", "two step", "two time", "two tone", "two way",
            "two week", "two year", "type cast", "type face", "type in",
            "type out", "type set", "type writer", "under age", "under arm",
            "under cut", "under dog", "under way", "up beat", "up date",
            "up grade", "up hill", "up keep", "up lift", "up load",
            "up right", "up scale", "up side", "up stage", "up state",
            "up swing", "up tight", "up time", "up town", "up turn",
            "up ward", "up wind", "used car", "user fee", "user name",
            "view port", "voice box", "voice mail", "vote down", "vote for",
            "vote in", "vote out", "vote up", "wait line", "wait list",
            "wait room", "wait time", "wake up", "walk away", "walk by",
            "walk down", "walk in", "walk off", "walk on", "walk out",
            "walk over", "walk past", "walk through", "walk to", "walk up",
            "wall art", "wall clock", "wall map", "wall safe", "wall unit",
            "warm day", "warm heart", "warm hug", "warm hugs", "warm milk",
            "warm room", "warm sun", "warm up", "warm wind", "wash away",
            "wash day", "wash down", "wash off", "wash out", "wash room",
            "wash up", "waste bin", "waste not", "watch dog", "watch for",
            "watch me", "watch out", "watch over", "water bag", "water bed",
            "water bike", "water bird", "water bowl", "water bug", "water can",
            "water cool", "water drop", "water fall", "water gun", "water hole",
            "water hose", "water ice", "water jug", "water leak", "water lily",
            "water line", "water log", "water main", "water mark", "water mill",
            "water park", "water pipe", "water play", "water pump", "water rat",
            "water ride", "water ring", "water run", "water ski", "water slide",
            "water tank", "water test", "water time", "water toy", "water tube",
            "water wall", "water wave", "water way", "water well", "water wing",
            "wave back", "wave bye", "wave down", "wave form", "wave good",
            "wave hi", "wave off", "wave pool", "wave top", "way back",
            "way down", "way off", "way out", "way over", "way past",
            "way point", "way side", "way station", "way stop", "way through",
            "way to", "way up", "weak link", "weak spot", "web cam",
            "web page", "web ring", "web site", "week day", "week end",
            "week long", "well done", "well fed", "well kept", "well made",
            "well off", "well read", "well worn", "wet bar", "wet day",
            "wet dock", "wet dream", "wet fish", "wet foot", "wet hair",
            "wet land", "wet look", "wet paint", "wet rock", "wet room",
            "wet sand", "wet suit", "wet towel", "wet wall", "wet wash",
            "what if", "what not", "what now", "wheel base", "wheel chair",
            "when ever", "where as", "where by", "white ant", "white bar",
            "white bat", "white bee", "white box", "white boy", "white bug",
            "white bus", "white cab", "white cap", "white car", "white cat",
            "white cow", "white cup", "white cut", "white day", "white dew",
            "white dog", "white dot", "white ear", "white egg", "white elk",
            "white eye", "white fan", "white fat", "white fin", "white fir",
            "white fit", "white fly", "white fog", "white fox", "white fur",
            "white gas", "white gem", "white gum", "white gun", "white hat",
            "white hen", "white hog", "white hot", "white ice", "white ink",
            "white jam", "white jet", "white job", "white key", "white lab",
            "white law", "white leg", "white lie", "white man", "white map",
            "white mat", "white meat", "white milk", "white mix", "white mud",
            "white net", "white oak", "white oil", "white out", "white owl",
            "white pad", "white pan", "white paw", "white pea", "white pen",
            "white pet", "white pie", "white pig", "white pin", "white pit",
            "white pot", "white rat", "white ray", "white red", "white rice",
            "white rim", "white rod", "white room", "white rope", "white rose",
            "white rum", "white run", "white sag", "white sand", "white sea",
            "white set", "white sex", "white she", "white sky", "white snow",
            "white sock", "white soil", "white song", "white spot", "white star",
            "white sun", "white tea", "white tie", "white tip", "white top",
            "white toy", "white van", "white war", "white way", "white web",
            "white wig", "white win", "white wine", "white wing", "white wolf",
            "white wood", "white wool", "white worm", "white yard", "who else",
            "who knows", "why not", "wide area", "wide awake", "wide base",
            "wide belt", "wide door", "wide eye", "wide face", "wide flat",
            "wide gate", "wide gulf", "wide hand", "wide lane", "wide leg",
            "wide line", "wide load", "wide look", "wide loop", "wide mouth",
            "wide open", "wide path", "wide plan", "wide range", "wide road",
            "wide room", "wide seat", "wide shot", "wide side", "wide sky",
            "wide smile", "wide span", "wide spot", "wide step", "wide tire",
            "wide turn", "wide view", "wide wall", "wild bear", "wild bird",
            "wild boar", "wild card", "wild cat", "wild deer", "wild dog",
            "wild duck", "wild fire", "wild fish", "wild fowl", "wild game",
            "wild goat", "wild hair", "wild hare", "wild hog", "wild horse",
            "wild hunt", "wild lamb", "wild land", "wild life", "wild mint",
            "wild oat", "wild ox", "wild pig", "wild rice", "wild ride",
            "wild rose", "wild side", "wild swan", "wild time", "wild type",
            "wild west", "wild wind", "wild wolf", "wind bag", "wind blow",
            "wind box", "wind burn", "wind chill", "wind down", "wind farm",
            "wind mill", "wind pipe", "wind storm", "wind surf", "wind up",
            "wine bar", "wine box", "wine cave", "wine club", "wine cork",
            "wine cup", "wine fair", "wine fest", "wine glass", "wine list",
            "wine rack", "wine red", "wine room", "wine shop", "wine time",
            "wine tour", "wing back", "wing beat", "wing nut", "wing span",
            "wing tip", "wipe away", "wipe down", "wipe off", "wipe out",
            "wire cage", "wire cut", "wire feed", "wire frame", "wire net",
            "wire rope", "wire run", "wise guy", "wise man", "wish bone",
            "wish list", "with draw", "with hold", "with in", "with out",
            "with stand", "wood bat", "wood bed", "wood bin", "wood block",
            "wood boat", "wood box", "wood burn", "wood chip", "wood cut",
            "wood deck", "wood fire", "wood folk", "wood frame", "wood glue",
            "wood land", "wood pile", "wood post", "wood pulp", "wood shed",
            "wood shop", "wood side", "wood stain", "wood stove", "wood work",
            "wool cap", "wool coat", "wool hat", "wool rug", "wool sock",
            "word book", "word game", "word list", "word play", "word wise",
            "work area", "work bag", "work bank", "work bay", "work bench",
            "work boat", "work book", "work boot", "work box", "work camp",
            "work cell", "work crew", "work day", "work desk", "work done",
            "work flow", "work folk", "work force", "work form", "work gang",
            "work gear", "work group", "work hand", "work hard", "work home",
            "work hour", "work item", "work land", "work late", "work life",
            "work line", "work load", "work log", "work loss", "work mate",
            "work out", "work over", "work pace", "work place", "work plan",
            "work play", "work room", "work rule", "work safe", "work shirt",
            "work shop", "work site", "work song", "work space", "work spot",
            "work team", "work time", "work tool", "work trip", "work unit",
            "work up", "work week", "work well", "work wise", "work yard",
            "work zone", "world art", "world beat", "world book", "world cup",
            "world end", "world fair", "world game", "world map", "world news",
            "world play", "world rock", "world song", "world tour", "world war",
            "world wide", "year book", "year end", "year long", "year old",
            "year one", "year round", "year two", "yes man", "yes vote",
            "you bet", "you know", "you win", "young age", "young boy",
            "young gun", "young kid", "young man", "your call", "your move",
            "your turn", "zero hour", "zero in", "zero out", "zip code",
            "zip file", "zip line", "zip lock", "zip up", "zone out",
            "zoom call", "zoom in", "zoom lens", "zoom out"
        ]
        
        self.three_word_phrases = [
            # 3-word phrases (total 10 chars including spaces) 
            "i love you", "i eat food", "go to bed", "see you", "hi there", 
            "bye now", "yes i can", "no i cant", "me too", "you rock",
            "so cool", "very nice", "too bad", "oh well", "be nice", 
            "go home", "come back", "stay here", "look out", "watch it",
            "slow down", "speed up", "turn left", "go right", "sit down",
            "stand up", "wake up", "go sleep", "eat more", "drink up"
        ]
        
        # Combine all phrase lists
        self.all_phrases = (self.ten_char_words + 
                           self.two_word_phrases + 
                           self.three_word_phrases)
        
        # Keep track of used phrases to avoid duplicates
        self.used_phrases = set()
    
    def is_valid_phrase(self, phrase: str) -> bool:
        """Check if phrase meets requirements"""
        # Must be exactly 10 characters
        if len(phrase) != 10:
            return False
        
        # No punctuation allowed (only letters, numbers, spaces)
        if not re.match(r'^[a-zA-Z0-9 ]+$', phrase):
            return False
        
        # Must not be already used
        if phrase in self.used_phrases:
            return False
            
        return True
    
    def get_next_date(self, last_date_str: str) -> str:
        """Get the next date in sequence"""
        try:
            last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
            next_date = last_date + timedelta(days=1)
            return next_date.strftime("%Y-%m-%d")
        except ValueError:
            # If parsing fails, start from a default date
            return "2025-08-01"
    
    def read_existing_phrases(self, filename: str = "words.txt") -> str:
        """Read existing phrases and return the last date"""
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
            
            if not lines:
                return "2025-07-31"  # Default start date
            
            # Extract used phrases and find last date
            last_date = "2025-07-31"
            for line in lines:
                line = line.strip()
                if ', ' in line:
                    date_part, phrase = line.split(', ', 1)
                    self.used_phrases.add(phrase)
                    last_date = date_part
            
            return last_date
        except FileNotFoundError:
            return "2025-07-31"  # Default start date
    
    def generate_phrases(self, count: int = 30) -> List[Tuple[str, str]]:
        """Generate specified number of new phrases"""
        # Read existing phrases to avoid duplicates
        last_date = self.read_existing_phrases()
        
        phrases = []
        current_date = last_date
        
        # Create a pool of available phrases
        available_phrases = [p for p in self.all_phrases if self.is_valid_phrase(p)]
        
        if len(available_phrases) < count:
            print(f"Warning: Only {len(available_phrases)} unique phrases available, requested {count}")
        
        # Shuffle for randomness
        random.shuffle(available_phrases)
        
        for i in range(min(count, len(available_phrases))):
            # Get next date
            current_date = self.get_next_date(current_date)
            phrase = available_phrases[i]
            
            # Mark as used
            self.used_phrases.add(phrase)
            
            phrases.append((current_date, phrase))
        
        return phrases
    
    def append_to_file(self, phrases: List[Tuple[str, str]], filename: str = "words.txt"):
        """Append new phrases to the file"""
        with open(filename, 'a') as f:
            for date, phrase in phrases:
                f.write(f"{date}, {phrase}\n")
    
    def generate_and_save(self, count: int = 30, filename: str = "words.txt"):
        """Generate phrases and save them to file"""
        print(f"Generating {count} new phrases...")
        
        new_phrases = self.generate_phrases(count)
        
        if not new_phrases:
            print("No new phrases could be generated!")
            return
        
        print(f"Generated {len(new_phrases)} phrases:")
        for date, phrase in new_phrases:
            print(f"{date}, {phrase}")
        
        self.append_to_file(new_phrases, filename)
        print(f"\nPhrases appended to {filename}")

def main():
    """Main function to run the phrase generator"""
    generator = PhraseGenerator()
    
    # Generate 30 phrases by default
    generator.generate_and_save(30)

if __name__ == "__main__":
    main()