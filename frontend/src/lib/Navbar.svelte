<script>
    export let navigate;

    const handleNavigation = (/** @type {string} */ page) => {
        navigate(page);
    };
</script>

<style>
    nav {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0;
        background-color: #333;
        z-index: 1000; 
        height: 3rem; 
    }

    .nav-link {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
        text-decoration: none;
        padding: 0.5rem 0;
        transition: background-color 0.3s;
        height: 100%;
        cursor: pointer;
    }

    .nav-link:hover {
        background-color: #555;
    }

</style>

<nav>
    <button class="nav-link" on:click={() => handleNavigation('home')} role="link">Home</button>
    <button class="nav-link" on:click={() => handleNavigation('stats')} role="link">Stats</button>
</nav>
