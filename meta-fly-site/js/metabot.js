async function fetchData(file) {
  try {
      const response = await fetch(file);
      return await response.json();
  } catch (error) {
      console.error(`Error fetching ${file}:`, error);
      return [];
  }
}

function appendMessage(text, isUser) {
  const chatbox = document.getElementById('chatbox');
  const messageDiv = document.createElement('div');
  messageDiv.className = isUser ? 'user-message' : 'bot-message';
  messageDiv.innerText = text;
  chatbox.appendChild(messageDiv);
  chatbox.scrollTop = chatbox.scrollHeight;
}

async function sendMessage() {
  const userInputElement = document.getElementById('userInput');
  const input = userInputElement.value.trim();
  if (!input) return;
  appendMessage(input, true);
  userInputElement.value = '';
  appendMessage('Loading...', false);

  let dataset = [];
  if (/\b(seat|seats)\b/i.test(input)) {
      dataset = await fetchData('data/seats.json');
  }
else if (/\b(airline|airlines)\b/i.test(input)) {
      dataset = await fetchData('data/airlines.json');
  }
else if (/\b(plane|aircraft)\b/i.test(input)) {
      dataset = await fetchData('data/aircraft-flight.json');
  }
else if (/\b(direct|transit)\b/i.test(input)) {
      dataset = await fetchData('data/direct-transit.json');
  }
else if (/\b(minimum|maximum)\b/i.test(input)) {
      dataset = await fetchData('data/min-max.json');
  }
else if (/\b(monthly)\b/i.test(input)) {
      dataset = await fetchData('data/monthly-fare.json');
  }
else if (/\b(cheapest|cheap)\b/i.test(input)) {
      dataset = await fetchData('data/cheapest.json');
  }
else if (/\b(busiest|busy)\b/i.test(input)) {
      dataset = await fetchData('data/busiest.json');
  }
else if (/\b(duration)\b/i.test(input)) {
      dataset = await fetchData('data/dur-price.json');
  }
else if (/\b(week|month|season|days|time)\b/i.test(input)) {
      dataset = await fetchData('data/trends.json');
  }

  const responseText = await fetchFromAPI(input, dataset);
  document.querySelector('.bot-message:last-child').innerText = responseText;
}

async function fetchFromAPI(query, dataset) {
  try {
      const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
          method: "POST",
          headers: {
              "Authorization": "Bearer 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",
              "Content-Type": "application/json"
          },
          body: JSON.stringify({
              "model": "deepseek/deepseek-r1:free",
              "messages": [
                  { "role": "user", "content": `User Question: ${query} \nDataset: ${JSON.stringify(dataset)} \nSend reply under 15 words` }
              ]
          })
      });
      const data = await response.json();
      return data.choices?.[0]?.message?.content || 'No response received.';
  } catch (error) {
      return 'Error: ' + error.message;
  }
}