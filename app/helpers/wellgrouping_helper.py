# Function to assign a color to each group
from randomcolor import RandomColor
from wordcloud import STOPWORDS, WordCloud

def assign_colors_to_groups(groups: list[list[str]]):
    rc = RandomColor()
    colors = rc.generate(luminosity='dark', count=len(groups))
    if "#000000" in colors:
        colors.remove("#000000") # Remove black color
        colors.append("#A9A9A9") # Add dark grey color
    return colors

def wordcloud_groupname(members: list[str]) -> str:
    custom_stopwords = set(STOPWORDS)
    #custom_stopwords.update(["STATE", "ST"])
    
    include_words = set()
    for member in members:
        include_words.update(member.split())
    
    filtered_include_words = include_words - custom_stopwords
    combined_text = ' '.join(members)
    filtered_words = ' '.join(word for word in combined_text.split() if word in filtered_include_words)
    
    result = ""
    if filtered_words.strip():
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(filtered_words)
        word_freq = wordcloud.words_
        
        for key in word_freq.keys():
            if word_freq[key] == 1.0:
                result += key + " "
                
    return result.rstrip()