<script>
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
    import { navigate } from 'svelte-routing';

    import Header from '../components/Header.svelte';
    import CharactersCard from '../components/CharactersCard.svelte';

    import { isAuthorized, formatAuthorizationHeader } from '../auth.js'
    import { apiUrl, siteTitle } from '../settings.js';


    let favoriteCharacters = [];

    onMount(async () => {
        if (isAuthorized()) {
            const result = await loadFavoriteCharacters();

            for (let item of result) {
                favoriteCharacters.push(writable(item));
            }

            favoriteCharacters = favoriteCharacters;
        } else {
            navigate('/login');
        }
    });

    async function loadFavoriteCharacters() {
        const response = await fetch(`${apiUrl}/characters/favorites`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Authorization': formatAuthorizationHeader()
            }
        });

        let responseData = await response.json();

        if (!response.ok) {
            navigate('/oops');
        }

        return responseData;
    };
</script>

<svelte:head>
    <title>Вподобані образи | {siteTitle}</title>
</svelte:head>

<Header/>
<div class="container">
    <h1>Вподобані образи</h1>
    <div class="characters-grid">
        {#if favoriteCharacters.length}
            {#each favoriteCharacters as character}
                <CharactersCard character={character}/>
            {/each}     
        {/if}
    </div>
</div>
<div style="height: 50px;"></div>

<style>
    h1 {
        text-align: center;
        margin-top: 20px;
        color: #383838;
    }
</style>
