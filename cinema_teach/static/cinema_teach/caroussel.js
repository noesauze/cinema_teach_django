// caroussel

$(document).ready(function () {
    // Variables
    var carrousel = $('.carrousel');
    var modal = $('#image-modal');
    var modalImage = $('#modal-image');

    // Fonction pour afficher l'image en grand
    function displayImageInModal(imageSrc) {
        modalImage.attr('src', imageSrc);
        modal.css('display', 'block');
    }

    // Fermer la modal
    $('.close').click(function () {
        modal.css('display', 'none');
    });

    // Gérer le clic sur une image du carrousel
    carrousel.on('click', '.carrousel-item', function () {
        var imageSrc = $(this).attr('src');
        displayImageInModal(imageSrc);
    });
});
