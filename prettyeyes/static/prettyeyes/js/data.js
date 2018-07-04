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
                $.each(value, function (index, order) {
                    if ($("#order_" + order.pk).length == 0) {
                        var order_menu = $('<div id="order_{0}"></div>'.format(order.pk));
                        $(order_menu).append('<img class="slider plus-icon"></img><a class="order-link" href="/orders/{0}" target="frame_data">{1}</a>'.format(order.pk, order.order_id));
                        $(order_menu).prependTo($("#order_list"))
                    }
                    if ($("#reportmenu_" + order.pk).length == 0) {
                        $("#order_" + order.pk).append($('<div id="reportmenu_{0}" class="sub-menu"></div>'.format(order.pk)));
                        $("#reportmenu_" + order.pk).hide()
                    }
                    $.each(order.reports, function (index, report) {
                        if($("#report_" + report.pk).length == 0) {
                            $("#reportmenu_" + order.pk).append($('<a id="report_{0}" href="/report/{1}" target="frame_data">{2}</a>'.format(report.pk, report.pk, report.name)));
                        }
                    });
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
    $("#order_list").on("click", '*[id^="order_"]', function(event) {
        if ($(event.target).attr('class') === "order-link") {
            $(this).find(".sub-menu").fadeIn(500);
            $(this).find(".plus-icon").addClass("minus-icon").removeClass("plus-icon");
        }
    });
    $("#order_list").on("click", ".slider", function(event) {
        $(this).siblings('.sub-menu').toggle();
        if ($(this).siblings('.sub-menu').is(":visible")) {
            $(this).addClass("minus-icon").removeClass("plus-icon");
        } else {
            $(this).addClass("plus-icon").removeClass("minus-icon");
        }
    });
} );