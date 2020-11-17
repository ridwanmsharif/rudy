import re

def prune_tweets():

    topics = {
        "Democrat": [
            "democra",
            "joe",
            "biden",
            "kamala",
            "harris",
            "obama",
            "bernie",
            "sanders",
        ],
        "Republic": [
            "republic",
            "gop",
            "donald",
            "trump",
            "mike",
            "pence",
            "bush",
            "mitch",
            "mcconnell"
        ],
        "Election Fraud": [
            "rigged",
            "fraud",
            "census",
            "mail",
            "ballot",
            "state",
            "glitch",
            "mech",
            "count",
        ],
        "SCOTUS": [
            "constit",
            "supreme",
            "court",
            "amy",
            "coney",
            "barrett",
            "scotus",
            "nomin",
        ],
        "Climate": [
            "climate",
            "change",
            "energy",
            "green",
            "air",
            "water",
            "fire",
            "earth",
            "pollution",
            "life",
            "flood",
            "hurricane",
            "preserve",
            "hydro",
            "protect",
            "env",
        ],
        "Economic": [
            "bank",
            "econ",
            "employ",
            "america",
            "trade",
            "small",
            "business",
            "biz",
            "retire",
            "scholarship",
            "$",
            "million",
            "dollar",
            "consume",
            "independen",
            "recover",
            "growth",
            "stimulus",
            "salt",
            "resource",
            "innovat",
            "rural",
            "infra",
            "transport",
            "social",
            "security",
            "fund",
            "policy",
            "policies",
            "chinese",
        ],
        "Foreign Military": [
            "iran",
            "turkey",
            "russia",
            "isis",
            "hezbollah",
            "aggression",
            "china",
            "crisis",
            "nuclear",
            "militant",
            "lebanon",
            "palestine",
            "middle east"
        ],
        "Local Military": [
            "military",
            "veteran",
            "army",
            "soldier",
            "navy",
            "air",
            "force",
            "american",
            "border",                                    
            "defense",                        
            "ww2",
            "wwII",
            "ww II",
            "world war",            
            "treaty",                            
            "duty",
            "serve",
            "ptsd",
            "israel",
            "nato",
            "nation",
            "secur",
            "protect",
            "fbi",
            "intelligence",
            "sensitive",
        ],
        "COVID": [
            "covid",
            "corona",
            "virus",
            "social",
            "distanc",
            "pandemic",
            "test",
            "hospital",
            "quarantine",
            "vaccine",
            "mask",
        ]
    }

    with open("../resources/tweets.csv", encoding="utf8") as r:
        with open("../resources/pruned_tweets.csv", "w") as w:
            identifier = 0
            for index, line in enumerate(r):
                line = line.strip()
                if re.match(r"^.*,(democrat|republican),[0-9]+$", line):
                    w.write(line)
                    w.write("\n")
                    identifier = index
                    print(line)
                    continue
                elif re.match(r"^[0-9]+$", line):
                    continue
                elif not line:
                    continue
                else:
                    tweet_classified = [str(identifier), line]
                    for topic in topics:
                        for word in topics[topic]:
                            if word in line.lower():
                                tweet_classified.append(topic)
                                break
                    if len(tweet_classified) != 2:                    
                        w.write(','.join(tweet_classified))
                        w.write("\n")


if __name__ == "__main__":
    prune_tweets()
