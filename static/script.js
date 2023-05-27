var response = "";

document.addEventListener("DOMContentLoaded", () => {
	setTimeout(function() {
		window.scrollTo(0,0);
	}, 500);

	const inputField = document.getElementById("input");
	inputField.addEventListener("keydown", (e) => {

	if (e.shiftKey && e.keyCode === "Enter") {
		// Add newline character to input value
		inputField.value += "\n";
		e.preventDefault();
	}
	});

	inputField.addEventListener("keydown", (e) => {

		if (e.code === "Enter" && e.shiftKey === false) {
			let input = inputField.value;
			inputField.value = "";

			const messagesContainer = document.getElementById("messages");
			let imgUser = document.createElement("div");
			let userDiv = document.createElement("div");
			const user = document.createElement("div");

			user.id = 'user';
			imgUser.innerHTML = `<img src="https://sylviapap.github.io/chatbot/user.png" class="avatar">`;
			userDiv.className = "user-response";
			userDiv.innerHTML = input;

			user.appendChild(userDiv);
			user.appendChild(imgUser);
			messagesContainer.appendChild(user);


			let botImg = document.createElement("div");
			let botDiv = document.createElement("div");
			let botText = document.createElement("div");
			let botPhoto = document.createElement("div");

			botDiv.id = "bot";
			botImg.innerHTML = '<img src="https://sylviapap.github.io/chatbot/bot-mini.png" class = "avatar">';
			//botPhoto.className = "photo";
			botText.className = "bot-response";
			botText.innerHTML = `<span>Typing...</span>`;

			botDiv.appendChild(botImg);
			botDiv.appendChild(botPhoto);
			botDiv.appendChild(botText);
			messagesContainer.appendChild(botDiv);

			// Keep messages at most recent
			messagesContainer.scrollTop = messagesContainer.scrollHeight - messagesContainer.clientHeight;

			var xhr = new XMLHttpRequest();
			xhr.open("GET", "/get?msg=" + input, true);
			xhr.onreadystatechange = function (){
				botPhoto.innerHTML = '';

				if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200)
				{
					response = xhr.responseText;
					if (response[0] === 'h' && response[1] === 't' && response[2] === 't' && response[3] === 'p') {
						botPhoto.className = "photo";
						botPhoto.innerHTML = '<img src="' + response + '" class="photo">';
						botText.remove();
						setTimeout(function() {
							messagesContainer.scrollTop = messagesContainer.scrollHeight - messagesContainer.clientHeight;
						}, 2000);
						messagesContainer.scrollTop = messagesContainer.scrollHeight - messagesContainer.clientHeight;
					}
					else botText.innerHTML = `<span>${response}</span>`;
					messagesContainer.scrollTop = messagesContainer.scrollHeight - messagesContainer.clientHeight;
				}

			};
			xhr.send();

		}
	});
});

// Text to Speech

const synth = window.speechSynthesis;

function detect(text) {
	let words = text.split(' ');
	let vietnameseCount = 0;
	let englishCount = 0;

	// Kiểm tra các từ và cụm từ để phân biệt tiếng Anh và tiếng Việt
	words.forEach(word => {
		// Kiểm tra tiếng Việt
		if (/^[a-zA-Z]*$/.test(word) === false && /[^\u0000-\u007F]+/.test(word) === true) {
			vietnameseCount++;
		}
		else {
			englishCount++;
		}
	});
	if (words.length <= 4 && vietnameseCount >= 1) return false;
	if (vietnameseCount >= 2) return false;
	return true;
}

const playButton = document.getElementById("playButton");

playButton.addEventListener("click", () => {
	var micIcon = document.querySelector('#playButton');
	let voice = new SpeechSynthesisUtterance(response);
	voice.text = response;

	if (detect(response)) voice.lang = "en-GB";
	else voice.lang = "vi-VN";

	voice.volume = 1;
	voice.rate = 1;
	voice.pitch = 1; // Can be 0, 1, or 2

	if (micIcon.classList.contains('active')){
		synth.cancel();
		playButton.classList.remove('active');
		inputField.focus();
	}
	else synth.speak(voice);

	// Toggle the 'active' class when audio starts playing
	voice.addEventListener('start', () => {
		playButton.classList.add('active');
	});

	// Toggle the 'active' class when audio ends playing
	voice.addEventListener('end', () => {
		inputField.focus();
		playButton.classList.remove('active');
	});

});

//Speech to text

window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();
recognition.interimResults = true;

const inputField = document.getElementById('input');
const button = document.getElementById('button');
var div = document.getElementById('content');

button.addEventListener('click', () => {
	var micIcon = document.querySelector('#button');

	if (micIcon.classList.contains('recording')) {
		recognition.stop();
	}
	else recognition.start();

	recognition.onstart = function() {
		micIcon.classList.add('recording');
	}

	recognition.onend = function() {
		inputField.focus();
		micIcon.classList.remove('recording');
	}

});

recognition.addEventListener('result', event => {
	const text = Array.from(event.results).map((result) => result[0]).map((result) => result.transcript).join("");
	inputField.value = text;
});


// The Copied Button

coppyButton = document.getElementById('copyButton');
coppyButton.addEventListener('click', () => {
	// response.select();
	// document.execCommand("copy");
	inputField.focus();
	navigator.clipboard.writeText(response);

	var notification = document.getElementById("copy-notification");
	notification.innerHTML = "Copied to clipboard";
	notification.classList.add("show");

	setTimeout(function() {
		notification.classList.remove("show");
	}, 2000);

});


// Get a reference to the "Popular" link
const popularLink = document.querySelector('a[href="#popular"]');

// Add a click event listener to the "Popular" link
popularLink.addEventListener('click', () => {
	// Get a reference to the "top" section
	const topSection = document.querySelector('.top');

	// Scroll the page to the "top" section
	topSection.scrollIntoView({ behavior: 'smooth' });
});

// Get a reference to the "Chatbot" link
const chatbotLink = document.querySelector('a[href="#chatbot"]');

// Add a click event listener to the "Chatbot" link
chatbotLink.addEventListener('click', () => {
	// Get a reference to the "bottom" section
	const bottomSection = document.querySelector('.bottom');

	// Scroll the page to the "bottom" section
	inputField.focus();
	bottomSection.scrollIntoView({ behavior: 'smooth' });
});
