const recordButton = document.getElementById('recordButton');
const audioElement = document.getElementById('audioElement');
const uploadInput = document.getElementById('uploadInput');

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
      formData.append('recorded_audio', blob, filename);
      recordCount++; 
    };
  })
  .catch(error => {
    console.log('Error accessing microphone:', error);
  });

uploadInput.addEventListener('change', () => {
  const file = uploadInput.files[0];
  formData.append('uploaded_audio', file);
});

const uploadButton = document.getElementById('uploadButton');
uploadButton.addEventListener('click', () => {
  fetch('/upload', {
    method: 'POST',
    body: formData
  })
  .then(response => {
    if (response.ok) {
      console.log('Audio uploaded successfully!');
      audioElement.style.display = 'none';
    } else {
      console.error('Error uploading audio');
    }
  })
  .catch(error => {
    console.error('Error uploading audio:', error);
  });
});
