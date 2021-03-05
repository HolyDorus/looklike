<script>
    export let clothes = [];

    function clothesItemClickHandler(event) {
        let item = event.currentTarget;
        let boxContainer = item.parentElement;
        let clothesBox = boxContainer.parentElement;
        const itemId = item.dataset.id;
        const itemName = item.querySelector('span').textContent;
        const isItemSelected = item.classList.contains('selected');

        let majorClothesBox = findMajorClothesBox(item);
        if (majorClothesBox) {
            removeAllSelectedItemFromClothesBox(majorClothesBox);
            majorClothesBox.dataset.selectedClothesId = itemId;
        }

        if (isItemSelected) {
            delete majorClothesBox.dataset.selectedClothesId;
            removeAllAdjacentClothesBox(item);
            return;
        }

        item.classList.add('selected');
        removeAllAdjacentClothesBox(item);

        if (item.dataset.isMajorItem) return;

        loadClothesChildren(itemId)
            .then(function(clothesChildren) {
                if (clothesChildren && clothesChildren.length) {
                    clothesBox.appendChild(createClothesBox(clothesChildren, itemName));
                }
            });
    };

    function createClothesBox(clothesList, boxTitle) {
        let box = document.createElement('div');
        box.className = 'clothes-box';

        let hr = document.createElement('hr');
        let h2 = document.createElement('h2');
        h2.textContent = `↪ ${boxTitle}`;

        let boxContainer =  document.createElement('div');
        boxContainer.className = 'clothes-box__container';

        for (const clothesObject of clothesList) {
            let newItem = document.createElement('div');
            newItem.className = 'clothes-box__container__item';
            newItem.dataset.id = clothesObject.id;
            newItem.addEventListener('click', clothesItemClickHandler);

            let imgWrapper = document.createElement('div');
            imgWrapper.className = 'img-wrapper';

            let img = document.createElement('img');
            img.src = clothesObject.image_path;
            img.alt = clothesObject.name;

            let span = document.createElement('span');
            span.textContent = clothesObject.name;
            
            imgWrapper.appendChild(img);
            newItem.appendChild(imgWrapper);
            newItem.appendChild(span);

            boxContainer.appendChild(newItem);
        }

        box.appendChild(h2);
        box.appendChild(hr);
        box.appendChild(boxContainer);

        return box;
    }

    function removeAllAdjacentClothesBox(item) {
        let boxContainer = item.parentElement;
        let box = boxContainer.parentElement;
        let subClothesBoxes = box.querySelectorAll('.clothes-box');

        if (subClothesBoxes) {
            for (let subBox of subClothesBoxes) {
                if (subBox.parentElement === box) box.removeChild(subBox);
            }
        }
    }

    function findMajorClothesBox(item) {
        let lastFoundClothesBox;
        let boxContainer = item.parentElement;
        if (!boxContainer) return undefined;
        let clothesBox = boxContainer.parentElement;

        if (!clothesBox) {
            return undefined;
        } else {
            lastFoundClothesBox = clothesBox;
        }

        while (lastFoundClothesBox) {
            let tmpClothesBox = lastFoundClothesBox.parentElement;

            if (tmpClothesBox && tmpClothesBox.classList.contains('clothes-box')) {
                lastFoundClothesBox = tmpClothesBox;
            } else {
                break;
            }
        }
        
        return lastFoundClothesBox;
    }

    function removeAllSelectedItemFromClothesBox(clothesBox) {
        let allSelectedItem = clothesBox.querySelectorAll('.selected');

        for (let item of allSelectedItem) {
            item.classList.remove('selected');
        }
    }

    async function loadClothesChildren(parent_id) {
        const url = `http://127.0.0.1:5000/api/v1/clothes/?parent_id=${parent_id}`;
        const response = await fetch(url, {
            method: 'GET'
        });

        if (!response.ok) {
            alert(response.status + ' ' + response.statusText);
            return;
        }

        return await response.json();
    };
</script>

<div class='clothes-box'>
    <h1>{clothes.name}</h1>
    <hr>
    <div class='clothes-box__container'>
        <div on:click={clothesItemClickHandler} class='clothes-box__container__item' data-id={clothes.id} data-is-major-item="true">
            <div class='img-wrapper'>
                <img src={clothes.image_path} alt={clothes.name}>
            </div>
            <span>Будь-які</span>
        </div>

        {#each clothes.children as children}
            <div on:click={clothesItemClickHandler} class='clothes-box__container__item' data-id={children.id}>
                <div class='img-wrapper'>
                    <img src={children.image_path} alt={children.name}>
                </div>
                <span>{children.name}</span>
            </div>
        {/each}
    </div>
</div>

<style>
    :global(.clothes-box) {
        margin-top: 40px;
        padding: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
    }

    :global(.clothes-box .clothes-box) {
        margin-top: 10px;
    }

    :global(.clothes-box hr) {
        border: none;
        color: rgb(212, 212, 212);
        background-color: rgb(212, 212, 212);
        height: 1px;
        margin-top: 10px;
    }

    :global(.clothes-box h1) {
        font-weight: 400;
        font-size: 1.8rem;
    }

    :global(.clothes-box h2) {
        font-weight: 400;
        font-size: 1.25rem;
    }

    :global(.clothes-box__container) {
        display: flex;
        flex-wrap: wrap;
    }

    :global(.clothes-box__container__item) {
        width: 120px;
        margin-top: 25px;
        cursor: pointer;
    }

    :global(.clothes-box__container__item .img-wrapper img) {
        width: 100%;
        height: 135px;
        transition: 0.1s all;
    }

    :global(.clothes-box__container__item span) {
        display: block;
        text-align: center;
        font-size: 0.8rem;
        margin-top: 5px;
        padding: 10px 0;
        transition: 0.3s all;
        line-height: 0.9rem;
    }

    :global(.clothes-box__container__item:hover .img-wrapper img) {
        transform: scale(1.07);
        transition: 0.1s all;
    }

    :global(.clothes-box__container__item:hover span) {
        transition: 0.3s all;
        background-color: rgb(241, 241, 241);
    }

    :global(.clothes-box__container__item.selected .img-wrapper) {
        position: relative;
    }

    :global(.clothes-box__container__item.selected .img-wrapper::after) {
        content: '';
        position: absolute;
        bottom: 0px;
        right: 0px;
        width: 40px;
        height: 40px;
        background: center no-repeat url('../images/selected.png');
        background-size: 40px 40px;
    }
</style>