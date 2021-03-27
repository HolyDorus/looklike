<script>
    import { onDestroy, onMount } from 'svelte';
    import { link } from 'svelte-routing';

    import { isAuthorized, logOut } from '../auth.js'


    let startPoint;

    onMount(() => {
        document.addEventListener('touchstart', function(event) {
            startPoint = event.changedTouches[0];
        });

        document.addEventListener('touchmove', function(event) {
            const currentPoint = event.changedTouches[0];

            const xDifference = currentPoint.clientX - startPoint.clientX;
            const yDifference = currentPoint.clientY - startPoint.clientY;          

            if(Math.abs(xDifference) > 100 && Math.abs(yDifference) < 50) {
                if(xDifference < 0) {
                    burgerMenuClose();
                }

                if(xDifference > 0) {
                    burgerMenuOpen();
                }
            }
        });
    });

    onDestroy(() => {
        document.body.parentElement.classList.remove('scroll-lock');
    });

    function burgerClickHandler(event) {
        const burger = event.currentTarget;
        const menu = burger.nextElementSibling;

        burger.classList.toggle('active');
        menu.classList.toggle('active');
        document.body.parentElement.classList.toggle('scroll-lock')
    }

    function burgerMenuOpen() {
        const burger = document.querySelector('.header__burger');
        const menu = burger.nextElementSibling;

        burger.classList.add('active');
        menu.classList.add('active');
        document.body.parentElement.classList.add('scroll-lock')
    }

    function burgerMenuClose() {
        const burger = document.querySelector('.header__burger');
        const menu = burger.nextElementSibling;

        burger.classList.remove('active');
        menu.classList.remove('active');
        document.body.parentElement.classList.remove('scroll-lock')
    }

    function logOutLinkClickHandler() {
        logOut();
    }
</script>

<header class="header">
    <div class="container">
        <div class="header__body">
            <a href="/" class="header__logo" use:link>
                <img src="images/logo.png" alt="Логотип">
            </a>

            <div class="header__burger" on:click={burgerClickHandler}>
                <span></span>
            </div>

            <nav class="header__menu">
                <ul class="header__list">
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
            </nav>
        </div>
    </div>
</header>
<div id="fake-header-area"></div>

<style>
    #fake-header-area {
        width: 100%;
        height: 60px;
    }

    .header {
        width: 100%;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 9999;
    }

    .header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgb(36, 36, 36);
        z-index: 2;
    }

    .header__body {
        position: relative;
        display: flex;
        justify-content: space-between;
        height: 60px;
        align-items: center;
    }

    .header__logo {
        flex: 0 0 100px;
        z-index: 3;
    }

    .header__logo img {
        display: block;
        max-width: 100%;
    }

    .header__burger {
        display: none;
    }

    :global(.header__burger.active::before) {
        transform: rotate(45deg);
        top: 9px !important;
    }

    :global(.header__burger.active::after) {
        transform: rotate(-45deg);
        bottom: 9px !important;
    }

    :global(.header__burger.active span) {
        transform: scale(0);
    }

    .header__list {
        display: flex;
        position: relative;
        z-index: 2;
    }

    .header__list li {
        position: relative;
        margin: 0 0 0 20px;
    }

    .header__list li a {
        font-size: 1.6rem;
        font-weight: 500;
        transition: 0.15s all;
        color: rgb(209, 209, 209);
    }

    .header__list li a:hover {
        transition: 0.15s all;
        color: white
    }

    @media (max-width: 768px) {
        :global(html.scroll-lock) {
            overflow: hidden;
            position: relative;
            height: 100%;
        }

        #fake-header-area {
            height: 50px;
        }

        .header__body {
            height: 50px;
        }

        .header__logo {
            flex: 0 0 80px;
        }

        .header__burger {
            display: block;
            position: relative;
            width: 30px;
            height: 20px;
            z-index: 3;
        }

        .header__burger span {
            background-color: white;
            border-radius: 15px;
            position: absolute;
            width: 100%;
            height: 2px;
            left: 0;
            top: 9px;
            transition: 0.3s all;
        }

        .header__burger::before,
        .header__burger::after {
            content: '';
            background-color: white;
            border-radius: 15px;
            position: absolute;
            width: 100%;
            height: 2px;
            left: 0;
            transition: 0.3s all;
        }

        .header__burger::before {
            top: 0;
        }

        .header__burger::after {
            bottom: 0;
        }

        .header__menu {
            position: fixed;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background-color: rgb(94, 94, 94);
            padding: 70px 20px 30px 20px;
            overflow: auto;
            transition: 0.3s all;
        }

        :global(.header__menu.active) {
            left: 0 !important;
        }

        .header__list {
            display: block;
        }

        .header__list li {
            margin: 0 0 20px 0;
        }

        .header__list li a {
            font-size: 2.5rem;
        }
    }
</style>