$(document).ready(function () {
    $('.like-button').click(function (event) {
        event.preventDefault();

        var postId = $(this).data('post-id');
        var csrfToken = Cookies.get('csrftoken');

        $.ajax({
            url: '/' + postId + '/like/',
            type: 'POST',
            data: {'post_id': postId},
            headers: {'X-CSRFToken': csrfToken},
            success: function (data) {
                if (data.redirect_url) {
                    window.location.href = data.redirect_url;
                } else {
                    $(event.target).closest('.like-elements').find('.like-text').text(data.likes_count);
                }
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
    });

    $('.dislike-button').click(function (event) {
        event.preventDefault();

        var postId = $(this).data('post-id');
        var csrfToken = Cookies.get('csrftoken');

        $.ajax({
            url: '/' + postId + '/dislike/',
            type: 'POST',
            data: {'post_id': postId},
            headers: {'X-CSRFToken': csrfToken},
            success: function (data) {
                if (data.redirect_url) {
                    window.location.href = data.redirect_url;
                } else {
                    $(event.target).closest('.like-elements').find('.dislike-text').text(data.dislikes_count);
                }
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
    });

});
