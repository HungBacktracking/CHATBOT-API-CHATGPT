# Chatbot with GPT API

This is a Flask application that implements a chatbot that utilizes the GPT (Generative Pre-trained Transformer) API to provide intelligent responses to user queries. The chatbot is integrated with The Movies Database API to ensure up-to-date knowledge about movies or tv-series, and it also incorporates the DALL·E API to generate images based on user description.

## Features

- Interactive chatbot powered by the GPT API.
- Integration with a movies database API to provide information about movies.
- Image generation using the DALL·E API.
- User-friendly web interface built with Flask framework: The application is built using the Flask framework, which allows for easy deployment.

<img src="./readme/demo.png>


## Installation

### Clone the repository

```
$ git clone https://github.com/HungBacktracking/CHATBOT-API-CHATGPT.git
```

### Change into the project directory:

```
$ cd CHATBOT-API-CHATGPT
```

### Install the required dependencies using pip:

```
$ pip install -r requirements.txt
```

## Usage

Start the Flask development server:

```
$ flask run
```

In flask, default port is 5000.

Open your web browser and go to http://localhost:5000 to access the chatbot interface.

Or access the chatbot in your web browser at [hungbacktracking.pythonanywhere.com](https://hungbacktracking.pythonanywhere.com/).


Type in your queries and interact with the chatbot. It will provide intelligent responses, retrieve movie information, and generate images based on your description.

## Application Structure 
```
├── /static
│   ├── botTopic.txt
│   ├── botImage.txt
│   ├── botNormal.txt
│   ├── botGenres.txt
│   ├── botTitle.txt
│   ├── botParagraph.txt
│   ├── style.css
│   └── script.js
├── /templates
│   └── index.html
├── app.py
└── requirements.txt
```

## Acknowledgments
- This project utilizes the GPT API, which is powered by OpenAI's GPT-3.5 language model.
- The movies database API integration is based on The Movies Database API service.
- Image generation is made possible by the DALL·E API.

