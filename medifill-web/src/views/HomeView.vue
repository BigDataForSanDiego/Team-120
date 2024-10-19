<template>
  <div class="container">
    <div class="card">
      <h2>Do you want to fill out the "Patient Questionnaire" form?</h2>
      <h4>NOTE: Some questions have already been answered for your given details from your health profile</h4>

      <div class="button-group">
        <button class="confirm-btn" @click="confirmStart">Yes, Start the Questionnaire</button>
        <button class="cancel-btn" @click="cancelStart">No, Cancel</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

// Method to handle confirmation and start the questionnaire
const confirmStart = () => {
  // Redirect to the page that prompts for voice input
  router.push("/questions");
};

// Method to handle cancellation
const cancelStart = () => {
  alert("You have canceled the process.");
  // Optionally, you can redirect to another page or home page
};
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

/* Button Group Styling */
.button-group {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
}

/* Confirm Button Styling */
.confirm-btn {
  background-color: #28a745;
  color: white;
  padding: 12px 20px;
  font-size: 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.confirm-btn:hover {
  background-color: #218838;
}

/* Cancel Button Styling */
.cancel-btn {
  background-color: #dc3545;
  color: white;
  padding: 12px 20px;
  font-size: 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.cancel-btn:hover {
  background-color: #c82333;
}

h2, h4 {
	color: black;
}
</style>
