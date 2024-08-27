<script lang="ts">
  import Navbar from './lib/Navbar.svelte';
  import Footer from './lib/Footer.svelte';
  import UserInput from './lib/UserInput.svelte';
  import Prediction from './lib/Prediction.svelte';
  import Stats from './lib/Stats.svelte';
  import { onMount } from 'svelte';

  let currentPage: string = 'home';
  let moveLeft: boolean = false;
  let visibility = 'hidden';

  const navigate = (page: string) => {
      currentPage = page;
      history.pushState(null, '', page === 'home' ? '/' : `/${page}`);
  };

  const handleButtonPress = () => {
      moveLeft = true;
      visibility = 'visible';
  };

  onMount(() => {
      const path = window.location.pathname.slice(1);
      currentPage = path || 'home';

      window.addEventListener('popstate', () => {
          currentPage = window.location.pathname.slice(1) || 'home';
      });
  });
</script>

<style>
    .move-left {
        transform: translateX(-450px);
        transition: transform 0.3s ease;
    }
</style>

<main>
  <Navbar {navigate} />

  {#if currentPage === 'home'}
      <div class:move-left={moveLeft}>
          <UserInput on:buttonPress={handleButtonPress} />
      </div>

    <Prediction {visibility}/>
  {:else if currentPage === 'stats'}
      <Stats />
  {/if}
</main>

<Footer/>