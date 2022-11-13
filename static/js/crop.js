const imgInput = document.getElementById('id_profile_pic');
const modal = document.getElementById('pyl-cropper-modal-background');
// image.src = url;



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
        minCropBoxWidth: 200,
        minCropBoxHeight: 200,
        });
    okButton.addEventListener('click', () => {
        cropper.getCroppedCanvas().toBlob((blob) => {
            let fileInput = document.getElementById('id_profile_pic');
            let file = new File([blob], imgInput.files[0].name, {type:"image/*", lastModified: new Date().getTime()});
            let container = new DataTransfer();
            container.items.add(file);
            fileInput.files = container.files;
            // destroy the cropper and close modal
            cropper.destroy();
            modal.style.display = 'none';

        });
    });
    cancelButton.addEventListener('click', () => {
        cropper.destroy();
        modal.style.display = 'none';
        imgInput.value = '';
    })
});
