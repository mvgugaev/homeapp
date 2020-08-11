BASE = {
    csrftoken: '',
    logout: function() {
        $('#logout').on('click', function(e) {
            $.ajax({
                url : "/user/api/logout/",
                type: "GET",
                contentType: "application/json; charset=utf-8",
                headers: {
                    "X-CSRFToken": BASE.csrftoken
                },
                success : function (data) {
                    window.location.href = '/user/login/';
                },
                error: function (data, exception) {
                    alertify.message('Ошибка выхода');
                },
            });
        })
    },
    init: function() {
        this.logout();
    }
}
