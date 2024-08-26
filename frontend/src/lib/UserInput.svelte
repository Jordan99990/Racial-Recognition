<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import { onMount } from 'svelte';
    import { image } from '../utils/imgStore';
    import { predictionStore, selectedModel } from '../utils/predictionStore';
    const dispatch = createEventDispatcher();

    function capturePhoto() {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                const video = document.createElement('video');
                video.srcObject = stream;
                video.play();
                document.body.appendChild(video);

                const canvas = document.createElement('canvas');
                const context = canvas.getContext('2d')!;

                video.addEventListener('loadeddata', () => {
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                    context.drawImage(video, 0, 0);
                    const dataUrl = canvas.toDataURL('image/png');

                    image.set(dataUrl);

                    const photoGallery = document.getElementById('photoGallery')!;
                    const existingImg = photoGallery.querySelector('img');
                    
                    if (existingImg) {
                        photoGallery.removeChild(existingImg);
                    }
                    
                    const img = document.createElement('img');
                    img.src = dataUrl;
                    img.classList.add('photo-preview');
                    img.style.borderRadius = '8px';
                    img.style.width = `${canvas.width}px`; 
                    img.style.height = `${canvas.height}px`; 
                    photoGallery.appendChild(img);

                    dispatch('buttonPress');

                    stream.getTracks().forEach(track => track.stop());
                    document.body.removeChild(video);

                    submitPrediction();
                });
            })
            .catch(error => {
                console.error('Error accessing the camera:', error);
            });
    }

    function handleFileSelect(event: Event) {
        const input = event.target as HTMLInputElement;
        if (input.files && input.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const dataUrl = e.target!.result as string;
                image.set(dataUrl);

                const photoGallery = document.getElementById('photoGallery')!;
                const existingImg = photoGallery.querySelector('img');
                
                

                if (existingImg) {
                    photoGallery.removeChild(existingImg);
                }
                
                const img = document.createElement('img');
                img.src = e.target!.result as string;
                img.classList.add('photo-preview');
                img.style.borderRadius = '8px';
                img.style.width = '100%';
                img.style.height = 'auto';

                img.onload = () => {
                    const canvasWidth = document.querySelector('video')?.videoWidth || 640; 
                    const canvasHeight = document.querySelector('video')?.videoHeight || 480; 

                    img.style.width = `${canvasWidth}px`;
                    img.style.height = `${canvasHeight}px`;
                };

                photoGallery.appendChild(img);

                submitPrediction();
            };
            reader.readAsDataURL(input.files[0]);
        }

        dispatch('buttonPress');
    }


    function handleSubmit() {
        const input = document.querySelector('input[type="file"]') as HTMLInputElement;
        input.click();
    }

    onMount(() => {
        image.subscribe(dataUrl => {
            if (dataUrl) {
                const photoGallery = document.getElementById('photoGallery')!;
                const existingImg = photoGallery.querySelector('img');
                
                if (existingImg) {
                    photoGallery.removeChild(existingImg);
                }
                
                const img = document.createElement('img');
                img.src = dataUrl;
                img.classList.add('photo-preview');
                img.style.width = '100%';
                img.style.height = 'auto';

                img.onload = () => {
                    const canvasWidth = document.querySelector('video')?.videoWidth || 640; 
                    const canvasHeight = document.querySelector('video')?.videoHeight || 480; 

                    img.style.width = `${canvasWidth}px`;
                    img.style.height = `${canvasHeight}px`;
                };

                photoGallery.appendChild(img);
            }
        });

        predictionStore.subscribe(prediction => {
            if (prediction) {
                console.log('3333333:', prediction);
            }
        });
    });

    async function submitPrediction() {
        const dataUrl = $image;
        if (!dataUrl) {
            console.error('No image available for prediction');
            return;
        }

        const response = await fetch(dataUrl);
        const blob = await response.blob();

        const formData = new FormData();
        formData.append('file', blob, 'image.png');


        let model: string = '';
        selectedModel.subscribe(value => model = value)();
        formData.append('model', model);

        const result = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        const prediction = await result.json();

        console.log('Prediction:', prediction);
        predictionStore.set(prediction);
        dispatch('predictionMade', { prediction });
    }
</script>

<div class="photo-gallery" id="photoGallery"></div>

<div class="user-input">
    <div class="area">
        <button class="button" on:click={capturePhoto}>Capture Photo</button>
    </div>

    <div class="divider">OR</div>

    <button type="button" class="button" on:click={handleSubmit}>
        Select Photo
        <input type="file" accept="image/*" on:change={handleFileSelect} hidden>
    </button>

</div>

<style>
    .photo-gallery {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin: 2rem 0;
        width: 100%;
        justify-content: center;
        border-radius: 8px;
    }

    .user-input {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 2rem;
        width: 100%;
        max-width: 600px;
        margin-left: 1.1rem;
    }

    .divider {
        margin: 1rem 0;
        font-size: 1.2rem;
        font-weight: bold;
    }

    input[type="file"] {
        margin-top: 1rem;
    }

</style>