<script>
    import { link } from "svelte-routing";
</script>

<header>
    <div class="container">
        <div class="header-wrapper">
            <a href="/" class="logo" use:link>
                <img src="images/logo.png" alt="Логотип">
            </a>
            <ul class="navbar">
                <li>
                    <a href="/search" use:link>Пошук</a>
                </li>
                <li>
                    <a href="/register" use:link>Зареєструватися</a>
                </li>
                <li>
                    <a href="/login" use:link>Увійти</a>
                </li>
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
        z-index: 9999;
    }

    .header-wrapper {
        display: flex;
        align-items: center;
        padding: 5px 0;
    }

    .logo {
        margin: 5px 0;
    }

    .logo img {
        height: 35px;
    }

    .navbar {
        margin-left: auto;
        display: flex;
        align-items: center;
    }

    .navbar li:not(:first-child){
        margin-left: 40px;
    }

    .navbar li a {
        transition: 0.1s all;
    }

    .navbar li a:hover {
        transition: 0.1s all;
        color: rgb(221, 221, 221);
    }

    #fake-header-area {
        width: 100%;
        height: 59px;
    }
</style>