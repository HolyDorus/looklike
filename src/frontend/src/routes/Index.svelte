<script>
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';

    import Header from '../components/Header.svelte';
    import Footer from '../components/Footer.svelte';
    import CharactersCard from '../components/CharactersCard.svelte';

    import { isAuthorized, formatAuthorizationHeader } from '../auth.js';
    import { apiUrl, siteTitle } from '../settings.js';


    let newessCharacters = [];
    let popularCharacters = [];

    
    onMount(async () => {
        const result = await loadNewessCharacters();
        const result2 = await loadPopularCharacters();

        for (let item of result) {
            newessCharacters.push(writable(item));
        }

        for (let item of result2) {
            popularCharacters.push(writable(item));
        }

        newessCharacters = newessCharacters;
        popularCharacters = popularCharacters;
    });

    async function loadNewessCharacters() {
        try {
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

            return await response.json();
        }
        catch (e) {
            navigate('/oops');
        }
    };

    async function loadPopularCharacters() {
        try {
            let request_headers = {
                'Accept': 'application/json'
            };

            if (isAuthorized()) {
                request_headers['Authorization'] = formatAuthorizationHeader();
            }

            const response = await fetch(`${apiUrl}/characters/filter?type=popularity&limit=3`, {
                method: 'GET',
                headers: request_headers
            });

            return await response.json();
        }
        catch (e) {
            navigate('/oops');
        }
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

    <h1>Найпопулярніші образи</h1>
    <div class="characters-grid">
        {#each popularCharacters as character}
            <CharactersCard character={character}/>
        {/each}
    </div>
</div>

<style>
    h1 {
        text-align: center;
        margin-top: 20px;
        color: #383838;
    }

    h1:not(:first-of-type) {
        margin-top: 60px;
    }
</style>
<Footer/>
