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
                $('#report_container').empty();
                $.each(value, function (index, report) {
                    $('#report_container').append('<div><table id="table-blue"><th>{0}</th><tr><td>{1}</td></tr></table></div><br/>'.format(report.name, report.report));
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