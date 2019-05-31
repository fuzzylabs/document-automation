$(document).ready(function() {
    $(":file").filestyle();

    var ctx = $("#canvas")[0].getContext("2d");

    $("#filepath").change(function() {
        var file = $("#filepath")[0].files[0];
        var objUrl = URL.createObjectURL(file);
        var img = new Image();
        img.src = objUrl;
        img.onload = function() {
            ctx.drawImage(img, 0, 0, 900, 1165);
            URL.revokeObjectURL(img.src);
        };
    });

    $("#upload").click(function() {
        var files = $("#filepath")[0].files[0];

        $("#paragraphs").empty();
        $("#classification").removeClass();
        $("#classification").addClass("text-muted");
        $("#classification").text("Processing");

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
                    var json = $.parseJSON(response);

                    var classification = json.classification[0].class;
                    $("#classification").addClass("text-success");
                    $("#classification").text(classification);

                    json.paragraphs.paragraphs.forEach(function(paragraph) {
                        ctx.moveTo(paragraph.boundingBox[0].x, paragraph.boundingBox[0].y);
                        ctx.lineTo(paragraph.boundingBox[1].x, paragraph.boundingBox[1].y);
                        ctx.lineTo(paragraph.boundingBox[2].x, paragraph.boundingBox[2].y);
                        ctx.lineTo(paragraph.boundingBox[3].x, paragraph.boundingBox[3].y);
                        ctx.lineTo(paragraph.boundingBox[0].x, paragraph.boundingBox[0].y);

                        $("#paragraphs").append("<p>" + paragraph.text + "</p>");
                    });

                    ctx.strokeStyle = "red";
                    ctx.stroke();
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
