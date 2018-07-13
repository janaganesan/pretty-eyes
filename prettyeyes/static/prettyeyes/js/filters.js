String.prototype.format = function() {
  var str = this;
  for (var i = 0; i < arguments.length; i++) {
    var reg = new RegExp("\\{" + i + "\\}", "gm");
    str = str.replace(reg, arguments[i]);
  }
  return str;
};

function add_row(text1, text2) {
    if(!text1) {text1='';}
    if(!text2) {text2='';}
    var filter_row = $('' +
        '<div class="input-group">' +
        '<input type="text" class="form-control m-md-2" name="key" value="{0}" placeholder="Field name"></input>'.format(text1) +
        '<input type="text" class="form-control m-md-2" name="value" value="{0}" placeholder="Value"></input>'.format(text2) +
        '<span><div class="remove-icon" /></span>' +
        '</div>');
    $(filter_row).appendTo($('#filter-content'));
}

function fetch_filters() {
    $('#filter-content').empty();
    $.ajax({
        type: 'GET',
        url: '/filters',
        data: $(this).serialize(),
        dataType: 'json',
        success: function (data) {
            $.each(data.filters, function (key, value) {
                add_row(key, value);
            });
        }
    });
}

$(document).ready( function () {
    $('#filtermodal').on('show.bs.modal', function() {
       fetch_filters();
    });
    $(".modal-body").on("click", ".add-icon", function(event) {
        add_row();
    });
    $("#filter-content").on("click", ".remove-icon", function(event) {
        $(this).parents('.input-group').fadeOut().remove();
    });
    $(".filter-form").on("click", "#form-submit", function(e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/filters/",
            data: $('form.filter-form').serialize(),
            success: function(response) {
                $("#filtermodal").modal('hide');
            },
            error: function() {
                alert('Error');
            }
        });
        return false;
    });
} );