$(document).ready(function() {
    $("#entities-title").hide();
    $("#text").hide();
    $(":file").filestyle();

    var ctx = $("#canvas")[0].getContext("2d");
    var canvasWidth = 600;
    var canvasHeight = 849;

    $("#filepath").change(function() {
        var file = $("#filepath")[0].files[0];
        var objUrl = URL.createObjectURL(file);
        var img = new Image();
        img.src = objUrl;
        img.onload = function() {
            ctx.clearRect(0, 0, canvasWidth, canvasHeight);

            // A little hack to get around images that have EXIF rotation due to phone orientation
            if (img.width > img.height) {
                ctx.translate(canvasWidth / 2, canvasHeight / 2);
                ctx.rotate(90 * Math.PI / 180);
                ctx.translate(-canvasHeight / 2, -canvasWidth / 2);
                ctx.drawImage(img, 0, 0, canvasHeight, canvasWidth);
                ctx.setTransform(1, 0, 0, 1, 0, 0);
            } else {
                ctx.drawImage(img, 0, 0, canvasWidth, canvasHeight);
            }
            URL.revokeObjectURL(img.src);
        };
    });

    $("#upload").click(function() {
        var files = $("#filepath")[0].files[0];

        $("#postcode").empty();
        $("#entities-title").hide();
        $("#text").hide();
        $("#entities").empty();
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
                    $("#classification").text("Document");
                    $("#text").text(json.text);

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

                    $("#entities-title").show();
                    $("#text").show();
                    Object.entries(json.entities).forEach(function([key, value]) {
                        $("#entities").append("<p><b>" + key + "</b>");
                        value.forEach(function(n) {
                            $("#entities").append(n.value + ", ");

                            n.metadata.forEach(function(meta) {
                                if (meta.postal_code != null) {
                                    $("#postcode").append("<b>Postcode</b> " + meta.postal_code);
                                }
                            });
                        });
                        $("#entities").append("</p>");
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
