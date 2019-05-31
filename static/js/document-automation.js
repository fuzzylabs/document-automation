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
            timeout: 30000,
            success: function(response) {
                if (response != 0) {
                    console.log(response);

                    var classification = $.parseJSON(response).classification[0].class;
                    $("#classification").removeClass();
                    $("#classification").addClass("text-success");
                    $("#classification").text(classification);
                } else {
                    var result = "Upload failed";
                    $("#classification").removeClass();
                    $("#classification").addClass("text-failure");
                    $("#classification").text(classification);
                    console.log("Error uploading file");
                }
            },
        });
    });
});
