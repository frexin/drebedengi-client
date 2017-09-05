class Form {

    constructor(url) {
        this.base_url = url;
        this.items = [];
    }

    init() {
        let xhr = new XMLHttpRequest();

        xhr.open('GET', this.base_url, true);
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
        let form_row = $('div.template').clone().removeClass('hide');

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
                'name' : $('input[name=pattern]', this).val(),
                'id' : $('input[name=id]', this).val(),
                'cat_id' : $('select', this).val(),
            };

            data.push(row);
        });

        data.shift();

        return data;
    }
}