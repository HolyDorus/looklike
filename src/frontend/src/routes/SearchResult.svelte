<script>
    import { onMount } from 'svelte';
    import { navigate } from 'svelte-routing';
    
    import CharactersCard from '../components/CharactersCard.svelte';
    import Header from '../components/Header.svelte';

    import { isAuthorized, formatAuthorizationHeader } from '../auth.js'
    import { apiUrl } from '../settings';
    import { getAllUrlGetParams, whooshAnimation } from '../utils.js';


    let error;
    let searchResult = [];

    onMount(async () => {
        const urlPart = formatUrlPart(window.location.href);
        const result = await loadSearchResult(urlPart);

        if (result && Array.isArray(result)){
            if (!result.length) {
                error = 'На жаль, образів з такими речами не знайдено';
            } else {
                searchResult = result;
            }
        }
    });

    function formatUrlPart(url) {
        const allUrlGetParams = getAllUrlGetParams(url);
        const clothesIds = allUrlGetParams.clothes[0];
        let ouputString = '?clothes=';

        if (!clothesIds) return ouputString;

        return ouputString + clothesIds;
    }

    async function loadSearchResult(urlPart) {
        let request_headers = {
            'Accept': 'application/json'
        };

        if (isAuthorized()) {
            request_headers['Authorization'] = formatAuthorizationHeader();
        }

        const response = await fetch(`${apiUrl}/characters/find${urlPart}`, {
            method: 'GET',
            headers: request_headers
        });

        let responseData = await response.json();

        if (!response.ok) {
            if (responseData.message === 'One or more Clothes from the list were not found!') {
                error = 'Не знайдено один або декілька елементів одягу зі списку';
            } else {
                navigate('/oops');
            }
        }

        return responseData;
    };
</script>

<Header/>
<div class="container">
    {#if searchResult.length}
        <h1>Знайдені образи</h1>
        <div class="characters-grid">
            {#each searchResult as character}
                <CharactersCard character={character}/>
            {/each}
        </div>
    {/if}

    {#if error}
        <div in:whooshAnimation class="block-status b-errors">
            <span>Помилки:</span>
            <ul>
                <li>{error}</li>
            </ul>
        </div>
    {/if}

    <div class="black-button-wrapper">
        <a class="black-button" href="/search">Обрати інший одяг</a>
    </div>
</div>

<style>
    h1 {
        text-align: center;
        margin-top: 20px;
        color: #383838;
    }

    .black-button-wrapper {
        padding: 30px 0;
        display: flex;
        justify-content: center;
    }
</style>