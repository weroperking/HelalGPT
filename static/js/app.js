// DOM Elements
const chatContainer = document.getElementById('chat-container');
const askButton = document.getElementById('ask-button');
const questionInput = document.getElementById('question');

// Function to send a question to the Flask backend
async function fetchData(question) {
  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ question })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.response || 'Request failed');
    }

    const data = await response.json();
    return data.response;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error; // Throw error to handle in caller
  }
}

function typeText(element, text, callback) {
  let index = 0;
  const interval = setInterval(() => {
    if (index < text.length) {
      element.innerHTML += text.charAt(index);
      index++;
    } else {
      clearInterval(interval);
      if (callback) callback();
    }
  }, 10); // Adjust typing speed here
}

// Function to create a chat message
function createChatMessage(message, isUser, isLoading = false) {
  const messageElement = document.createElement('div');
  messageElement.className = `flex items-start space-x-2 w-full max-w-md ${isUser ? 'justify-end' : 'justify-start'}`;

  if (isUser) {
    messageElement.innerHTML = `
      <div class="gradient-bg text-white p-4 rounded-lg shadow-md">
        <p class="font-semibold">${message}</p>
      </div>
      <img alt="User avatar" class="w-8 h-8 rounded-full" height="40" src="./static/imgs/User.jpg" width="40"/>
    `;
  } else {
    messageElement.innerHTML = `
      <div class="flex items-start space-x-2 w-full">
        <img alt="HelalGPT logo" class="w-8 h-8 rounded-full" src="./static/imgs/logo.jpg"/>
        <div class="bg-white text-black p-4 rounded-lg shadow-md w-full relative newstyle">
          <p>${isLoading ? '<i class="fas fa-spinner animate-spin"></i> Typing...' : message}</p>
          <!-- Buttons at the lower left -->
          <div class="flex space-x-2 mt-2">
            <button class="copy-button bg-gray-200 text-black px-2 py-1 rounded-full flex items-center shadow-md hover:bg-gray-300 transition text-sm">
              <i class="fas fa-copy mr-1"></i> 
            </button>
          </div>
        </div>
      </div>
    `;
  }

  chatContainer.appendChild(messageElement);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  return messageElement;
}

// Event Listener for the "Send" button
askButton.addEventListener('click', async () => {
  const question = questionInput.value.trim();
  if (!question) return;

  try {
    // Show loading state
    askButton.innerHTML = '<i class="fas fa-spinner animate-spin"></i>';
    askButton.disabled = true;

    // Add user's message to the chat
    createChatMessage(question, true);
    questionInput.value = '';

    // Add loading indicator for bot response
    const loadingMessageElement = createChatMessage('', false, true);

    // Fetch and display response
    const response = await fetchData(question);
    const responseElement = loadingMessageElement.querySelector('p');
    responseElement.innerHTML = ''; // Clear loading indicator
    typeText(responseElement, response);
  } catch (error) {
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: error.message || 'Failed to get response',
      confirmButtonColor: '#7c3aed',
    });
  } finally {
    // Reset button state
    askButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
    askButton.disabled = false;
  }
});

// Event Listener for the Enter key
questionInput.addEventListener('keypress', (event) => {
  if (event.key === 'Enter') {
    askButton.click();
  }
});

// Event Delegation for buttons
chatContainer.addEventListener('click', async (event) => {
  const target = event.target;
  const copyButton = target.closest('.copy-button');

  // Copy Button
  if (copyButton) {
    try {
      const message = copyButton.closest('.bg-white').querySelector('p').textContent;
      await navigator.clipboard.writeText(message);
      Swal.fire({
        icon: 'success',
        title: 'Copied!',
        toast: true,
        position: 'bottom-end',
        showConfirmButton: false,
        timer: 2000,
        timerProgressBar: true,
      });
    } catch (error) {
      Swal.fire({
        icon: 'error',
        title: 'Copy Failed',
        text: 'Failed to copy text to clipboard',
        confirmButtonColor: '#7c3aed',
      });
    }
  }
});


document.addEventListener("DOMContentLoaded", function() {
    Swal.fire({
        title: "تنبيه",
        text: "يرجى إدخال رسالة مباشرة تحتوي على جميع التفاصيل، لا يمتلك النموذج ذاكرة طويلة المدى.",
        icon: "warning",
        confirmButtonText: "حسنًا"
    });
});
