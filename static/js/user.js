USER = {
    error_list_create: function(data) {
        let error_html = '';

        for (const [key, value] of Object.entries(data)) {
            error_html += `
                <div class="alert alert-danger" role="alert">
                    ${value}
                </div>
            `;
        }

        return error_html;

    },
    login: {
        login_form: undefined,
        login_from_error_block: undefined,
        required_fields: ['email', 'password'],
        init: function() {
            this.login_form = $('#login_form');
            this.login_from_error_block = this.login_form.find('#login_form_errors');

            let that = this;

            this.login_form.on('submit', function(e) {
                e.preventDefault();

                let request_data = {};

                that.required_fields.forEach(function(field) {
                    console.log(field);
                    console.log(that.login_form.find('[name="' + field + '"]').val());
                    request_data[field] = that.login_form.find('[name="' + field + '"]').val();
                });

                $.ajax({
                    url : "/user/api/login/",
                    type: "POST",
                    contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    data: JSON.stringify(request_data),
                    headers: {
                        "X-CSRFToken": that.login_form.find('[name="csrfmiddlewaretoken"]').val()
                    },
                    success : function (data) {
                        window.location.replace('/');
                    },
                    error: function (data, exception) {
                        that.login_from_error_block.html(USER.error_list_create(data.responseJSON));
                    },
                });
            });
        }
    }
}