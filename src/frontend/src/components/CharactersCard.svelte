<script>
    import { navigate } from "svelte-routing";

    import { isAuthorized, formatAuthorizationHeader } from '../auth.js';
    import { apiUrl } from '../settings.js';
    import { formatBigNumber } from '../utils.js';


    export let character;

    async function likeButtonClickHandler(event) {
        if (!isAuthorized()) {
            navigate('/login');
            return;
        }

        if ($character.is_favorite) {
            await removeFromFavorites($character.id);
            $character.is_favorite = false;
            $character.likes -= 1;
        } else {
            await addToFavorites($character.id);
            $character.is_favorite = true;
            $character.likes += 1;
        }
    }

    async function removeFromFavorites(character_id) {
        try {
            const response = await fetch(`${apiUrl}/characters/${character_id}/remove-from-favorites`, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Authorization': formatAuthorizationHeader()
                }
            });

            if (response.status === 401) {
                navigate('/login');
                return;
            }

            if (response.status === 404) {
                navigate('/oops');
                return;
            }
        }
        catch (e) {
            navigate('/oops');
            return;
        }
    }

    async function addToFavorites(character_id) {
        try {
            const response = await fetch(`${apiUrl}/characters/${character_id}/add-to-favorites`, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Authorization': formatAuthorizationHeader()
                }
            });

            if (response.status === 401) {
                navigate('/login');
                return;
            }

            if (response.status === 404 || response.status === 400) {
                navigate('/oops');
                return;
            }
        }
        catch (e) {
            navigate('/oops');
            return;
        }
    }
</script>

<div class="character-item">
    <img src={$character.image_path} class="character-item__image" alt="Образ">
    <div class="character-item__clothes-grid" >
        {#each $character.clothes as clothes}
            <div class="character-item__clothes-wrapper">
                <div tooltip={clothes.name}>
                    <img src={clothes.image_path} class="character-item__clothes-image" alt={clothes.name}>
                </div>
            </div>
        {/each}
    </div>
    <p>{$character.description}</p>
    <div class="character-item__additional-wrapper">
        <span class="character-item__date" tooltip={$character.posted_at.time}>{$character.posted_at.date}</span>
        <button class="like-button" on:click={likeButtonClickHandler}>
            {#if $character.is_favorite}
                <i class="material-icons like-icon active">favorite</i>
                <span class="character-item__likes-count active">{formatBigNumber($character.likes)}</span>
            {:else}
                <i class="material-icons like-icon disactive">favorite_border</i>
                <span class="character-item__likes-count disactive">{formatBigNumber($character.likes)}</span>
            {/if}
        </button>
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
        padding: 15px 15px 70px 15px;
        text-align: justify;
        font-size: 1.6rem;
        line-height: 1.5em;
    }

    .character-item__additional-wrapper {
        position: absolute;
        bottom: 0;
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 15px 15px 15px;
    }

    .character-item__date {
        display: block;
        position: relative;
        font-size: 1.6rem;
        color: rgb(82, 82, 82);
    }

    .like-button {
        display: flex;
        align-items: center;
        background-color: transparent;
        cursor: pointer;
        transition: 0.2s all;
    }

    .like-button:hover {
        background-color: rgba(255, 255, 255, 0.1);        
        transition: 0.2s all;
    }

    .character-item__likes-count {
        margin-left: 5px;
        font-size: 1.6rem;
        font-weight: 500;
    }

    .like-icon {
        font-size: 25px !important;
        transition: 0.2s all;
    }

    .disactive {
        color: rgb(128, 128, 128);
    }

    .active  {
        color: #f7c121;
    }

    @media (max-width: 768px) {
        .character-item:hover {
            /* Removes original hover effect on mobile devices */
            transform: none;
            box-shadow: 0 0 10px rgba(0,0,0,0.3);
        }
    }
</style>