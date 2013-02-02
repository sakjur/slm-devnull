function jsonToMap(json, shipson) {
    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext('2d');

    for (var i = 0; i < json.stars.length; i++)
    {
        star = json.stars[i];

        ctx.fillStyle = "rgb(200,0,0)";
        ctx.fillRect(star.x, star.y, 4, 4);

        $("#starlist").append("<a href=\"/" + star.name + "\">" + star.name + "</a><br />");
    };

    console.log (shipson);
    ctx.fillStyle = "rgb(0,0,200)"
    ctx.fillRect(shipson.unix, shipson.uniy, 4, 4)

    setTimeout(location.reload,3000)

}