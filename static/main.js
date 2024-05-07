const recordButton = document.getElementById('recordButton');
const audioElement = document.getElementById('audioElement');
const canvas = document.getElementById('waveform');
const canvasCtx = canvas.getContext('2d');
let isRecording = false;
let mediaRecorder;
let audioChunks = [];
let audioContext;
let sourceNode;
let analyser;
let dataArray;

recordButton.addEventListener('click', () => {
  if (!isRecording) {
    startRecording();
  } else {
    stopRecording();
  }
});

function startRecording() {
  isRecording = true;
  recordButton.classList.add('active');

  navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
      mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.addEventListener('dataavailable', event => {
        audioChunks.push(event.data);
      });

      mediaRecorder.addEventListener('stop', () => {
        isRecording = false;
        recordButton.classList.remove('active');

        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        const audioUrl = URL.createObjectURL(audioBlob);
        audioElement.src = audioUrl;
        audioElement.controls = true;
        audioElement.style.display = 'block';

        // Clear audio chunks for next recording
        audioChunks = [];
      });

      mediaRecorder.start();

      // Visualize waveform
      visualizeWaveform(stream);
    })
    .catch(error => {
      console.log('Error accessing microphone:', error);
    });
}

function stopRecording() {
  mediaRecorder.stop();
}

function visualizeWaveform(stream) {
  audioContext = new AudioContext();
  analyser = audioContext.createAnalyser();
  sourceNode = audioContext.createMediaStreamSource(stream);
  sourceNode.connect(analyser);
  analyser.fftSize = 2048;
  const bufferLength = analyser.frequencyBinCount;
  dataArray = new Uint8Array(bufferLength);

  drawWaveform();
}

function drawWaveform() {
  if (!isRecording) return;

  canvasCtx.clearRect(0, 0, canvas.width, canvas.height);

  const drawVisual = requestAnimationFrame(drawWaveform);

  analyser.getByteTimeDomainData(dataArray);

  canvasCtx.fillStyle = 'rgb(200, 200, 200)';
  canvasCtx.fillRect(0, 0, canvas.width, canvas.height);

  canvasCtx.lineWidth = 2;
  canvasCtx.strokeStyle = 'rgb(0, 0, 0)';

  canvasCtx.beginPath();

  const sliceWidth = canvas.width / dataArray.length;
  let x = 0;

  for (let i = 0; i < dataArray.length; i++) {
    const v = dataArray[i] / 128.0;
    const y = v * canvas.height / 2;

    if (i === 0) {
      canvasCtx.moveTo(x, y);
    } else {
      canvasCtx.lineTo(x, y);
    }

    x += sliceWidth;
  }

  canvasCtx.lineTo(canvas.width, canvas.height / 2);
  canvasCtx.stroke();
}
