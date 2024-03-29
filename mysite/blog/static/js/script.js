$(document).ready(function () {
    $('.like-button').click(function (event) {
        event.preventDefault();

        var postId = $(this).data('post-id');
        var reactChoice = $(this).data('choice');
        var csrfToken = Cookies.get('csrftoken');

        $.ajax({
            url: '/' + postId + '/' + reactChoice + '/reaction/',
            type: 'POST',
            data: {'post_id': postId, 'choice': reactChoice},
            headers: {'X-CSRFToken': csrfToken},
            success: function (data) {
                if (data.redirect_url) {
                    window.location.href = data.redirect_url;
                } else {
                    $('#like-element-text-' + postId).text(data.likes_count);
                    $('#dislike-element-text-' + postId).text(data.dislikes_count);
                }
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
    });


    $(".share-button").click( function(event) {
        event.preventDefault();
        var postId = $(this).data('post-id')
        var dialogId = 'list-dialog-' + postId
        $('#' + dialogId).dialog({
            modal: true,
            width: 600,
            height: 240,
        });

        var clipboard = new ClipboardJS('#copyButton-' + postId, {
            target: function(trigger) {
                return $('#postUrl-' + postId).get(0);
            }
        });

    });

    $('.subscribe-button').click(function (event) {
        event.preventDefault();

        var postId = $(this).data('post-id');
        var csrfToken = Cookies.get('csrftoken');
        var formData = $('#subscription-email-field').val();

        $.ajax({
            url: '/' + postId + '/subscription/',
            crossOrigin: true,
            type: 'POST',
            dataType: 'json',
            data: {'post_id': postId, 'email': formData,},
            headers: {'X-CSRFToken': csrfToken},
            success: function (data) {
                console.log('Success');
                var successMessage = $('<p class="text-center" id="subscription-message">Subscription successfully activated&#9989;</p>');
                $('#subscription-form-wrapper').replaceWith(successMessage);
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
    });

});
