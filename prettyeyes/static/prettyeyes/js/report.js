var interval = 3000;

String.prototype.format = function() {
  var str = this;
  for (var i = 0; i < arguments.length; i++) {
    var reg = new RegExp("\\{" + i + "\\}", "gm");
    str = str.replace(reg, arguments[i]);
  }
  return str;
};


function report_history() {
    $.ajax({
        type: 'GET',
        url: window.location.pathname + 'reportjson/',
        data: $(this).serialize(),
        dataType: 'json',
        success: function (data) {
            $.each(data, function (key, value) {
                $.each(value, function (index, report) {
                    var report_class = $('<div id="table_{0}"></div>'.format(report.pk));
                    if($("#table_" + report.pk).length == 0) {
                        $(report_class).append('<table id="report-history"><th>{0}</th><tr><td>{1}</td></tr></table><br/>'.format(report.name, report.report));
                        $('#report_container').append(report_class);
                    }
                });
            });
        },
        complete: function (data) {
                // Schedule the next
                setTimeout(report_history, interval);
        }
    });
}

$(document).ready( function () {
    report_history();
} );