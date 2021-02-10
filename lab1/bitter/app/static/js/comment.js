let btns = $('.comment');
let posts = $('.post-card');
const URL = 'comment';
const ADD_COMMENT_OK = '<div class="alert alert-success" role="alert">Commented!</div>';
const ADD_COMMENT_ERR = '<div class="alert alert-danger" role="alert">Error</div>';

$(document).ready(function(){
    load_all_comments()
    btns.on('click', function(e){
        e.preventDefault();
        post_comment($(this));
    });
    $('#test_form').on('submit', function(e){
        e.preventDefault();
        console.log(e);
    })
})

function post_comment(btn) {
    let post_id = btn.attr('id').split('_')[1];
    let item_id = '#comment_post_' + post_id;
    let comment = $(item_id);        
    if (comment.val().length > 0) {
        $.ajax({
            type: 'POST',
            url: URL,
            data: JSON.stringify({body: comment.val(), post_id: post_id}),
            contentType: 'application/json;charset=UTF-8'
        }).done(function(){
            btn.after(ADD_COMMENT_OK);
            load_comments();
            comment.val('');
        }).fail(function(){
            btn.after(ADD_COMMENT_ERR);
            load_comments();
            comment.val('')
        });
    }
};


function load_all_comments(){
    $.each(posts, function(index, post){
        let post_id = $(post).attr('id').split('_')[1];
        load_comments(post_id);
    })
}


function load_comments(post_id){
    let url = 'post_comments/' + post_id;
    $.ajax({
        type: 'GET',
        url: url,
        contentType: 'application/json;charset=UTF-8'
    }).done(function(response){
        $.each(response, function(index, comment){
            render_comment(comment, post_id);
        })
    }).fail(function(response){
        // show error
    });
};

function render_comment(comment, post_id){
    let html = '<div class="card text-white bg-secondary mb-3" style="max-width: 18rem;">';
    html += '<div class="card-header">' + comment.username + ' ' + comment.pub_date + '</div>';
    html += '<div class="card-body">';
    html += '<p class="card-text">' + comment.body + '</p></div></div>';
    let post_dom_id = '#postid_' + post_id;    
    $(post_dom_id).append(html);
}
