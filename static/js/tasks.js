TASKS = {
    csrftoken: '',
    workflow_id: '',
    list: {
        list_block: undefined,
        list_errors_block: undefined,
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
        set_errors: function(data) {
            TASKS.list.list_errors_block.html(TASKS.list.error_list_create(data));
        },
        create_list: function(data) {
            let list_content = '';

            data.forEach(function(element) {
                list_content += `
                    <div class="card card-task">
                        <div class="progress">
                            <div class="progress-bar bg-danger" role="progressbar" style="width: 75%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100">
                            </div>
                        </div>
                        <div class="card-body">
                            <div class="card-title">
                                <a href="#">
                                    <h6 data-filter-by="text" class="H6-filter-by-text">${element.name}</h6>
                                </a>
                                <span class="text-small">${element.created_at}</span>
                            </div>
                        </div>
                    </div>
                `;
            });

            return list_content
        },
        render_list: function(data) {
            let content_list = TASKS.list.create_list(data);

            $('#workflow_list').html(content_list);
        },
        load_data: function(data_callback, error_callback) {
            $.ajax({
                url : "/tasks/api/" + TASKS.workflow_id,
                type: "GET",
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                headers: {
                    "X-CSRFToken": TASKS.csrftoken
                },
                success : function (data) {
                    data_callback(data['tasks']);
                },
                error: function (data, exception) {
                    error_callback(data.responseJSON)
                },
            });
        },
        update_list: function() {
            this.load_data(this.render_list, this.set_errors);
        },
        init: function(workflow_id) {
            
            TASKS.workflow_id = workflow_id;

            this.list_block = $('#tasks_list');
            this.list_errors_block = $('#load_list_errors');

            this.update_list();
        }
    }
}