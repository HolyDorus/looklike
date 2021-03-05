<script>
    import { onMount } from 'svelte';
    import { elasticOut } from 'svelte/easing';
    import { navigate } from "svelte-routing";
    
    import CharactersCard from '../components/CharactersCard.svelte';
    import Header from './../components/Header.svelte';

    import { getAllUrlParams } from '../utils.js';

    function whooshAnimation(node, params) {
		const existingTransform = getComputedStyle(node).transform.replace('none', '');

		return {
			delay: params.delay || 0,
			duration: params.duration || 400,
			easing: params.easing || elasticOut,
			css: (t, u) => `transform: ${existingTransform} scale(${t})`
		};
	}

    let error;
    let searchResult = [];

    onMount(() => {
        const urlPart = formatUrlPart(window.location.href);

        loadSearchResult(urlPart)
            .then(function(result) {
                searchResult = result;

                if (Array.isArray(searchResult) && !searchResult.length) {
                    error = 'На жаль, образів з такими речами не знайдено';
                }
            });
    });

    function formatUrlPart(url) {
        const getParams = getAllUrlParams(url);
        const clothesIdsList = getParams.clothes;
        let ouputString = '?clothes=';

        if (!clothesIdsList) return undefined;

        if (typeof clothesIdsList === 'string') {
            return ouputString + clothesIdsList;
        } else if (Array.isArray(clothesIdsList)) {
            for (let i = 0; i < clothesIdsList.length; i++) {
                ouputString += clothesIdsList[i];
                if (i !== clothesIdsList.length - 1) ouputString += ','
            }
        } else {
            return undefined;
        }

        return ouputString;
    }

    async function loadSearchResult(urlPart) {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/characters${urlPart}`, {
            method: 'GET'
        });

        let responseData = await response.json();

        if (!response.ok) {
            if (responseData.message === 'One or more Clothes from the list were not found!') {
                error = 'Один або декілька одягів зі списку не знайдено';
            } else {
                navigate('/oops');
            }
        }

        return responseData;
    };
</script>

<Header/>
<div class="container">
    <div class="characters-grid">
        {#if searchResult.length}
            {#each searchResult as character}
                <CharactersCard character={character}/>
            {/each}            
        {/if}
    </div>

    {#if error}
        <div transition:whooshAnimation class="block-status b-errors">
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
    .characters-grid {
        display: grid;
        grid-template-columns: repeat(3, 32%);
        justify-content: space-between;
    }

    .black-button-wrapper {
        padding: 30px 0;
        display: flex;
        justify-content: center;
    }
</style>