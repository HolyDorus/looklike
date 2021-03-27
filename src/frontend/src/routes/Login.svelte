<script>
    import { link, navigate } from 'svelte-routing';

    import Header from '../components/Header.svelte';

    import { setToken } from '../auth.js'
    import { apiUrl, siteTitle } from '../settings.js';
    import { LoginFormValidator } from '../form-validators.js';
    import { whooshAnimation } from '../utils.js';


    let errors = [];


    async function submitLoginFormHandler(event) {
        event.preventDefault();

        const validator = new LoginFormValidator(event.target);
        const validationErrors = validator.validate();

        if (validationErrors.length) {
            errors = validationErrors;
            return;
        }

        const tokenObject = await tryLogin(validator.username, validator.password);

        if (tokenObject) {
            setToken(tokenObject.access_token);
            navigate('/');
        }
    }

    async function tryLogin(username, password) {
        try {
            const response = await fetch(`${apiUrl}/users/login`, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({username, password})
            });

            if (response.status === 404) {
                errors = ['Не знайдено користувача з таким ім\'ям!']
                return null;
            }

            if (response.status === 401) {
                errors = ['Надано невірний пароль!']
                return null;
            }

            return await response.json();
        }
        catch (e) {
            navigate('/oops');
        }
    }
</script>

<svelte:head>
    <title>Вхід | {siteTitle}</title>
</svelte:head>

<Header/>
<div class="container">
    {#if errors.length }
        <div in:whooshAnimation class="block-status b-errors">
            <span>Помилки:</span>
            <ul>
                {#each errors as error}
                    <li>{error}</li>
                {/each}
            </ul>
        </div>
    {/if}

    <div class="lr-card" class:min-margin-if-errors = "{errors.length}">
        <div class="lr-card-title">Вхід</div>
        <div class="lr-card-main">
            <form on:submit={submitLoginFormHandler} method="POST">
                <div class="lr-card-form-container">
                    <div class="lr-card-fields-wrapper">
                        <label>Логін: <input type="text" name="username" autocomplete="username"></label>
                        <label>Пароль: <input type="password" name="password" autocomplete="current-password"></label>
                    </div>
                    <button type="submit" class="black-button lr-card-button">Увійти</button>
                </div>
            </form>
        </div>
        <div class="lr-card-additionally">У вас ще немає акаунту? <a href="/register" class="lr-card-link" use:link>Зареєструватися</a></div>
    </div>
</div>