// script.js

document.addEventListener("DOMContentLoaded", function() {
    const chatMessages = document.getElementById("chat-messages");
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user_input");
  
    // Auto-scroll au chargement
    if (chatMessages) {
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  
    // Auto-scroll après soumission
    if (chatForm) {
      chatForm.addEventListener("submit", function() {
        setTimeout(() => {
          if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
          }
        }, 100);
      });
    }
  
    // Envoi du message en appuyant sur "Enter"
    if (userInput) {
      userInput.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
          event.preventDefault();
          chatForm.submit();
        }
      });
    }
  });
  