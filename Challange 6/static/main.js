function jsonToMap(json) {
    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext('2d');

    for (var i = 0; i < json.stars.length; i++)
    {
        console.log(json.stars[i].name);
        star = json.stars[i];

        ctx.fillStyle = "rgb(200,0,0)";
        ctx.fillRect(star.x, star.y, 4, 4)
    };
}