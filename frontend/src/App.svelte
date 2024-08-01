<script lang="ts">
  import Navbar from './lib/Navbar.svelte';
  import Footer from './lib/Footer.svelte';
  import UserInput from './lib/UserInput.svelte';
  import { onMount } from 'svelte';

  let currentPage: string = 'home';

  const navigate = (page: string) => {
      currentPage = page;
      history.pushState(null, '', page === 'home' ? '/' : `/${page}`);
  };

  onMount(() => {
      const path = window.location.pathname.slice(1);
      currentPage = path || 'home';

      window.addEventListener('popstate', () => {
          currentPage = window.location.pathname.slice(1) || 'home';
      });
  });
</script>

<main>
  <Navbar {navigate} />

  {#if currentPage === 'home'}
      <UserInput/>
  {:else if currentPage === 'stats'}
      <div>
          <h1>Stats Page</h1>
          <p>Here are some statistics.</p>
      </div>
  {/if}
</main>

<Footer/>