let nextDom = document.getElementById('next');
let prevDom = document.getElementById('prev');
let sliderDom = document.querySelector('.slider');
let listItemDom = document.querySelector('.slider .list');
let thumbnailDom = document.querySelector('.slider .thumbnail');

nextDom.onclick = function () {
    showSlider('next');
};

prevDom.onclick = function () {
    showSlider('prev');
};

const timeRunning = 3000;
let runTimeOut;

function showSlider(type) {
    const itemSlider = document.querySelectorAll('.slider .list .item');
    const itemThumbnail = document.querySelectorAll('.slider .thumbnail .item');

    if (type === 'next') {
        listItemDom.appendChild(itemSlider[0]);
        thumbnailDom.appendChild(itemThumbnail[0]);
        sliderDom.classList.add('next');
    } else {
        const positionLastItem = itemSlider.length - 1;
        listItemDom.insertBefore(itemSlider[positionLastItem], listItemDom.firstChild);
        thumbnailDom.insertBefore(itemThumbnail[positionLastItem], thumbnailDom.firstChild);
        sliderDom.classList.add('prev');
    }

    clearTimeout(runTimeOut);
    runTimeOut = setTimeout(() => {
        sliderDom.classList.remove('next');
        sliderDom.classList.remove('prev');
    }, timeRunning);
}