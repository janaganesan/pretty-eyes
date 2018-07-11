String.prototype.format = function() {
  var str = this;
  for (var i = 0; i < arguments.length; i++) {
    var reg = new RegExp("\\{" + i + "\\}", "gm");
    str = str.replace(reg, arguments[i]);
  }
  return str;
};

function fetch_filters() {
    $.ajax({
        type: 'GET',
        url: '/filters',
        data: $(this).serialize(),
        dataType: 'json',
        success: function (data) {
            $.each(data.filters, function (key, value) {
                add_row(key, value);
                alert(key + value);
            });
        }
    });
    //if($('.filter-row').length === 0) {add_row();}
}

function add_row(text1, text2) {
    if(!text1) {text1='';}
    if(!text2) {text2='';}
    var row_id = 0;
    if($('.filter-row').length > 0) {
        row_id = parseInt($('.filter-row').last().attr('id').split('_')[1]) + 1;
    }
    var filter_row = $('<div id="row_{0}" class="filter-row"></div>'.format(row_id));
    $(filter_row).append($('<input class="form-input" value="{0}"></input><input class="form-input" value="{1}"></input>'.format(text1, text2)));
    $(filter_row).append($('<img id="rm_{0}" class="remove-icon" />'.format(row_id)));
    $(filter_row).appendTo($('#container'));
}

$(document).ready( function () {
    fetch_filters();
    $(".filter-form").on("click", "#add-row", function(event) {
        add_row();
    });
    $(".filter-form").on("click", ".remove-icon", function(event) {
        row_id = $(event.target).attr('id').split('_')[1];
        $("#row_" + row_id).remove();
    });
} );