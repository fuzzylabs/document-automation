$(document).ready(function() {
    $(":file").filestyle();

    $("#filepath").change(function() {
        var file = $("#filepath")[0].files[0];
        $("#document").attr("src", window.URL.createObjectURL(file));
    });

    $("#upload").click(function() {
        var files = $("#filepath")[0].files[0];

        $.ajax({
            url: "/classify",
            type: "POST",
            data: files,
            contentType: "application/octet-stream",
            processData: false,
            success: function(response) {
                if (response != 0) {
                    console.log(response);
                } else {
                    console.log("Error uploading file");
                }
            },
        });
    });
});
