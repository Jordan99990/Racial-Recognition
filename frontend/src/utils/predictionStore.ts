import { writable } from 'svelte/store';

export const predictionStore = writable({});
export const selectedModel = writable(localStorage.getItem('selectedModel') || 'fastai v1');

selectedModel.subscribe(value => {
    localStorage.setItem('selectedModel', value);
});