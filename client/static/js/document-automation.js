$(document).ready(function() {
    $(":file").filestyle();

    var ctx = $("#canvas")[0].getContext("2d");
    var canvasWidth = 900;
    var canvasHeight = 1274;

    $("#filepath").change(function() {
        var file = $("#filepath")[0].files[0];
        var objUrl = URL.createObjectURL(file);
        var img = new Image();
        img.src = objUrl;
        img.onload = function() {
            ctx.clearRect(0, 0, canvasWidth, canvasHeight);
            ctx.drawImage(img, 0, 0, canvasWidth, canvasHeight);
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

                    //var classification = json.classification[0].class;
                    //$("#classification").addClass("text-success");
                    //$("#classification").text(classification);
                    $("#classification").addClass("text-success");
                    $("#classification").text("...");

                    var xcoeff = canvasWidth / json.width;
                    var ycoeff = canvasHeight / json.height;

                    json.paragraphs.paragraphs.forEach(function(paragraph) {
                        ctx.beginPath();
                        ctx.strokeStyle = "red";
                        ctx.moveTo(paragraph.boundingBox[0].x * xcoeff, paragraph.boundingBox[0].y * ycoeff);
                        ctx.lineTo(paragraph.boundingBox[1].x * xcoeff, paragraph.boundingBox[1].y * ycoeff);
                        ctx.lineTo(paragraph.boundingBox[2].x * xcoeff, paragraph.boundingBox[2].y * ycoeff);
                        ctx.lineTo(paragraph.boundingBox[3].x * xcoeff, paragraph.boundingBox[3].y * ycoeff);
                        ctx.lineTo(paragraph.boundingBox[0].x * xcoeff, paragraph.boundingBox[0].y * ycoeff);
                        ctx.closePath();
                        ctx.stroke();
                    });

                    Object.entries(json.entities).forEach(function([key, value]) {
                        $("#paragraphs").append("<p><b>" + key + "</b>");
                        value.forEach(function(n) {
                            $("#paragraphs").append(n.name + ", ");
                        });
                        $("#paragraphs").append("</p>");
                    });
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
