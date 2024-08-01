<style>
    footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0;
        background-color: #1a1a1a;
        color: #fff;
        z-index: 1000;
        height: 3rem;
        border-radius: 10px; 
    }

    .footer-content {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        height: 100%;
    }

    .footer-info {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
        padding: 0.5rem;
    }
</style>

<footer>
    <div class="footer-content">
        <div class="footer-info">
            <p>&copy; {new Date().getFullYear()} Racial Recognition App</p>
        </div>
    </div>
</footer>
