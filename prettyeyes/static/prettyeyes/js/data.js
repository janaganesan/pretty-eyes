var interval = 3000;
function fetch_orders() {
    $.ajax({
        type: 'GET',
        url: '/orders',
        data: $(this).serialize(),
        dataType: 'json',
        success: function (data) {
            $.each(data, function (key, value) {
                var list = $('<ul></ul>');
                $('#order_list').empty();
                $('#order_list').append(list);
                $.each(value, function (index, order) {
                    list.append('<li>' + order.order_id + '</li>');
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