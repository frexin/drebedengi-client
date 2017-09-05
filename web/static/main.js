class Form {

    constructor(url, rcid) {
        this.base_url = url;
        this.items = [];
        this.rcid = rcid;
    }

    init() {
        let xhr = new XMLHttpRequest();
        let url = this.base_url  + '/get?receipt_id=' + this.rcid;

        xhr.open('GET', url, true);
        xhr.send();

        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                let response = xhr.responseText;
                this.items = JSON.parse(response);

                this.render_fields()
            }
        }.bind(this)
    }

    render_fields() {
        let form_row = $('div.template').clone().removeClass('d-none');

        for (let i in this.items) {
            let item = this.items[i];

            $('input[name=pattern]', form_row).val(item['name']);
            $('input[name=id]', form_row).val(item['id']);

            $('.rows').append(form_row);
        }

        $('.cat_select').select2();
    }

    serialize() {
        let data = [];

        $('.rows .form-row').each(function() {
            let row = {
                'pattern' : $('input[name=pattern]', this).val(),
                'id' : $('input[name=id]', this).val(),
                'cat_id' : $('select', this).val(),
            };

            data.push(row);
        });

        data.shift();

        return data;
    }

    send_data(data, callback) {
        let url = this.base_url + '/update';

        $.ajax(url, {
            'data' : JSON.stringify(data),
            'type' : 'POST',
            'processData' : false,
            'contentType' : 'application/json',
            'success' : callback
        })
    }
}