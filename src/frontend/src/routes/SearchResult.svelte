<script>
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
    import { navigate } from 'svelte-routing';
    
    import CharactersCard from '../components/CharactersCard.svelte';
    import Header from '../components/Header.svelte';
    import Footer from '../components/Footer.svelte';

    import { isAuthorized, formatAuthorizationHeader } from '../auth.js'
    import { apiUrl, siteTitle } from '../settings.js';
    import { getAllUrlGetParams, whooshAnimation } from '../utils.js';


    let searchResult = [];
    let errors = [];


    onMount(async () => {
        const urlPart = formatUrlPart(window.location.href);
        const result = await loadSearchResult(urlPart);

        if (result && Array.isArray(result)){
            if (!result.length) {
                errors = ['На жаль, образів з такими речами не знайдено'];
            } else {
                for (let item of result) {
                    searchResult.push(writable(item));
                }

                searchResult = searchResult;
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
        try {
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

            if (response.status === 404) {
                errors = ['Не знайдено один або декілька елементів одягу зі списку']
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
    <title>Результати пошуку | {siteTitle}</title>
</svelte:head>

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

    {#if errors.length}
        <div in:whooshAnimation class="block-status b-errors">
            <span>Помилки:</span>
            <ul>
                {#each errors as error}
                    <li>{error}</li>
                {/each}
            </ul>
        </div>
    {/if}

    <div class="black-button-wrapper">
        <a class="black-button" href="/search">Обрати інший одяг</a>
    </div>
</div>
<Footer/>

<style>
    h1 {
        text-align: center;
        margin-top: 20px;
        color: #383838;
    }

    .black-button-wrapper {
        margin-top: 30px;
        display: flex;
        justify-content: center;
    }
</style>