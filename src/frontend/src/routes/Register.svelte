<script>
    import { link, navigate } from 'svelte-routing';

    import Header from '../components/Header.svelte';
    import Footer from '../components/Footer.svelte';

    import { setToken } from '../auth.js'
    import { apiUrl, siteTitle } from '../settings.js';
    import { RegisterFormValidator } from '../form-validators.js';
    import { whooshAnimation } from '../utils.js';


    let errors = [];

    
    async function submitRegisterFormHandler(event) {
        event.preventDefault();

        const validator = new RegisterFormValidator(event.target);
        const validationErrors = validator.validate();

        if (validationErrors.length) {
            errors = validationErrors;
            return;
        }

        const tokenObject = await tryRegister(validator.username, validator.password);

        if (tokenObject) {
            setToken(tokenObject.access_token);
            navigate('/');
        }
    }

    async function tryRegister(username, password) {
        try {
            const RegisterResponse = await fetch(`${apiUrl}/users/register`, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({username, password})
            });

            if (RegisterResponse.status === 409) {
                errors = ['Користувач з таким ім\'ям вже існує!']
                return null;
            }

            const LoginResponse = await fetch(`${apiUrl}/users/login`, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({username, password})
            });

            return await LoginResponse.json();
        }
        catch (e) {
            navigate('/oops');
        }
    }
</script>

<svelte:head>
    <title>Реєстрація | {siteTitle}</title>
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
        <div class="lr-card-title">Реєстрація</div>
        <div class="lr-card-main">
            <form on:submit={submitRegisterFormHandler} method="POST">
                <div class="lr-card-form-container">
                    <div class="lr-card-fields-wrapper">
                        <label>Логін: <input type="text" name="username" autocomplete="username"></label>
                        <label>Пароль: <input type="password" name="password" autocomplete="new-password"></label>
                        <label>Підтвердження паролю: <input type="password" name="passwordConfirmation" autocomplete="new-password"></label>
                    </div>
                    <button type="submit" class="black-button lr-card-button">Зареєструватися</button>
                </div>
            </form>
        </div>
        <div class="lr-card-additionally">У вас вже є акаунту? <a href="/login" class="lr-card-link" use:link>Увійти</a></div>
    </div>
</div>
<Footer/>
