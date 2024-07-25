<script>
	let selectedFile = null;

	function handleFileUpload(event) {
		selectedFile = event.target.files[0];
		const formData = new FormData();
		formData.append('file', selectedFile);

		fetch('/upload', {
			method: 'POST',
			body: formData,
		})
		.then(response => response.json())
		.then(data => {
			console.log('File uploaded successfully:', data);
		})
		.catch(error => {
			console.error('Error uploading file:', error);
		});
	}
</script>

<input type="file" on:change={handleFileUpload} />