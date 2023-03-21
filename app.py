from nltk.chat.util import Chat, reflections
from flask import Flask, request, render_template
import time
import numpy as np
import requests
import json
import config 

# set up API key
tmdb_api_key = config.tmdb_api_key
api_key = config.api_key

genreList = {   
    "Action": 28,
    "Adventure": 12, 
    "Animation": 16, 
    "Comedy": 35, 
    "Crime": 80, 
    "Documentary": 99, 
    "Drama": 18, 
    "Family": 10751, 
    "Fantasy": 14, 
    "History": 36, 
    "Horror": 27, 
    "Music": 10402, 
    "Mystery": 9648, 
    "Romance": 10749, 
    "Science Fiction": 878, 
    "TV Movie": 10770, 
    "Thriller": 53, 
    "War": 10752, 
    "Western": 37,
    "Action & Adventure": 10759,
    "Reality": 10764,
    "Sci-Fi & Fantasy": 10765,
    "Soap": 10766,
    "War & Politics": 10768,
}

app = Flask(__name__)
history = ""
historyCount = 0

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get", methods = ["GET"])
def generate_response_main():
    data = requests.get(f"https://hungbacktracking.github.io/facts.github.io/CHATBOT-API-CHATGPT/botNormal.txt")
    description = data.text
    user_message = request.args.get('msg')

    global history
    global historyCount
    if historyCount == 2:
        for i in range(1, len(history)):
            if history[i : i + 5] == "User:":
                history = history[i:]
                break
        historyCount -= 1

    topic = classify_botTopic(user_message)
    if topic == 'image':
        response = generate_response_botImage(user_message)
    elif topic == 'movie':
        history += "\nUser: " + user_message + "\nBrend: " 
        response = generate_response_botMovie(user_message)

        history += response
        historyCount += 1
    else:
        history += "\nUser: " + user_message + "\nBrend: " 
        prompt = description + history
        response = generate_response_botNormal(prompt)

        history += response 
        historyCount += 1
    
    return response


def generate_response(user_message, description_file=""):
    if description_file == "":
        prompt = user_message
    else:   
        data = requests.get(f"https://hungbacktracking.github.io/facts.github.io/CHATBOT-API-CHATGPT/{description_file}")
        description = data.text
        prompt = description + user_message + "\nYou: "    

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers = {"Authorization" : f"Bearer {api_key}"},
        json={
            "model": "gpt-3.5-turbo",
            "max_tokens": 350,
            "temperature": 0.4,
            "messages" : [
                {"role": "user", "content": prompt}
            ]
        },
    )

    if response.ok:
        result = response.json()["choices"][0]["message"]["content"].strip()    
        return result
    else:
        return "I'm sorry, I'm having trouble generating a response right now."


def get_movie_info(movie_title):
    url1 = f"https://api.themoviedb.org/3/search/tv?api_key={tmdb_api_key}&query={movie_title}"
    response1 = requests.get(url1)
    results1 = response1.json()["results"]

    url2 = f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_api_key}&query={movie_title}"
    response2 = requests.get(url2)
    results2 = response2.json()["results"]

    if len(results1) == 0 and len(results2) == 0:
        return response_anyway()
    elif len(results1) == 0:
        return json.dumps(results2[0]) 
    elif len(results2) == 0:
        return json.dumps(results1[0])
    
    if float(json.dumps(results1[0]["popularity"])) >= float(json.dumps(results2[0]["popularity"])):
        return json.dumps(results1[0])
    elif float(json.dumps(results1[0]["popularity"])) < float(json.dumps(results2[0]["popularity"])):
        return json.dumps(results2[0]) 
    elif similarity(json.dumps(results1[0]["name"]).lower(), str(movie_title).lower()) >= similarity(json.dumps(results2[0]["title"]).lower(), str(movie_title).lower()):
        return json.dumps(results1[0])
    else:
        return json.dumps(results2[0]) 
    

def generate_response_botImage(user_message):
    result = generate_image(user_message)
    return result


def generate_response_botMovie(user_message):
    data = requests.get(f"https://hungbacktracking.github.io/facts.github.io/CHATBOT-API-CHATGPT/botNormal.txt")
    description = data.text

    global history
    prompt = description + history

    movieTopic = classify_botMovieTopic(user_message)
    if movieTopic == 'info':
        result = generate_response_botInfo(user_message)
    elif movieTopic == 'similar':
        result = generate_response_botSimilar(user_message)
    elif movieTopic == 'genre':
        result = generate_response_botGenre(user_message)
    elif movieTopic == 'trending':
        result = generate_response_botTrending(user_message)
    else:
        result = generate_response_botNormal(prompt)
    
    return result


def generate_response_botNormal(prompt):
    return generate_response(prompt, "")


def classify_botTopic(user_message):
    return generate_response(user_message, "botTopic.txt")


def classify_botMovieTopic(user_message):
    response = generate_response(user_message, "botMovieTopic.txt")
    return response

def generate_response_botInfo(user_message):
    response = generate_response(user_message, "botTitles.txt")
    titles = response.split('; ')

    result = ""
    if len(titles) == 0:
        return response_anyway()
    else:
        for title in titles:
            info = get_movie_info(title)
            para = generate_response_botParagraph(info)
            result += para + "\n\n"    
        return result
    

def generate_response_botSimilar(user_message):
    response = generate_response(user_message, "botTitles.txt")
    titles = response.split('; ')
    title = titles[0]

    url1 = f"https://api.themoviedb.org/3/search/tv?api_key={tmdb_api_key}&query={title}"
    response1 = requests.get(url1)
    results1 = response1.json()["results"]

    url2 = f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_api_key}&query={title}"
    response2 = requests.get(url2)
    results2 = response2.json()["results"]

    if len(results1) == 0 and len(results2) == 0:
        return response_anyway()
    elif len(results1) == 0:
        try:
            movie_id = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_api_key}&query={title}").json()["results"][0]["id"]
            movies = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/similar?api_key={tmdb_api_key}").json()["results"]
        except:
            movies = []  
    elif len(results2) == 0:
        try:
            movie_id = requests.get(f"https://api.themoviedb.org/3/search/tv?api_key={tmdb_api_key}&query={title}").json()["results"][0]["id"]
            movies = requests.get(f"https://api.themoviedb.org/3/tv/{movie_id}/similar?api_key={tmdb_api_key}").json()["results"]
        except:
            movies = []  
    elif float(json.dumps(results1[0]["popularity"])) >= float(json.dumps(results2[0]["popularity"])):
        try:
            movie_id = requests.get(f"https://api.themoviedb.org/3/search/tv?api_key={tmdb_api_key}&query={title}").json()["results"][0]["id"]
            movies = requests.get(f"https://api.themoviedb.org/3/tv/{movie_id}/similar?api_key={tmdb_api_key}").json()["results"]
        except:
            movies = [] 
    elif float(json.dumps(results1[0]["popularity"])) < float(json.dumps(results2[0]["popularity"])):
        try:
            movie_id = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_api_key}&query={title}").json()["results"][0]["id"]
            movies = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/similar?api_key={tmdb_api_key}").json()["results"]
        except:
            movies = [] 
    elif similarity(json.dumps(results1[0]["name"]).lower(), title.lower()) >= similarity(json.dumps(results2[0]["title"]).lower(), title.lower()):
        try:
            movie_id = requests.get(f"https://api.themoviedb.org/3/search/tv?api_key={tmdb_api_key}&query={title}").json()["results"][0]["id"]
            movies = requests.get(f"https://api.themoviedb.org/3/tv/{movie_id}/similar?api_key={tmdb_api_key}").json()["results"]
        except:
            movies = [] 
    else: 
        try:
            movie_id = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_api_key}&query={title}").json()["results"][0]["id"]
            movies = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/similar?api_key={tmdb_api_key}").json()["results"]
        except:
            movies = []    

    result = ""
    if len(movies) == 0:
        return response_anyway()
    else:
        for i in range(min(3, len(movies))):
            para = generate_response_botParagraph(json.dumps(movies[i]))
            result += para + "\n\n"    
        return result

def response_anyway():
    data = requests.get(f"https://hungbacktracking.github.io/facts.github.io/CHATBOT-API-CHATGPT/botNormal.txt")
    description = data.text

    global history
    prompt = description + history
    return generate_response_botNormal(prompt)
    

def generate_response_botGenre(user_message):
    response = generate_response(user_message, "botGenres.txt")
    if response == 'undefined':
        return response_anyway()

    genre = response.split('; ')
    for i in range(len(genre)):
        genre[i] = genreList[genre[i]]
    
    genreTV = []
    for i in range(len(genre)):
        x = genre[i]
        if x == 28 or x == 12: x = 10759
        if x == 878 or x == 14: x = 10765
        genreTV.append(x)
    
    url1 = f"https://api.themoviedb.org/3/discover/tv?api_key={tmdb_api_key}&with_genres="
    for i in range(len(genreTV)):
        url1 += str(genreTV[i]) + ','

    url2 = f"https://api.themoviedb.org/3/discover/movie?api_key={tmdb_api_key}&with_genres="
    for i in range(len(genre)):
        url2 += str(genre[i]) + ','
    
    movies1 = requests.get(f"{url1}").json()["results"]
    movies2 = requests.get(f"{url2}").json()["results"]
    if len(movies1) and len(movies2) == 0:
        return response_anyway()

    result = ""
    if len(movies1) == 0:
        for i in range(min(3, len(movies2))):
            para = generate_response_botParagraph(json.dumps(movies2[i]))
            result += para + "\n\n"
    elif len(movies2) == 0:
        for i in range(min(3, len(movies1))):
            para = generate_response_botParagraph(json.dumps(movies1[i]))
            result += para + "\n\n"
    else:
        for i in range(min(2, len(movies1))):
            para = generate_response_botParagraph(json.dumps(movies1[i]))
            result += para + "\n\n"
        para = generate_response_botParagraph(json.dumps(movies2[0]))
        result += para + "\n"
    
    return result


def generate_response_botTrending(user_message):
    response = generate_response(user_message, "botGenres.txt")
    genre = response.split('; ')

    if genre[0] == "undefined":
        genre = []
    for i in range(len(genre)):
        genre[i] = genreList[genre[i]]
    
    genreTV = []
    for i in range(len(genre)):
        x = genre[i]
        if x == 28 or x == 12: x = 10759
        if x == 878 or x == 14: x = 10765
        genreTV.append(x)

    url = f"https://api.themoviedb.org/3/trending/all/week?api_key={tmdb_api_key}"
    movies = requests.get(f"{url}").json()["results"]

    result = ""
    movieCount = 0
    for i in range(len(movies)):
        if movieCount == 3: break

        cnt = 0
        for j in range(min(4, len(genreTV))):
            for k in range(len(movies[i]["genre_ids"])):
                if json.dumps(movies[i]["genre_ids"][k]) == str(genreTV[j]):
                    cnt += 1

        for j in range(min(2, len(genre))):
            for k in range(len(movies[i]["genre_ids"])):
                if json.dumps(movies[i]["genre_ids"][k]) == str(genre[j]):
                    cnt += 1

        if cnt == 0 and len(genre) != 0: continue
        para = generate_response_botParagraph(json.dumps(movies[i]))
        result += para + "\n\n"
        movieCount += 1
    
    if movieCount == 0:
        return response_anyway()

    return result
        

def generate_response_botParagraph(info):
    return generate_response(info, "botParagraph.txt")


def generate_image(user_message):
    prompt = user_message
    response = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers = {"Authorization" : f"Bearer {api_key}"},
        json={
            "prompt": prompt,
            "n": 1,
            "size":"256x256"
        },
    )
    return response.json()["data"][0]["url"].strip()

def similarity(s1, s2):
    """
    Calculate the similarity between two strings using the Levenshtein distance.
    Return the result as a percentage.
    """
    # initialize a matrix with zeros
    matrix = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]
    
    # populate the matrix with edit distances
    for i in range(len(s1) + 1):
        for j in range(len(s2) + 1):
            if i == 0:
                matrix[i][j] = j
            elif j == 0:
                matrix[i][j] = i
            elif s1[i-1] == s2[j-1]:
                matrix[i][j] = matrix[i-1][j-1]
            else:
                matrix[i][j] = 1 + min(matrix[i-1][j], matrix[i][j-1], matrix[i-1][j-1])
    
    # calculate the similarity as 1 - (edit distance / max length)
    max_length = max(len(s1), len(s2))
    similarity = 1 - (matrix[len(s1)][len(s2)] / max_length)
    
    # return the similarity as a percentage
    return round(similarity * 100, 2)


if __name__ == "__main__":
    app.run()