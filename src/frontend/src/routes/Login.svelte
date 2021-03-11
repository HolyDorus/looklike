<script>
    import Header from './../components/Header.svelte';


    function submitLoginFormHandler() {
        alert('Знаходиться в розробці...')
    }
</script>

<svelte:head>
    <title>Look Like | Вхід</title>
</svelte:head>

<Header/>
<div class="container">
    <div class="lr-card">
        <div class="lr-card-title">Вхід</div>
        <div class="lr-card-main">
            <form on:submit={submitLoginFormHandler} method="POST">
                <div class="lr-card-form-container">
                    <div class="lr-card-fields-wrapper">
                        <label>Логін: <input type="text" name="login"></label>
                        <label>Пароль: <input type="password" name="password"></label>
                    </div>
                    <button type="submit" class="black-button lr-card-button">Увійти</button>
                </div>
            </form>
        </div>
        <div class="lr-card-additionally">У вас ще немає акаунту? <a href="/register" class="lr-card-link">Зареєструватися</a></div>
    </div>
</div>