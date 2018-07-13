var interval = 1000;

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
                    var order_container = $("#order_" + order.pk);
                    var reports_menu = $("#reportmenu_" + order.pk);
                    if (order_container.length == 0) {
                        var order_menu = $('<div id="order_{0}"></div>'.format(order.pk));
                        $(order_menu).append('<img class="slider plus-icon"></img><a class="order-link" href="/orders/{0}" target="frame_data">{1}</a>'.format(order.pk, order.order_id));
                        $(order_menu).prependTo($("#order_list"))
                    }
                    if (reports_menu.length == 0) {
                        order_container.append($('<div id="reportmenu_{0}" class="sub-menu pl-md-2"></div>'.format(order.pk)));
                         $("#reportmenu_" + order.pk).hide()
                    }
                    $.each(order.reports, function (index, report) {
                        if($("#report_" + report.pk).length == 0) {
                            var report_menu = $('' +
                                '<div class="form-check">' +
                                '<input type="checkbox" class="form-check-input mt-2" id="cb_{0}">'.format(report.pk) +
                                '<a id="report_{0}" href="/report/{1}" target="frame_data">{2}</a>'.format(report.pk, report.pk, report.name) +
                                '</div>'
                            );
                            reports_menu.append(report_menu);
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

function diff_table(data) {
    $("#compare-report").empty();
    $("#compare-report").append('<th>{0}</th><th>{1}</th>'.format(data.name1, data.name2));
    for(var i = 0; i < Object.keys(data["col1"]).length; i++) {
        var row = $('<tr></tr>');
        $('<td class="{0}">{1}</td>'.format(data.col1[i].class, data.col1[i].content)).appendTo(row);
        $('<td class="{0}">{1}</td>'.format(data.col2[i].class, data.col2[i].content)).appendTo(row);
        $("#compare-report").append(row);
    }
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
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
    $("#order_list").on("change", '*[id^="cb_"]', function(event) {
        if($('*[id^="cb_"]:checked').length == 2) {
            $("#btn-compare").prop('disabled', false);
        } else {
            $("#btn-compare").prop('disabled', true);
        }
    });
    $(document).on("click", '#btn-compare', function(event) {
        var report_ids = [];
        $('*[id^="cb_"]:checked').each(function() {
            report_ids.push($(this).attr('id').split('_')[1]);
        });
        $.ajaxSetup({
            beforeSend: function(xhr, settings) { xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken')); }
        });
        $.ajax({
            type: "POST",
            url: "/diffreport/",
            data: {left: report_ids[0], right: report_ids[1]},
            //beforeSend: function(xhr){xhr.setRequestHeader('X-CSRFToken', "{{csrf_token}}");},
            success: function(data) {
                diff_table(data);
            },
            error: function() {
                alert('Error');
            }
        });
    });
} );