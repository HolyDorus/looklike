<script>
    import Header from '../components/Header.svelte';
    
    import { siteTitle } from '../settings.js';
</script>

<svelte:head>
    <title>Сторінка не знайдена | {siteTitle}</title>
</svelte:head>

<Header/>
<div class="container">
    <div id="notfound">
        <div class="notfound">
            <div class="notfound-404">
                <h1>4<span></span>4</h1>
            </div>
            <h2>Упс! Сторінку не знайдено</h2>
            <p>Невірно набрана адреса, або такої сторінки на сайті більше не існує</p>
            <a class="black-button" href="/">Повернутися на головну</a>
        </div>
    </div>
</div>

<style>
    #notfound {
        position: relative;
        height: 80vh;
    }

    #notfound .notfound {
        position: absolute;
        left: 50%;
        top: 50%;
        -webkit-transform: translate(-50%, -50%);
        -ms-transform: translate(-50%, -50%);
        transform: translate(-50%, -50%);
    }

    .notfound {
        max-width: 520px;
        width: 100%;
        text-align: center;
        line-height: 1.4;
    }

    .notfound .notfound-404 {
        height: 190px;
    }

    .notfound .notfound-404 h1 {
        font-size: 146px;
        font-weight: 700;
        margin: 0px;
        color: #383838;
    }

    .notfound .notfound-404 h1>span {
        display: inline-block;
        width: 120px;
        height: 120px;
        background-image: url('../images/emoji.png');
        background-size: cover;
        z-index: -1;
    }

    .notfound h2 {
        font-size: 22px;
        font-weight: 700;
        margin: 0;
        color: #383838;
    }

    .notfound p {
        color: #787878;
        font-size: 1.6rem;
        font-weight: 300;
        margin: 1.6rem 0 3.2rem 0;
    }
</style>