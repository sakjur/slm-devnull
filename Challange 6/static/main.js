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

function awesomeToMap(awesome, shipson) {
    ctx.fillStyle = "rgb(200, 100, 0)";
    ctx.fillRect(100,100,10,10);

    console.log(awesome)

    for (var i = 0; i < awesome.system.planetarray.length; i++)
    {
        planet = awesome.system.planetarray[i];

        ctx.fillStyle = "rgb(0,200,0)";
        ctx.fillRect(planet.x, planet.y, 4, 4);

        $("#planetlist").append("<div id=\"s" + i + "\">" + planet.planet_no + "</div>");
    };
    
    $("#planetlist").append("<div id=\"edge\">Edge</div>");

    $("#planetlist div").on('click', function () {
        id = $(this).attr('id');
        id = id.replace("s", "")
        if (id == "edge")
        {
            planet = "edge"
            console.log("Going to FTL-space")
        }
        else
        {
            planet = awesome.system.planetarray[id].planet_no
            planet = planet.replace(" ", "%20")

            $("#planetinfo").html(JSON.stringify(awesome.system.planetarray[id]));
        }
        $.ajax("/current/flyto/" + planet);
    });

    ctx.fillStyle = "rgb(0,0,200)";
    ctx.fillRect(shipson.systemx, shipson.systemy, 4, 4);

    setInterval(
        function() {
            $.ajax("https://lostinspace.lanemarknad.se:8000/api2/?session=f6319047-1cfb-4bfa-ae4b-318355d2b90e&command=ship&arg=show")
             .done(function ( data )
                { 
                    data = $.parseJSON(data)
                    ctx.clearRect(0,0,200,200)
                    ctx.fillStyle = "rgb(200, 100, 0)";
                    ctx.fillRect(100,100,10,10);

                    for (var i = 0; i < awesome.system.planetarray.length; i++)
                    {
                        planet = awesome.system.planetarray[i];

                        ctx.fillStyle = "rgb(0,200,0)";
                        ctx.fillRect(planet.x, planet.y, 4, 4);
                    };

                    ctx.fillStyle = "rgb(0,0,200)";
                    ctx.fillRect(data.systemx, data.systemy, 4, 4);
                    });
        }, 1000)
}