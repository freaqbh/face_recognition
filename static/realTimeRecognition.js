const video = document.getElementById('video');
const result = document.getElementById('result');
const uploadRef = document.getElementById('uploadRef');
const preview = document.getElementById('preview');
let ws;

// Access webcam
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
  })
  .catch(err => console.error("Webcam error:", err));

// Start streaming when button clicked
document.getElementById('start').onclick = () => {
  ws = new WebSocket('ws://localhost:8080/ws');

  ws.onopen = () => {
    console.log('WebSocket connected');
    startSendingFrames();
  };

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    result.textContent = data.verified ? `Match ✅ (distance: ${data.distance.toFixed(2)})` : `Not match ❌ (distance: ${data.distance.toFixed(2)})`;
  };

  ws.onerror = (err) => console.error('WebSocket error:', err);
  ws.onclose = () => console.log('WebSocket closed');
};

function startSendingFrames() {
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');

  setInterval(() => {
    if (video.readyState === video.HAVE_ENOUGH_DATA) {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      ctx.drawImage(video, 0, 0);
      const dataUrl = canvas.toDataURL('image/jpeg');
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(dataUrl);
      }
    }
  }, 1500); // Send a frame every 1.5 seconds
}

// Stop streaming when button clicked
document.getElementById('stop').onclick = () => {
  if (ws) {
    ws.close();
    console.log('WebSocket closed');
  }
};

uploadRef.addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        preview.src = e.target.result; // Set the image source to the file's data URL
        preview.style.display = "block"; // Make the image visible
      };
      reader.readAsDataURL(file); // Read the file as a data URL
    }
});

uploadRef.onchange = async function(event) {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append("file", file);
  
    await fetch("/upload", {
      method: "POST",
      body: formData,
    });
  };

  function triggerMatch() {
    ws.send("match");
  }