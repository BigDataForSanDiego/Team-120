<template>
  <div class="container">
    <div class="card">
      <h2 class="question">Hello, {{ userName }}</h2>

      <p v-if="!userName">Fetching your health profile...</p>

		<!-- Display the current question -->
      <h2 v-if="currentQuestion">{{ currentQuestion }}</h2>
      <p v-else>No questions available</p>

      <button class="record-btn" @click="toggleRecording">
        {{ isRecording ? "Stop Recording" : "Start Recording" }}
      </button>

      <div v-if="transcript" class="transcript-box">
        <strong>Transcript:</strong>
        <textarea v-model="transcript" class="transcript-textbox"></textarea>
      </div>

      <div class="button-group">
        <button class="prev-btn" @click="prevQuestion" :disabled="currentQuestionIndex === 0">Previous Question</button>
        <button class="next-btn" @click="nextQuestion" :disabled="currentQuestionIndex >= questions.length - 1">Next Question</button>
      </div>

      <div v-if="profileMessage" class="profile-message">{{ profileMessage }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import RecordRTC from 'recordrtc';

// State
const questions = ref([]); // Dynamic questions based on missing questions from API
const currentQuestionIndex = ref(0);
const currentQuestion = ref("");
const recorder = ref(null);
const transcript = ref("");
const isRecording = ref(false); // To track whether it's recording or not
const profileMessage = ref(""); // To display messages related to health profile
const userName = ref(""); // To store the user's name

// Methods to fetch the health profile and missing questions
const fetchHealthProfile = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/get_profile');
	console.log(response);
    if (response.data.profile_data && response.data.profile_data.name) {
      userName.value = response.data.profile_data.name; // Set the user's name
      profileMessage.value = `Welcome, ${userName.value}!`;
    } else {
      profileMessage.value = "Error: Profile data does not contain a name.";
    }
  } catch (error) {
    profileMessage.value = "Error fetching health profile.";
    console.error("Error fetching health profile:", error);
  }
};

const fetchMissingQuestions = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/missing_questions');
    questions.value = response.data.missing_questions;
    currentQuestion.value = questions.value[currentQuestionIndex.value];
  } catch (error) {
    console.error("Error fetching missing questions:", error);
  }
};

// Methods for recording audio and sending it for transcription
const prevQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--;
    currentQuestion.value = questions.value[currentQuestionIndex.value];
    transcript.value = ""; // Clear transcript when navigating to another question
  }
};

const nextQuestion = () => {
  if (currentQuestionIndex.value < questions.value.length - 1) {
    currentQuestionIndex.value++;
    currentQuestion.value = questions.value[currentQuestionIndex.value];
    transcript.value = ""; // Clear transcript when navigating to another question
  }
};

const startRecording = () => {
  navigator.mediaDevices.getUserMedia({ audio: true })
    .then((stream) => {
      recorder.value = new RecordRTC(stream, { type: 'audio' });
      recorder.value.startRecording();
      isRecording.value = true; // Update state to recording
    })
    .catch((err) => {
      console.error("Microphone access denied:", err);
    });
};

const stopRecording = () => {
  recorder.value.stopRecording(() => {
    const audioBlob = recorder.value.getBlob();
    // Send the audio blob to the API for transcription
    sendAudioForTranscription(audioBlob);
    isRecording.value = false; // Update state to stopped
  });
};

const toggleRecording = () => {
  if (isRecording.value) {
    stopRecording();
  } else {
    startRecording();
  }
};

const sendAudioForTranscription = async (audioBlob) => {
  const formData = new FormData();
  formData.append('file', audioBlob, 'audio.wav'); // Append the Blob as a file

  try {
    // Replace 'YOUR_WHISPER_API_ENDPOINT' with your actual API endpoint
    const response = await axios.post('YOUR_WHISPER_API_ENDPOINT', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    transcript.value = response.data.transcription; // Update transcript with the API's response
  } catch (error) {
    console.error("Error transcribing audio:", error);
  }
};

// Lifecycle - fetch health profile when the component mounts
onMounted(() => {
  fetchHealthProfile(); // Fetch the health profile when the app starts
  fetchMissingQuestions();
});
</script>

<style scoped>
/* Global Container */
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f4f4f9;
  margin: 0;
  padding: 0;
}

/* Card Styling */
.card {
  background: #fff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  text-align: center;
  transition: box-shadow 0.3s ease;
}

.card:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

/* Question Text Styling */
.question {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 20px;
  font-weight: 600;
}

/* Record Button Styling */
.record-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 12px 20px;
  font-size: 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
  margin-bottom: 20px;
}

.record-btn:hover {
  background-color: #0056b3;
  transform: translateY(-2px);
}

.record-btn:active {
  transform: translateY(0);
}

/* Transcript Box Styling */
.transcript-box {
  margin-top: 20px;
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  text-align: left;
  font-size: 1.1rem;
  color: #555;
}

.transcript-box strong {
  font-weight: 600;
  color: #000;
}

.transcript-textbox {
  width: 100%;
  height: 100px;
  margin-top: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
  resize: none;
}

/* Button Group Styling */
.button-group {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
}

/* Previous and Next Button Styling */
.prev-btn,
.next-btn {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 12px 20px;
  font-size: 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.prev-btn:disabled,
.next-btn:disabled {
  background-color: #c8c9cc;
  cursor: not-allowed;
}

.prev-btn:hover:not(:disabled),
.next-btn:hover:not(:disabled) {
  background-color: #5a6268;
}

/* Profile Message */
.profile-message {
  margin-top: 20px;
  font-size: 1.1rem;
  color: green;
}

h2 {
	color: #000;
}
</style>
