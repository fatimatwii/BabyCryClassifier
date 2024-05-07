const recordButton = document.getElementById('recordButton');
    const audioElement = document.getElementById('audioElement');

    let isRecording = false;
    let chunks = [];

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
          const blob = new Blob(chunks, { type: 'audio/webm' });
          const url = URL.createObjectURL(blob);
          audioElement.src = url;
          audioElement.style.display = 'block';
        };
      })
      .catch(error => {
        console.log('Error accessing microphone:', error);
      });
