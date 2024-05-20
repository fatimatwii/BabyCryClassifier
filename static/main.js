const recordButton = document.getElementById('recordButton');
const audioElement = document.getElementById('audioElement');
const uploadInput = document.getElementById('uploadInput');
const uploadButton = document.getElementById('uploadButton');
const predictionElement = document.getElementById('prediction');  // Element to display the prediction

let isRecording = false;
let chunks = [];
let formData = new FormData();
let recordCount = 1; 

navigator.mediaDevices.getUserMedia({ audio: true })
  .then(stream => {
    const mediaRecorder = new MediaRecorder(stream);

    recordButton.addEventListener('click', () => {
      if (!isRecording) {
        chunks = [];
        mediaRecorder.start();
        isRecording = true;
        recordButton.classList.add('active');
      } else {
        mediaRecorder.stop();
        isRecording = false;
        recordButton.classList.remove('active');
      }
    });

    mediaRecorder.ondataavailable = event => {
      chunks.push(event.data);
    };

    mediaRecorder.onstop = () => {
      const blob = new Blob(chunks, { type: 'audio/wav' });
      const url = URL.createObjectURL(blob);
      audioElement.src = url;
      audioElement.style.display = 'block';
      
      const filename = `record${recordCount}.wav`; 
      formData.append('audio_file', blob, filename);
      recordCount++; 

      // Automatically upload the recorded audio after stopping
      uploadAudio();
    };
  })
  .catch(error => {
    console.log('Error accessing microphone:', error);
  });

uploadInput.addEventListener('change', () => {
  const file = uploadInput.files[0];
  formData.append('uploaded_audio', file);
});

uploadButton.addEventListener('click', () => {
  uploadAudio();
});

function uploadAudio() {
  fetch('/upload', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      console.log('Audio uploaded successfully!');
      predictionElement.innerText = data.prediction;  // Display the prediction
      predictionElement.style.display = 'block';
      audioElement.style.display = 'none';
      formData = new FormData(); 
    } else {
      console.error('Error uploading audio');
    }
  })
  .catch(error => {
    console.error('Error uploading audio:', error);
  });
}
