<script>
    import Header from '../components/Header.svelte';
</script>

<svelte:head>
    <title>Look Like | Сторінка не знайдена</title>
</svelte:head>

<Header/>
<div class="container">
    <div id="some-error">
        <div class="some-error">
            <div>
                <span></span>
            </div>
            <h2>Упс! Щось пішло не так</h2>
            <p>Невірно оброблений запит, або сервер наразі недоступний</p>
            <a class="black-button" href="/">Повернутися на головну</a>
        </div>
    </div>
</div>

<style>
    #some-error {
        position: relative;
        height: 80vh;
    }

    #some-error .some-error {
        position: absolute;
        left: 50%;
        top: 50%;
        -webkit-transform: translate(-50%, -50%);
        -ms-transform: translate(-50%, -50%);
        transform: translate(-50%, -50%);
    }

    .some-error {
        max-width: 520px;
        width: 100%;
        text-align: center;
        line-height: 1.4;
    }

    .some-error div {
        height: 190px;
    }

    .some-error span {
        display: inline-block;
        width: 120px;
        height: 120px;
        background-image: url('../images/emoji.png');
        background-size: cover;
        -webkit-transform: scale(1.2);
        -ms-transform: scale(1.2);
        transform: scale(1.2);
        z-index: -1;
    }

    .some-error h2 {
        font-size: 22px;
        font-weight: 700;
        margin: 0;
        color: #383838;
    }

    .some-error p {
        color: #787878;
        font-weight: 300;
        margin: 1rem 0 2rem 0;
    }
</style>