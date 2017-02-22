$(document).ready(function () {
    var ipver = $("#ip-version").text();
    if (ipver == "IPv4") {
        $("#legacy-ip-modal").modal();
    }
});