<script>
    import { link } from 'svelte-routing';

    import { isAuthorized, logOut } from '../auth.js'


    function logOutLinkClickHandler() {
        logOut();
    }
</script>

<header>
    <div class="container">
        <div class="header-wrapper">
            <a href="/" class="logo" use:link>
                <img src="images/logo.png" alt="Логотип" width=102 height=35>
            </a>
            <ul class="navbar">
                <li>
                    <a href="/search" use:link>Пошук</a>
                </li>

                {#if isAuthorized()}
                    <li>
                        <a href="/favorites" use:link>Вподобані образи</a>
                    </li>
                    <li>
                        <a href="/" class="logout-link" on:click={logOutLinkClickHandler}>Вийти</a>
                    </li>
                {:else}
                    <li>
                        <a href="/register" use:link>Зареєструватися</a>
                    </li>
                    <li>
                        <a href="/login" use:link>Увійти</a>
                    </li>
                {/if}
            </ul>
        </div>
    </div>
</header>
<div id="fake-header-area"></div>

<style>
    header {
        background-color: rgb(36, 36, 36);
        width: 100%;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 9999;
    }

    .header-wrapper {
        display: flex;
        align-items: center;
        padding: 10px 0;
    }

    .logo,
    .logo img {
        height: 35px;
    }

    .navbar {
        margin-left: auto;
        display: flex;
        align-items: center;
        justify-content: space-around;
        width: 40%;        
    }

    .navbar li {
        text-align: center;
    }

    .navbar li a {
        transition: 0.1s all;
        font-size: 1.6rem;
    }

    .navbar li a:hover {
        transition: 0.1s all;
        color: rgb(221, 221, 221);
    }

    #fake-header-area {
        width: 100%;
        height: 55px;
    }

    .logout-link {
        transition: 0.2s all !important;
    }

    .logout-link:hover {
        transition: 0.2s all !important;
        color: rgb(228, 2, 2) !important;
    }
</style>