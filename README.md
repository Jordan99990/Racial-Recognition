<h1 align="center">Ethnicity Classifier</h1>

<p align="justify">
This project aims to use FastAI models trained on Face Data dataset to perform facial recognition and classification tasks. The goal is to leverage the capabilities of FastAI to accurately identify and categorize faces(also gender and age).
</p>

# Architecture
![](/img/3.png)

## Built with
![Svelte](https://img.shields.io/badge/svelte-%23f1413d.svg?style=for-the-badge&logo=svelte&logoColor=white)![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)


<p align="justify">
The project leverages a variety of technologies and tools to achieve its goals. The main components of the tech stack include:

1. **FastAI:**
   - FastAI is used for building and training the deep learning models. It provides high-level abstractions for common deep learning tasks, making it easier to implement state-of-the-art models with minimal code.

2. **Flask:**
   - Flask is used to serve the trained model as a web application. It provides a lightweight and flexible framework for building web APIs and serving static files.

3. **Svelte:**
   - Svelte is used for building the front-end of the web application. It is a modern JavaScript framework that compiles components into highly efficient imperative code, providing a fast and responsive user interface.

4. **Jupyter Notebooks:**
   - Jupyter Notebooks are used for experimentation and prototyping. They allow for interactive development and visualization of results, making it easier to iterate on model improvements.
  
</p>

# Dataset

The dataset utilized for model training and evaluation is [Fairface](https://github.com/dchen236/FairFace).

A Multi-Task Cascaded Convolutional Network (MTCNN) was used to detect and crop faces from images. The models were exclusively trained on facial data.

# FastAI Architecture
## Model V1

- **Architecture**: ResNet34
- **Training**:
  - Fine-tuning for 10 epochs with a base learning rate of 1e-3.
  - Metrics: `accuracy_multi`
  - Model saved as `fairface_v1.pkl` and `fairface_v1.pth`.

## Model V2

- **Architecture**: ResNet34
- **Training**:
  - Fine-tuning for 10 epochs with a base learning rate of 1e-3.
  - First 3 epochs with frozen layers.
  - Metrics: `partial(accuracy_multi, thresh=0.5)`
  - Model saved as `fairface_v2.pkl` and `fairface_v2.pth`.

## Model V3

- **Architecture**: ResNet50
- **Training**:
  - Fine-tuning for 12 epochs with a base learning rate of 1e-3.
  - Callbacks: `SaveModelCallback`, `EarlyStoppingCallback`, `ReduceLROnPlateau`
  - Metrics: `partial(accuracy_multi, thresh=0.5)`
  - Model saved as `fairface_v3.pkl` and `fairface_v3.pth`.

# Screenshots
<p align="justify">

![](/img/first.png)
![](/img/second.png)
![](/img/third.png)

</p>