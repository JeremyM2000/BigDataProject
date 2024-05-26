document.addEventListener('DOMContentLoaded', function() {
    const audioPlayer = document.getElementById('audioPlayer');
    const predElement = document.getElementById('pred');
    const radio1 = document.getElementById('radio1');
    const radio2 = document.getElementById('radio2');
    const radio3 = document.getElementById('radio3');
    const radio4 = document.getElementById('radio4');
    const form = document.getElementById('formQuizz');
    const countdownElement = document.getElementById('countdown');


    let mediaRecorder;
    let audioChunks = [];
    let audioContext = new AudioContext();

    async function startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const source = audioContext.createMediaStreamSource(stream);
            const destination = audioContext.createMediaStreamDestination();
            source.connect(destination);

            mediaRecorder = new MediaRecorder(destination.stream);
            mediaRecorder.start();

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                audioPlayer.src = URL.createObjectURL(audioBlob);
                audioChunks = [];

                const formData = new FormData();
                formData.append('audioFile', audioBlob, 'input_sample.webm');
                try {
                    const response = await fetch('/upload-audio', {
                        method: 'POST',
                        body: formData
                    });
                    const data = await response.json();
                    // predElement.innerText = `Réponse donnée: ${data.prediction}`;
                    radio1.checked = (data.prediction === 1);
                    radio2.checked = (data.prediction === 2);
                    radio3.checked = (data.prediction === 3);
                    radio4.checked = (data.prediction === 4);
                    setTimeout(() => {
                        form.submit();
                    },2000)
                    } catch (error) {
                    console.error('Error:', error);
                    // predElement.innerText = 'Error in audio processing';
                }
            };

        let secondsRemaining = 5;
        countdownElement.style.fontSize = '4rem';
        countdownElement.style.textAlign = 'center';
        countdownElement.innerText = `${secondsRemaining} `;


        const countdownTimer = setInterval(() => {
            secondsRemaining--;
            countdownElement.innerText = `${secondsRemaining}`;
            updateCountdownStyle(secondsRemaining);
            if (secondsRemaining <= 0) {
                clearInterval(countdownTimer);
                if (mediaRecorder && mediaRecorder.state === 'recording') {
                    mediaRecorder.stop();
                }
            }
        }, 1000);
        } catch (error) {
            console.error('Pas accès au micro', error);
        }
    }


    function updateCountdownStyle(seconds) {
        countdownElement.innerText = `${seconds}`;
        countdownElement.style.color = `rgb(${255 - (seconds * 28)}, 0, ${seconds * 28})`;
    }

    // Laisser le temps de lire 
    const delayToRead = 4000;
    setTimeout(() => {
        startRecording();
    }, delayToRead);
    
    
});
