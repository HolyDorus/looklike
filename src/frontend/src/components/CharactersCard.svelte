<script>
    import { navigate } from "svelte-routing";

    import { isAuthorized } from "../auth";


    export let character;
    let localCharacter = {...character}

    function likeButtonClickHandler(event) {
        if (!isAuthorized()) {
            navigate('/login');
            return;
        }

        console.log('Do', localCharacter.is_favorite)

        localCharacter.is_favorite = !localCharacter.is_favorite;

        console.log('Posle', localCharacter.is_favorite)
    }
</script>

<div class="character-item">
    <button class="like-button" on:click={likeButtonClickHandler}>
        {#if localCharacter.is_favorite}
            <i class="material-icons active-like-icon">favorite</i>
        {:else}
            <i class="material-icons disactive-like-icon">favorite_border</i>
        {/if}
    </button>

    <img src={localCharacter.image_path} class="character-item__image" alt="Образ">
    <div class="character-item__clothes-grid" >
        {#each localCharacter.clothes as clothes}
            <div class="character-item__clothes-wrapper">
                <div tooltip={clothes.name}>
                    <img src={clothes.image_path} class="character-item__clothes-image" alt={clothes.name}>
                </div>
            </div>
        {/each}
    </div>
    <p>{localCharacter.description}</p>
    <div class="character-item__date-wrapper">
        <span tooltip={localCharacter.posted_at.time}>{localCharacter.posted_at.date}</span>
    </div>
</div>

<style>
    .character-item {
        position: relative;
        transition: 0.4s all;
        margin-top: 30px;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
    }

    .character-item:hover {
        transform: translate(-3px, -3px);
        transition: 0.2s all;
        box-shadow: 0 0 15px rgba(0,0,0,0.9);
    }

    .character-item__image {
        width: 100%;
        height: 560px;
    }

    .character-item__image:hover {
        cursor: pointer;
    }

    .character-item__clothes-grid {
        display: flex;
        flex-wrap: wrap;
        padding: 0 5px;
        width: 100%;
    }

    .character-item__clothes-wrapper {
        width: 14%;
        position: relative;
    }

    .character-item__clothes-image {
        width: 100%;
        height: 60px;
        margin-top: 10px;
        cursor: pointer;
    }

    .character-item p {
        padding: 15px 15px 55px 15px;
        font-size: 1.44rem;
    }

    .character-item__date-wrapper {
        position: absolute;
        bottom: 20px;
        right: 20px;
    }

    .character-item__date-wrapper span {
        position: relative;
        font-size: 1.44rem;
        color: rgb(119, 119, 119);
    }

    .like-button {
        position: absolute;
        right: 0;
        top: 5px;
        height: 50px;
        width: 50px;
        background-color: transparent;
        border-radius: 10px;
        cursor: pointer;
        transition: 0.2s all;
        z-index: 2;
    }

    .character-item::after {
        content: '';
        position: absolute;
        top: 0px;
        right: 0;
        width: 70px;
        height: 70px;
        background-color: rgb(255, 254, 248);
        border-radius: 0 0 0 100%;
        cursor: pointer;
        z-index: 1;
    }

    .like-button:hover {
        background-color: rgba(255, 255, 255, 0.1);        
        transition: 0.2s all;
    }

    .disactive-like-icon {
        color: #f7c121;
        font-size: 35px !important;
        transition: 0.2s all;
    }

    .active-like-icon  {
        color: #f7c121;
        font-size: 35px !important;
        transition: 0.2s all;
    }
</style>