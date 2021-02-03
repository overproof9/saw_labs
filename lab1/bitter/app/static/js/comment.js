$(document).ready(function(){
    let btns = $('.comment');
    let url = 'comment';
    let add_comment_ok = '<div class="alert alert-success" role="alert">Commented!</div>';
    let add_comment_err = '<div class="alert alert-danger" role="alert">Error</div>';
    btns.on('click', function(e){
        e.preventDefault();
        let btn = $(this);
        let post_id = btn.attr('id').split('_')[1];
        let item_id = '#comment_post_' + post_id;
        let comment = $(item_id);
        let data = JSON.stringify({body: comment.val(), post_id: post_id});
        console.log(data)
        
        if (comment.val().length > 0) {
            $.ajax({
                type: 'POST',
                url: url,
                data: JSON.stringify({body: comment.val(), post_id: post_id}),
                contentType: 'application/json;charset=UTF-8'
            }).done(function(){
                btn.after(add_comment_ok);
                console.log('add comment success')
                comment.val('');
            }).fail(function(){
                btn.after(add_comment_err);
                console.log('add comment bad')
                comment.val('')
            });
        }
    });
})