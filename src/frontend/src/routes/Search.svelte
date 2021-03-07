<script>
    import { onMount } from 'svelte';
    import { elasticOut } from 'svelte/easing';
    import { navigate } from "svelte-routing";

    import Header from './../components/Header.svelte';
    import ClothesBox from './../components/ClothesBox.svelte';

    import { apiUrl } from '../settings';

    
    function whooshAnimation(node, params) {
		const existingTransform = getComputedStyle(node).transform.replace('none', '');

		return {
			delay: params.delay || 0,
			duration: params.duration || 400,
			easing: params.easing || elasticOut,
			css: (t, u) => `transform: ${existingTransform} scale(${t})`
		};
	}

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
        const response = await fetch(`${apiUrl}/api/v1/clothes/?primary_only`, {
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
    {#each clothesList as clothes}
        <ClothesBox clothes={clothes}/>
    {/each}
    
    {#if error }
        <div transition:whooshAnimation class="block-status b-errors">
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
    .black-button-wrapper {
        display: flex;
        justify-content: center;
        padding: 30px 0;
    }
</style>
