<script lang="ts">
let photoData: string;

async function capturePhoto(): Promise<void> {
    const constraints: MediaStreamConstraints = { video: true };
    const video: HTMLVideoElement = document.createElement('video');
    const canvas: HTMLCanvasElement = document.createElement('canvas');
    const context: CanvasRenderingContext2D | null = canvas.getContext('2d');

    try {
        const stream: MediaStream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = stream;
        await video.play();

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context?.drawImage(video, 0, 0, canvas.width, canvas.height);

        const dataUrl: string = canvas.toDataURL('image/jpeg');
        photoData = dataUrl;

        video.srcObject = null;
        stream.getTracks().forEach(track => track.stop());
    } catch (error) {
        console.error('Error accessing camera:', error);
    }
}

</script>

<div class="user-input">
    <div class="area">
        <button class="button" on:click={capturePhoto}>Capture Photo</button>
    </div>

    <div class="divider">OR</div>

    <button type="button" class="button">
        Select Photo
        <input type="file" accept="image/*" class="hidden"/>
    </button>
</div>

<style>
    .user-input {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 2rem;
    }

    .divider {
        margin: 1rem 0;
        font-size: 1.2rem;
        font-weight: bold;
    }

    input[type="file"] {
        margin-top: 1rem;
    }

    .hidden {
        display: none;
    }
</style>