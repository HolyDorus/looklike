<script>
    import { link, navigate } from "svelte-routing";

    import Header from './../components/Header.svelte';

    import { whooshAnimation } from '../utils.js';
    import { RegisterFormValidator } from '../form-validators.js';


    let errors = [];

    
    async function submitRegisterFormHandler(event) {
        event.preventDefault();

        const validator = new RegisterFormValidator(event.target);
        const validationErrors = validator.validate();

        if (validationErrors.length) {
            errors = validationErrors;
            return;
        }

        // await tryToRegister(validator.login, validator.password);

        navigate('/');
    }

    // async function tryToRegister(login, password) {
    //     const response = await fetch(`${apiUrl}/users/register`, {
    //         method: 'POST',
    //         headers: {
    //             'Accept': 'application/json',
    //             'Content-Type': 'application/json'
    //         },
    //         body: {
    //             login,
    //             password
    //         }
    //     });
    //     return await response.json();
    // };
</script>

<svelte:head>
    <title>Look Like | Реєстрація</title>
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
                        <label>Логін: <input type="text" name="login"></label>
                        <label>Пароль: <input type="password" name="password"></label>
                        <label>Підтвердження паролю: <input type="password" name="passwordConfirmation"></label>
                    </div>
                    <button type="submit" class="black-button lr-card-button">Зареєструватися</button>
                </div>
            </form>
        </div>
        <div class="lr-card-additionally">У вас вже є акаунту? <a href="/login" class="lr-card-link" use:link>Увійти</a></div>
    </div>
</div>
