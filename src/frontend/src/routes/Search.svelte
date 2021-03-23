<script>
    import { onMount } from 'svelte';
    import { navigate } from 'svelte-routing';

    import Header from '../components/Header.svelte';
    import ClothesBox from './../components/ClothesBox.svelte';

    import { apiUrl } from '../settings';
    import { whooshAnimation } from '../utils.js';


    let clothesList = [];
    let error;

    onMount(async () => {
        const result = await loadPrimaryClothes();
        clothesList = result;
    });

    function searchButtonClickHandler(event) {
        const allSelectedItemIds = collectAllSelectedItemIds();

        if (!allSelectedItemIds.length) {
            error = 'Небхідно обрати хоча б один елемент одягу!';
            return;
        }

        const formatedSelectedItemIdsString = formatSelectedItemIds(allSelectedItemIds);
        const url = `/search-result?${formatedSelectedItemIdsString}`

        navigate(url);
    }

    function collectAllSelectedItemIds() {
        let selectedItemIds = [];
        let allMajorClothesBoxes = document.querySelectorAll('.clothes-box');

        for (let majorClothesBox of allMajorClothesBoxes) {
            const selectedItemId = majorClothesBox.dataset.selectedClothesId;
            if (selectedItemId) selectedItemIds.push(selectedItemId);
        }

        return selectedItemIds;
    }

    function formatSelectedItemIds(allSelectedItemIds) {
        let str = 'clothes[]=';

        for (let i = 0; i < allSelectedItemIds.length; i++) {
            str += allSelectedItemIds[i];
            if (i !== allSelectedItemIds.length - 1) str += ',';
        }

        return str;
    }

    async function loadPrimaryClothes() {
        const response = await fetch(`${apiUrl}/clothes/?primary_only`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });
        return await response.json();
    };
</script>

<svelte:head>
    <title>Look Like | Пошук</title>
</svelte:head>

<Header/>
<div class="container">
    <h1>Оберіть вподобаний одяг</h1>
    {#each clothesList as clothes}
        <ClothesBox clothes={clothes}/>
    {/each}
    
    {#if error }
        <div in:whooshAnimation class="block-status b-errors">
            <span>Помилки:</span>
            <ul>
                <li>{error}</li>
            </ul>
        </div>
    {/if}

    <div class="black-button-wrapper">
        <button class="black-button" on:click={searchButtonClickHandler}>Підібрати образи</button>
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
        padding: 30px 0;
    }
</style>
