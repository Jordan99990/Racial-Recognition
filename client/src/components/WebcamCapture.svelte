<script>
	import { onMount } from 'svelte';

	let videoElement;

	function startWebcam() {
		navigator.mediaDevices.getUserMedia({ video: true })
			.then(stream => {
				videoElement.srcObject = stream;
			})
			.catch(error => {
				console.error('Error accessing webcam:', error);
			});
	}

	function captureImage() {
		const canvas = document.createElement('canvas');
		canvas.width = videoElement.videoWidth;
		canvas.height = videoElement.videoHeight;
		const context = canvas.getContext('2d');
		context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
		const imageData = canvas.toDataURL('image/png');
		console.log('Captured image:', imageData);
	}

	onMount(startWebcam);
</script>

<video bind:this={videoElement} autoplay>
	<track kind="captions" />
</video>
<button on:click={captureImage}>Capture Image</button>

<style>
	video {
		width: 100%;
		max-width: 500px;
	}
	button {
		display: block;
		margin-top: 10px;
	}
</style>
