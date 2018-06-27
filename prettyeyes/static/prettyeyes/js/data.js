var interval = 3000;

String.prototype.format = function() {
  var str = this;
  for (var i = 0; i < arguments.length; i++) {
    var reg = new RegExp("\\{" + i + "\\}", "gm");
    str = str.replace(reg, arguments[i]);
  }
  return str;
};

function fetch_orders() {
    $.ajax({
        type: 'GET',
        url: '/orders',
        data: $(this).serialize(),
        dataType: 'json',
        success: function (data) {
            $.each(data, function (key, value) {
                $('#order_list').empty();
                $.each(value, function (index, order) {
                    $('#order_list').append('<a href="/orders/{0}">{1}</a>'.format(order.pk, order.order_id));
                });
            });
        },
        complete: function (data) {
                // Schedule the next
                setTimeout(fetch_orders, interval);
        }
    });
}

$(document).ready( function () {
    fetch_orders();
    //$.getJSON('/orders', function(data) {
    //    $.each(data, function (key, value) {
    //        var list = $('<ul></ul>');
    //        $('body').append(list);
    //        $.each(value, function (index, order) {
    //            list.append('<li>' + order.order_id + '</li>');
    //        });
    //    });
    //});
} );