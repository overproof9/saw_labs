$(document).ready(function(){
    const SET_ROLE_OK = '<div class="alert alert-success" role="alert">Success!</div>';
    const SET_ROLE_ERR = '<div class="alert alert-danger" role="alert">Error</div>';
    let url = "/user_role"
    let btns = $('.role_btn');
    btns.on('click', function(e) {
        e.preventDefault();
        update_role($(this));
    })

    function update_role(btn){
        
        let user_id = $(btn).attr('id').split('_')[2];
        let select_string = '#select_role_' + user_id.toString(10);
        let select = $(select_string);
        let new_role = select.val();

        $.ajax({
            type: 'POST',
            url: url,
            data: JSON.stringify({user_id: user_id, new_role: new_role}),
            contentType: 'application/json;charset=UTF-8'
        }).done(function(){
            btn.after(SET_ROLE_OK);
        }).fail(function(){
            btn.after(SET_ROLE_ERR);
        });
    }
});