<script>
    export let character;
</script>

<div class="character-item">
    <img src={character.image_path} class="character-item__image" alt="Образ">
    <div class="character-item__clothes-grid" >
        {#each character.clothes as clothes}
            <div class="character-item__clothes-wrapper">
                <div tooltip={clothes.name}>
                    <img src={clothes.image_path} class="character-item__clothes-image" alt={clothes.name}>
                </div>
            </div>
        {/each}
    </div>
    <p>{character.description}</p>
    <div class="character-item__date-wrapper">
        <span tooltip={character.posted_at.time}>{character.posted_at.date}</span>
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
        font-size: 0.9rem;
    }

    .character-item__date-wrapper {
        position: absolute;
        bottom: 20px;
        right: 20px;
    }

    .character-item__date-wrapper span {
        position: relative;
        font-size: 0.9rem;
        color: rgb(119, 119, 119);
    }
</style>