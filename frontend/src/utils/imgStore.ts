import { writable } from "svelte/store";

export const image = writable<string | null>(null);