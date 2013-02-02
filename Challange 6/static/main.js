var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');

function jsonToMap(json, shipson) {

    for (var i = 0; i < json.stars.length; i++)
    {
        star = json.stars[i];

        ctx.fillStyle = "rgb(200,0,0)";
        ctx.fillRect(star.x, star.y, 4, 4);

        $("#starlist").append("<a href=\"/" + star.name + "\">" + star.name + "</a><br />");
    };

    ctx.fillStyle = "rgb(0,0,200)"
    ctx.fillRect(shipson.unix, shipson.uniy, 4, 4)

    setTimeout(location.reload,3000)

}

function awesomeToMap(awesome) {
    ctx.fillStyle = "rgb(200, 100, 0)";
    ctx.fillRect(100,100,10,10);

    for (var i = 0; i < json.awesome.length; i++)
    {
        planet = json.awesome[i];

        ctx.fillStyle = "rgb(200,0,0)";
        ctx.fillRect(planet.x, planet.y, 4, 4);

        $("#starlist").append("<a href=\"/" + star.name + "\">" + star.name + "</a><br />");
    };
    
    ctx.fillStyle = "rgb(0,0,200)"
    ctx.fillRect(shipson.unix, shipson.uniy, 4, 4)
}