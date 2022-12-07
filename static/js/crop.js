const imgInput = document.getElementById('id_profile_pic');
const modal = document.getElementById('pyl-cropper-modal-background');
const changeImg = document.getElementById('profile_pic-id-image');
const changeImgOvr = document.getElementById('profile_pic-ovr-id');
const fileSize = document.getElementById('file-size');
// const changeImg = document.querySelectorAll('.multi-select');



imgInput.addEventListener('change', () => {
    // new Promise()
    modal.style.display = 'block';
    // modal.style = "display:flex; justify-content:center; align-items:center; align-content:center";
    const url = URL.createObjectURL(imgInput.files[0]);
    const imageDiv = document.querySelector('.image-container');
    // console.log(url)
    imageDiv.innerHTML = `<img src=${url} id="image" alt="#">`;
    const image = document.getElementById('image');
    const okButton = document.getElementById('crop-image-ok');
    const cancelButton = document.getElementById('crop-image-cancel');

    const cropper = new Cropper(image, {
        aspectRatio: 1 / 1,
        autoCropArea: 1,
        viewMode: 1,
        scalable: false,
        zoomable: false,
        movable: false,
        minCropBoxWidth: 50,
        minCropBoxHeight: 50,
        });
    okButton.addEventListener('click', () => {
        cropper.getCroppedCanvas().toBlob((blob) => {
            let fileInput = document.getElementById('id_profile_pic');
            let file = new File([blob], imgInput.files[0].name, {type:"image/*", lastModified: new Date().getTime()});
            let sizeMB = Number((file.size / 1048576).toFixed(2));
            fileSize.innerHTML = (file.size < 1048576) ? `Cropped image size: <span class="bold-big">${sizeMB}</span> MB` : 
            `Cropped image size: <span class="bold-big red-underline">${sizeMB}</span> MB<br><span class="red-underline">Max file size is 1.0 MB !</span>`;
            let container = new DataTransfer();
            container.items.add(file);
            fileInput.files = container.files;
            changeImg.src = URL.createObjectURL(blob)
            // destroy the cropper and close modal
            cropper.destroy();
            modal.style.display = 'none';

        }, 'image/jpeg'); // this line from: https://github.com/fengyuanchen/cropperjs/issues/853#issuecomment-877184909 (issues with file size)
    });
    cancelButton.addEventListener('click', () => {
        cropper.destroy();
        modal.style.display = 'none';
        imgInput.value = '';
    })
});

changeImg.addEventListener('click', () => imgInput.click());
changeImgOvr.addEventListener('click', () => imgInput.click());
// changeImg.forEach(elem => addEventListener('click', () => imgInput.click()));
