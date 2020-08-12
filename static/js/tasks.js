TASKS = {
    csrftoken: '',
    workflow_id: '',
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
    render_dot_loading: function() {
        let content = `
            <div class="form_button_loading">
                <span class="one">.</span>
                <span class="two">.</span>
                <span class="three">.</span>
            </div>
        `;

        return content;
    },
    create: {
        form_instance: undefined,
        form_error_block: undefined,
        required_fields: ['name', 'description', 'mode', 'workflow_id', 'last_date', 'cycle'],
        block_form: function() {
            this.form_instance.find('button[type="submit"]').html(TASKS.render_dot_loading());
            this.form_instance.css({'pointer-events': 'none'});
            this.form_instance.find('.modal-header.close').css({'opacity': 0.6});
            this.form_instance.find('.nav-tabs').css({'opacity': 0.6});
            this.form_instance.find('.modal-body').css({'opacity': 0.6});
        },
        unblock_form: function() {
            this.form_instance.find('button[type="submit"]').html('Создать задачу');
            this.form_instance.css({'pointer-events': 'auto'});
            this.form_instance.find('.modal-header.close').css({'opacity': 1});
            this.form_instance.find('.nav-tabs').css({'opacity': 1});
            this.form_instance.find('.modal-body').css({'opacity': 1});
        },
        get_data: function() {
            let data = {
                'users': []
            };
            let that = this;

            this.required_fields.forEach(function(field) {
                data[field] = that.form_instance.find('[name="' + field + '"]').val();
            });

            this.form_instance.find('input[name="user_check"]').each(function() {
                if($(this).prop('checked')) {
                    data['users'].push({
                        'id': $(this).attr('value')
                    });
                }
            });

            return data;
        },
        create_task: function() {
            let that = this;
            let request_data = {
                'type': 'create',
                'task': this.get_data()
            }

            $.ajax({
                url : "/tasks/api/",
                type: "POST",
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                data: JSON.stringify(request_data),
                headers: {
                    "X-CSRFToken": TASKS.csrftoken
                },
                success : function (data) {
                    that.unblock_form();
                    that.form_instance.modal('hide');
                    TASKS.list.update_list();
                },
                error: function (data, exception) {
                    that.unblock_form();
                    that.form_error_block.html(TASKS.error_list_create(data.responseJSON));
                },
            });
        },
        init: function() {
            this.form_instance = $('#task-add-modal');
            this.form_error_block = $('#add_task_form_errors');

            let that = this;

            // this.form_instance.find('[name="mode"]').select2();
            $(".flatpickr-input").flatpickr({
                enableTime: true,
                dateFormat: "d.m.Y H:i",
                defaultDate: [new Date()]
            });

            sortable('.form-group-users', {forcePlaceholderSize: true});

            this.form_instance.on('submit', function(e) {
                e.preventDefault();
                that.block_form();

                try {
                    that.create_task();
                }
                catch (e) {

                    let error_data = {
                        'error': 'Ошибка в процессе создания задачи'
                    }

                    that.form_error_block.html(TASKS.error_list_create(error_data));
                    that.unblock_form();
                }
            });


        }
    },
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
        block_task: function(element) {
            element.css({'pointer-events': 'none', 'opacity': 0.8});
        },
        unblock_task: function(element) {
            element.css({'pointer-events': 'auto', 'opacity': 1});
        },
        set_task_events: function(element) {

            let that = this;

            element.find('.exec_task').on('click', function(e) {
                  e.preventDefault();
                  let parent_element = $(this).closest('.card-task');
                  let task_id = $(this).attr('data-id');

                  that.exec_task(task_id, parent_element);  
            });

            element.find('.change_task_status').on('click', function(e) {
                e.preventDefault();
                let parent_element = $(this).closest('.card-task');
                let task_id = $(this).attr('data-id');
                let status_code = $(this).attr('data-status');
                let status = status_code != '0';

                that.change_status(task_id, status, parent_element);  
            });

            element.find('.delete_task').on('click', function(e) {
                e.preventDefault();
                let parent_element = $(this).closest('.card-task');
                let task_id = $(this).attr('data-id');

                Swal.fire({
                    title: 'Удалить задачу?',
                    text: "История задачи будет удалена без возможности восстановления!",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'Удалить',
                    cancelButtonText: 'Отменить'
                  }).then((result) => {
                    if (result.value) {
                        that.delete(task_id, parent_element);
                    }
                  }); 
            });
        },
        set_tasks_events: function() {

            let that = this;

            this.list_block.find('.card-task').each(function() {
                console.log('asdasd');
                that.set_task_events($(this));
            });
        },
        render_task_element: function(task_id, element) {
            this.block_task(element);
            let that = this;
            
            $.ajax({
                url : "/tasks/api/" + task_id,
                type: "GET",
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                headers: {
                    "X-CSRFToken": TASKS.csrftoken
                },
                success : function (data) {

                    let task_data = data['tasks'][0];
                    let task_element = $(that.render_list_element(task_data));

                    $(element).replaceWith(task_element);
                    that.set_task_events(task_element);
                    that.unblock_task(task_element);
                },
                error: function (data, exception) {
                    that.unblock_task(element);
                    that.list_errors_block.html(TASKS.error_list_create(data.responseJSON));
                },
            });

        },
        change_status: function(task_id, status, element) {
            this.block_task(element);

            let that = this;
            let request_data = {
                'type': 'change_status',
                'task': {
                    'id': task_id,
                    'status': status
                }
            }

            $.ajax({
                url : "/tasks/api/",
                type: "POST",
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                data: JSON.stringify(request_data),
                headers: {
                    "X-CSRFToken": TASKS.csrftoken
                },
                success : function (data) {
                    that.unblock_task(element);
                    that.update_list();
                },
                error: function (data, exception) {
                    that.unblock_task(element);
                    that.list_errors_block.html(TASKS.error_list_create(data.responseJSON));
                },
            });
        },
        delete: function(task_id, element) {
            this.block_task(element);

            let that = this;
            let request_data = {
                'type': 'delete',
                'task': {
                    'id': task_id,
                }
            }

            $.ajax({
                url : "/tasks/api/",
                type: "POST",
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                data: JSON.stringify(request_data),
                headers: {
                    "X-CSRFToken": TASKS.csrftoken
                },
                success : function (data) {
                    that.unblock_task(element);
                    that.update_list();
                },
                error: function (data, exception) {
                    that.unblock_task(element);
                    that.list_errors_block.html(TASKS.error_list_create(data.responseJSON));
                },
            });
        },
        exec_task: function(task_id, element) {

            this.block_task(element);

            let that = this;
            let request_data = {
                'type': 'exec',
                'task': {
                    'id': task_id
                }
            }

            $.ajax({
                url : "/tasks/api/",
                type: "POST",
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                data: JSON.stringify(request_data),
                headers: {
                    "X-CSRFToken": TASKS.csrftoken
                },
                success : function (data) {
                    that.unblock_task(element);
                    that.render_task_element(task_id, element);
                },
                error: function (data, exception) {
                    that.unblock_task(element);
                    that.list_errors_block.html(TASKS.error_list_create(data.responseJSON));
                },
            });
        },
        render_list_element: function(data) {

            let user_list = '';
            let task_type_text = {
                '0': 'Разовая',
                '1': 'Повтор',
                '2': 'Повтор по времени',
                '3': 'Повтор по порядку',
                '4': 'Повтор по порядку и времени'
            }

            data.users.forEach(function(user) {
                user_list += `
                    <li style="${data.executor ? `${data.executor.id == user.id ? ``: `opacity:0.4;`}` : ``}">
                        <a href="#" data-toggle="tooltip" title="" data-original-title="${user.email}">
                          <img alt="${user.username}" class="avatar" src="${user.avatar_url}">
                        </a>
                    </li>
                    `;
            });

            let list_element_content = `
                <div class="card card-task">
                    <div class="card-body">
                        <div class="card-title">
                            <a href="#">
                                <h6 data-filter-by="text" class="H6-filter-by-text">${data.name}</h6>
                            </a>
                            <span class="text-small">${task_type_text[data.mode]}</span>
                        </div>
                        <div class="card-meta">
                        ${data.mode == '4' && !data.compleated ? `
                        <div class="d-flex align-items-center mr-2" style="${data.to_retry_count_day <= 2 ? 'color:red;' : 'opacity:0.4;'}">
                            <span>Осталось: ${data.to_retry_count_day} дней(я) </span>
                        </div>` : ``}
                        ${data.compleated ? `
                            <div class="d-flex align-items-center mr-2">
                                <i class="material-icons">playlist_add_check</i>
                                <span>Выполнена</span>
                            </div>` : ``}
                        <ul class="avatars">
                            ${user_list}
                        </ul>
                        <div class="dropdown card-options">
                            <button class="btn-options" type="button" id="task-dropdown-button-1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            <i class="material-icons">more_vert</i>
                            </button>
                            <div class="dropdown-menu dropdown-menu-right" x-placement="bottom-end" style="position: absolute; transform: translate3d(-132px, 24px, 0px); top: 0px; left: 0px; will-change: transform;">
                                <a class="dropdown-item exec_task text-success" href="#" data-id="${data.id}" style="${data.compleated ? 'opacity:0.4; pointer-events:none;': ''}">Выполнить</a>
                                <div class="dropdown-divider">
                                </div>
                                <a class="dropdown-item change_task_status text-info" data-id="${data.id}" data-status="${data.closed ? '0': '1'}" href="#">${data.closed ? 'Открыть': 'Закрыть'}</a>
                                <div class="dropdown-divider">
                                </div>
                                <a class="dropdown-item delete_task text-danger" data-id="${data.id}" href="#">Удалить</a>
                            </div>
                        </div>
                        </div>
                    </div>
                </div>
            `;

            return list_element_content;
        },
        create_list: function(data) {
            let list_content = '';
            let that = this;

            data.forEach(function(element) {
                list_content += that.render_list_element(element);
            });

            return list_content
        },
        render_list: function(data) {
            let content_list = TASKS.list.create_list(data);

            $('#tasks_list').html(content_list);
            this.set_tasks_events();
        },
        set_stat: function(stat_data) {
            $('#tasks_progress').css({'width': stat_data['progress'] + '%'});
            $('#tasks_progress_count').html(stat_data['compleated'] + '/' + stat_data['opened']);
        },
        load_data: function() {
            let that = this;
            $.ajax({
                url : "/tasks/api/?workflow_id=" + TASKS.workflow_id,
                type: "GET",
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                headers: {
                    "X-CSRFToken": TASKS.csrftoken
                },
                success : function (data) {
                    that.render_list(data['tasks']);
                    that.set_stat(data['stat']);
                    that.unblock_list();
                },
                error: function (data, exception) {
                    that.set_errors(data.responseJSON);
                    that.unblock_list();
                },
            });
        },
        block_list: function() {
            this.list_block.css({'pointer-events': 'none', 'opacity': 0.8});
        },
        unblock_list: function() {
            this.list_block.css({'pointer-events': 'auto', 'opacity': 1});
        },
        update_list: function() {
            let that = this;
            this.block_list();

            try {
                this.load_data();
            }
            catch (e) {

                let error_data = {
                    'error': 'Ошибка в процессе создания задачи'
                }

                that.list_errors_block.html(TASKS.error_list_create(error_data));
                that.unblock_list();
            }
        },
        init: function(workflow_id) {
            
            TASKS.workflow_id = workflow_id;

            this.list_block = $('#tasks_list');
            this.list_errors_block = $('#load_list_errors');

            this.update_list();
        }
    }
}