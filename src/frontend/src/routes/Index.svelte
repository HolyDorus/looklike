<script>
    import { onMount } from 'svelte';

    import Header from '../components/Header.svelte';
    import CharactersCard from '../components/CharactersCard.svelte';

    import { isAuthorized, formatAuthorizationHeader } from '../auth.js';
    import { apiUrl } from '../settings';


    let newessCharacters = [];

    onMount(async () => {
        const result = await loadNewessCharacters();
        newessCharacters = result;
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
    <title>Look Like | Головна</title>
</svelte:head>

<Header/>
<div class="container">
    <h1>Найновіші образи</h1>
    <div class="characters-grid">
        {#if newessCharacters.length}
            {#each newessCharacters as character}
                <CharactersCard character={character}/>
            {/each}     
        {/if}
    </div>
    <h1>Найпопулярніші образи</h1>
    <div class="characters-grid">
        {#if newessCharacters.length}
            {#each newessCharacters as character}
                <CharactersCard character={character}/>
            {/each}     
        {/if}
    </div>
    <div style="height: 50px;"></div>
</div>

<style>
    h1 {
        text-align: center;
        margin-top: 20px;
        color: #383838;
    }
</style>