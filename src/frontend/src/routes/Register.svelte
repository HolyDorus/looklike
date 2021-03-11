<script>
    import Header from './../components/Header.svelte';


    function submitRegisterFormHandler() {
        alert('Знаходиться в розробці...')
    }
</script>

<svelte:head>
    <title>Look Like | Реєстрація</title>
</svelte:head>

<Header/>
<div class="container">
    <div class="lr-card">
        <div class="lr-card-title">Реєстрація</div>
        <div class="lr-card-main">
            <form on:submit={submitRegisterFormHandler} method="POST">
                <div class="lr-card-form-container">
                    <div class="lr-card-fields-wrapper">
                        <label>Логін: <input type="text" name="login"></label>
                        <label>Пароль: <input type="password" name="password"></label>
                        <label>Підтвердження паролю: <input type="password" name="password"></label>
                    </div>
                    <button type="submit" class="black-button lr-card-button">Зареєструватися</button>
                </div>
            </form>
        </div>
        <div class="lr-card-additionally">У вас вже є акаунту? <a href="/login" class="lr-card-link">Увійти</a></div>
    </div>
</div>

<style>
    .lr-card {
        margin: 100px auto 0 auto;
        background-color: inherit;
        max-width: 450px;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
    }

    .lr-card-title {
        text-align: center;
        padding-top: 20px;
        padding-bottom: 25px;
        font-size: 2rem;
        font-weight: 500;
    }

    .lr-card-additionally {
        text-align: center;
        padding-top: 30px;
        padding-bottom: 20px;
    }

    .lr-card-button {
        width: 100%;
        font-size: 1.3rem;
        padding: 10px 0;
    }

    .lr-card-link {
        text-decoration: underline;
        color: rgb(5, 105, 220);
    }

    .lr-card-main label {
        display: block;
    }

    .lr-card-form-container {
        padding: 0 10%;
    }

    .lr-card-fields-wrapper {
        padding-bottom: 10px;
    }

    .lr-card-fields-wrapper input {
        width: 100%;
        font-size: 1.5rem;
        margin-bottom: 15px;
        margin-top: 7px;
        padding: 5px 10px;
        color: #383838;
        outline: rgb(161, 161, 161) solid 1px;
    }

    .lr-card-fields-wrapper input:focus {
        outline: rgb(102, 102, 102) solid 2px;
    }
</style>