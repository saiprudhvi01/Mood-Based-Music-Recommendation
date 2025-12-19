from flask import Flask, render_template, request, send_from_directory
import random
import string
import os

app = Flask(__name__)

# ---------- Mood Keywords ----------
mood_keywords = {
    "Happy": [
        "happy","joy","joyful","excited","fun","smile","great","awesome","amazing","love","cheerful","fantastic",
        "glad","delighted","thrilled","ecstatic","euphoric","elated","jubilant","merry","gleeful","content",
        "pleased","satisfied","optimistic","hopeful","enthusiastic","vibrant","lively","upbeat","bright","sunny",
        "celebration","party","dancing","laugh","laughter","wonderful","excellent","brilliant","spectacular","fabulous",
        "terrific","superb","magnificent","outstanding","remarkable","incredible","blessed","fortunate","lucky",
        "cheer","rejoice","glee","delight","bliss","happiness","elation","euphoria","jubilation","exhilaration",
        "radiant","shining","sparkling","colorful","rainbow","sunshine","summer","vacation","holiday","festive",
        "playful","joking","humorous","witty","charming","sweet","cute","adorable","beautiful","gorgeous",
        "wins","victory","triumph","achievement","success","accomplishment","praise","compliment","reward","prize"
    ],
    "Sad": [
        "sad","lonely","depressed","cry","broken","pain","miss","lost","hopeless","low",
        "melancholy","sorrowful","grief","heartbroken","devastated","miserable","gloomy","blue","downcast",
        "somber","tearful","wistful","pensive","forlorn","despondent","dejected","crushed","empty","numb",
        "tragedy","suffering","agony","misery","despair","anguish","torment","torture","burden","heavy",
        "darkness","night","winter","cold","storm","rain","tears","weeping","sobbing","crying",
        "goodbye","farewell","separation","divorce","breakup","loss","death","dying","gone","disappeared",
        "failure","defeat","rejection","abandonment","betrayal","disappointment","regret","guilt","shame","embarrassment",
        "isolated","alone","solitary","abandoned","neglected","forgotten","ignored","unwanted","unloved","hated",
        "sick","ill","injured","hurt","wounded","damaged","ruined","destroyed","broken","shattered"
    ],
    "Angry": [
        "angry","mad","furious","rage","annoyed","frustrated","hate","irritated",
        "outraged","enraged","infuriated","resentful","bitter","hostile","aggressive","violent","temper",
        "wrath","disgusted","livid","irate","incensed","provoked","antagonized","exasperated","indignant",
        "furious","outraged","enraged","infuriated","resentful","bitter","hostile","aggressive","violent","temper",
        "wrath","disgusted","livid","irate","incensed","provoked","antagonized","exasperated","indignant",
        "mad","insane","crazy","wild","berserk","uncontrollable","explosive","volatile","dangerous","threatening",
        "revenge","vengeance","justice","punishment","payback","retaliation","fight","battle","war","conflict",
        "argument","dispute","quarrel","fight","clash","confrontation","opposition","resistance","defiance","rebellion",
        "destroy","damage","break","smash","crush","kill","harm","hurt","injure","attack",
        "stupid","idiot","fool","dumb","ridiculous","absurd","nonsense","garbage","trash","disgusting"
    ],
    "Calm": [
        "calm","relaxed","relax","peaceful","peace","quiet","meditation","breathe","soothing",
        "serene","tranquil","composed","collected","centered","balanced","grounded","still","restful",
        "gentle","mellow","placid","harmonious","zen","repose","comfortable","at ease","untroubled",
        "meditation","mindfulness","contemplation","reflection","introspection","silence","stillness","serenity","tranquility","peacefulness",
        "nature","forest","ocean","beach","mountain","river","lake","sky","clouds","stars",
        "soft","smooth","warm","cozy","comfortable","safe","secure","protected","sheltered","hidden",
        "slow","steady","rhythmic","flowing","drifting","floating","gliding","sailing","wandering","roaming",
        "healing","recovery","restoration","renewal","rejuvenation","refreshment","revitalization","restoration","comfort","solace"
    ],
    "Neutral": [
        "neutral","okay","fine","normal","average","regular","standard","typical","ordinary",
        "balanced","stable","steady","consistent","moderate","middle","medium","fair","acceptable",
        "satisfactory","adequate","reasonable","calm","composed","unaffected","indifferent","impartial",
        "normal","usual","common","typical","standard","regular","average","ordinary","mediocre","so-so",
        "nothing","none","neither","nor","either","maybe","perhaps","possibly","probably","sometimes",
        "routine","daily","everyday","usual","habitual","customary","traditional","conventional","standard","normal",
        "boring","dull","uninteresting","plain","simple","basic","unremarkable","average","ordinary","commonplace",
        "waiting","watching","observing","seeing","looking","noticing","aware","conscious","alert","awake",
        "working","studying","reading","writing","learning","thinking","considering","pondering","reflecting","contemplating"
    ],
    "Anxious": [
        "anxious","worried","nervous","scared","fear","panic","stressed","overthinking",
        "tense","uneasy","apprehensive","restless","agitated","troubled","disturbed","concerned","afraid",
        "frightened","intimidated","overwhelmed","vulnerable","insecure","uncertain","doubtful","hesitant",
        "panic","terror","horror","nightmare","phobia","dread","apprehension","foreboding","premonition","anxiety",
        "sweating","shaking","trembling","tremor","palpitations","heartbeat","racing","pounding","throbbing","pulsing",
        "breathing","hyperventilating","choking","suffocating","drowning","trapped","stuck","cornered","helpless","powerless",
        "danger","threat","risk","peril","hazard","menace","warning","alarm","emergency","crisis",
        "failure","mistake","error","fault","blame","responsibility","pressure","expectation","deadline","exam",
        "crowd","people","social","public","speaking","presentation","performance","evaluation","judgment","criticism"
    ],
    "Motivated": [
        "motivated","inspired","confident","focus","goal","success","determined","energetic",
        "driven","ambitious","passionate","dedicated","committed","enthusiastic","empowered","strong",
        "powerful","ready","prepared","focused","disciplined","resilient","persistent","hardworking","productive",
        "champion","winner","victor","leader","pioneer","innovator","creator","builder","achiever","accomplisher",
        "power","strength","force","energy","vitality","stamina","endurance","courage","bravery","valor",
        "action","movement","progress","advancement","improvement","growth","development","evolution","transformation","change",
        "dream","vision","ambition","aspiration","purpose","mission","calling","destiny","fate","future",
        "exercise","training","practice","preparation","planning","strategy","tactics","method","approach","technique",
        "work","business","career","profession","job","task","project","assignment","duty","responsibility"
    ]
}

# ---------- Songs and Genres ----------
music_recommendations = {
    "Happy": {
        "genres": ["Pop", "Dance", "EDM"],
        "songs": [
            "Happy - Pharrell Williams",
            "Can't Stop the Feeling - Justin Timberlake", 
            "Uptown Funk - Mark Ronson ft. Bruno Mars",
            "Shake It Off - Taylor Swift",
            "Good as Hell - Lizzo"
        ]
    },
    "Sad": {
        "genres": ["Acoustic", "Piano", "Indie"],
        "songs": [
            "Someone Like You - Adele",
            "Mad World - Gary Jules",
            "Hurt - Johnny Cash",
            "Blackbird - The Beatles",
            "The Night We Met - Lord Huron"
        ]
    },
    "Angry": {
        "genres": ["Rock", "Rap", "Metal"],
        "songs": [
            "Killing in the Name - Rage Against the Machine",
            "Lose Yourself - Eminem",
            "Break Stuff - Limp Bizkit",
            "Stronger - Kanye West",
            "Bodies - Drowning Pool"
        ]
    },
    "Calm": {
        "genres": ["Classical", "Lo-fi", "Ambient"],
        "songs": [
            "Clair de Lune - Claude Debussy",
            "Weightless - Marconi Union",
            "River Flows in You - Yiruma",
            "Study Lo-fi Hip Hop Mix",
            "Spiegel im Spiegel - Arvo Pärt"
        ]
    },
    "Neutral": {
        "genres": ["Indie", "Soft Pop", "Alternative"],
        "songs": [
            "Ho Hey - The Lumineers",
            "Banana Pancakes - Jack Johnson",
            "Better Together - Jack Johnson",
            "Little Talks - Of Monsters and Men",
            "Home - Edward Sharpe & The Magnetic Zeros"
        ]
    },
    "Anxious": {
        "genres": ["Ambient", "Instrumental", "Meditation"],
        "songs": [
            "Ambient 1 - Brian Eno",
            "Weightless - Marconi Union",
            "Om Namo Bhagavate - Krishna Das",
            "Breathing Meditation - Calm",
            "Deep Focus - Spotify Playlist"
        ]
    },
    "Motivated": {
        "genres": ["Workout", "Hip-Hop", "EDM"],
        "songs": [
            "Eye of the Tiger - Survivor",
            "Lose Yourself - Eminem",
            "Till I Collapse - Eminem",
            "Thunder - Imagine Dragons",
            "Can't Hold Us - Macklemore & Ryan Lewis"
        ]
    }
}

# ---------- Functions ----------
def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

def get_music_files(mood):
    music_dir = os.path.join(os.path.dirname(__file__), 'music', mood)
    if os.path.exists(music_dir):
        music_files = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav', '.ogg', '.m4a'))]
        return music_files
    return []

def detect_mood(text):
    text = preprocess(text)
    words = text.split()
    scores = {}
    
    # Calculate scores for each mood
    for mood, keywords in mood_keywords.items():
        score = 0
        keyword_matches = 0
        
        for keyword in keywords:
            # Check for exact word matches
            keyword_count = words.count(keyword)
            if keyword_count > 0:
                # Weight by keyword importance
                weight = 1 + (len(keyword) - 3) * 0.1 if len(keyword) > 3 else 1
                # Stronger weight for more specific emotions
                if mood in ["Happy", "Sad", "Angry"]:
                    weight *= 1.2
                elif mood in ["Anxious", "Motivated"]:
                    weight *= 1.1
                
                score += keyword_count * weight
                keyword_matches += keyword_count
                
            # Check for partial matches (for compound words)
            for word in words:
                if keyword in word and word != keyword:
                    partial_weight = 0.5
                    score += partial_weight
        
        # Bonus for multiple different keywords from same mood
        if keyword_matches >= 2:
            score *= 1.3
        elif keyword_matches >= 3:
            score *= 1.5
            
        scores[mood] = score
    
    # Find the best mood
    best_mood = max(scores, key=scores.get)
    best_score = scores[best_mood]
    
    # If no keywords found, return Neutral
    if best_score == 0:
        return "Neutral"
    
    # Calculate confidence metrics
    total_score = sum(scores.values())
    confidence_ratio = best_score / total_score if total_score > 0 else 0
    second_best = sorted(scores.values(), reverse=True)[1] if len(scores) > 1 else 0
    
    # Strong confidence conditions
    if best_score >= 3:  # Strong evidence
        return best_mood
    elif confidence_ratio >= 0.4:  # Clear majority
        return best_mood
    elif best_score - second_best >= 1.5:  # Clear winner
        return best_mood
    
    # Moderate confidence - check for mood-specific patterns
    if best_score >= 1.5:
        # Prefer more specific moods over neutral when there's some evidence
        if best_mood != "Neutral" and scores["Neutral"] < best_score * 0.8:
            return best_mood
    
    # Low confidence - return Neutral
    return "Neutral"

# ---------- Routes ----------
@app.route("/", methods=["GET", "POST"])
def index():
    mood = None
    songs = []
    music_files = []
    genres = None
    user_text = ""

    if request.method == "POST":
        user_text = request.form["text"]
        mood = detect_mood(user_text)
        
        # Get actual music files from mood folder
        music_file_list = get_music_files(mood)
        if music_file_list:
            for file in music_file_list:
                music_files.append(f"/music/{mood}/{file}")
                songs.append(file)
        else:
            # Fallback to placeholder if no music files found
            songs = music_recommendations[mood]["songs"]
            music_files = []
        
        genres = ", ".join(music_recommendations[mood]["genres"])

    return render_template(
        "index.html",
        mood=mood,
        songs=songs,
        music_files=music_files,
        genres=genres,
        user_text=user_text
    )

@app.route("/music/<mood>/<filename>")
def serve_music(mood, filename):
    music_dir = os.path.join(os.path.dirname(__file__), 'music', mood)
    return send_from_directory(music_dir, filename)

if __name__ == "__main__":
    app.run(debug=True)
