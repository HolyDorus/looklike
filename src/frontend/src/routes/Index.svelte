<script>
    import { onMount } from 'svelte';
    import { link } from 'svelte-routing';
    import { writable } from 'svelte/store';

    import Header from '../components/Header.svelte';
    import CharactersCard from '../components/CharactersCard.svelte';

    import { isAuthorized, formatAuthorizationHeader } from '../auth.js';
    import { apiUrl, siteTitle } from '../settings.js';


    let newessCharacters = [];

    onMount(async () => {
        const result = await loadNewessCharacters();

        for (let item of result) {
            newessCharacters.push(writable(item));
        }

        newessCharacters = newessCharacters;
    });

    async function loadNewessCharacters() {
        let request_headers = {
            'Accept': 'application/json'
        };

        if (isAuthorized()) {
            request_headers['Authorization'] = formatAuthorizationHeader();
        }

        const response = await fetch(`${apiUrl}/characters/filter?type=newness&limit=3`, {
            method: 'GET',
            headers: request_headers
        });

        let responseData = await response.json();

        if (!response.ok) {
            navigate('/oops');
        }

        return responseData;
    };
</script>

<svelte:head>
    <title>{siteTitle}</title>
</svelte:head>

<Header/>
<div class="container">
    <h1>Найновіші образи</h1>
    <div class="characters-grid">
        {#each newessCharacters as character}
            <CharactersCard character={character}/>
        {/each}
    </div>
    <div class="black-button-wrapper">
        <a href="/test1" class="black-button" use:link>Дивитись ще</a>
    </div>

    <h1>Найпопулярніші образи</h1>
    <div class="characters-grid">
        {#each newessCharacters as character}
            <CharactersCard character={character}/>
        {/each}
    </div>
    <div class="black-button-wrapper">
        <a href="/test2" class="black-button" use:link>Дивитись ще</a>
    </div>
</div>

<style>
    h1 {
        text-align: center;
        margin-top: 20px;
        color: #383838;
    }

    .black-button-wrapper {
        display: flex;
        justify-content: center;
        margin: 30px 0 60px 0;
    }
</style>