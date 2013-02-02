var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');

function jsonToMap(json, shipson) {

    console.log(json)

    for (var i = 0; i < json.length; i++)
    {
        star = json[i];

        ctx.fillStyle = "rgb(200,0,0)";
        ctx.fillRect(star.x, star.y, 4, 4);

        $("#starlist").append("<a href=\"/" + star.name + "\">" + star.name + "</a><br />");
    };

    ctx.fillStyle = "rgb(0,0,200)"
    ctx.fillRect(shipson.unix, shipson.uniy, 4, 4)

    setInterval(
        function() {
            $.ajax("https://lostinspace.lanemarknad.se:8000/api2/?session=f6319047-1cfb-4bfa-ae4b-318355d2b90e&command=ship&arg=show")
             .done(function ( data )
                { 
                    data = $.parseJSON(data)
                    ctx.clearRect(0,0,200,200)

                    for (var i = 0; i < json.length; i++)
                    {
                        star = json[i];

                        ctx.fillStyle = "rgb(200,0,0)";
                        ctx.fillRect(star.x, star.y, 4, 4);
                    };

                    ctx.fillStyle = "rgb(0,0,200)";
                    ctx.fillRect(data.unix, data.uniy, 4, 4);
                    });
        }, 1000)

}

function awesomeToMap(awesome, shipson) {
    ctx.fillStyle = "rgb(200, 100, 0)";
    ctx.fillRect(100,100,10,10);

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
            $.ajax("/current/flyto/edge");
        }
        else
        {
            inpplanet = awesome.system.planetarray[id]
            planet = inpplanet.planet_no.replace(" ", "%20")

            $("#planetinfo").html( 
                function()
                {
                    fixedPlan = inpplanet.planet_no.replace("'", "%27")
                    output = "<div id='q" + id + "' onClick='$.ajax(\"/current/flyto/" + fixedPlan + "\")'>Goto</div>"
                    output += "<h3>" + inpplanet.planet_no + "</h3>";
                    output += "Day: " + inpplanet.day + "<br />";
                    output += "Esc velocity: " + inpplanet.esc_velocity + "<br />";
                    output += "Cloud cover: " + inpplanet.cloud_cover + "<br />";
                    output += "Radius: " + inpplanet.radius + "<br />";
                    output += "Type: " + inpplanet["type"] + "<br />";
                    output += "Planet #: " + inpplanet.planet_no + "<br />";
                    output += "Planet coords: (" + inpplanet.x + ", " + inpplanet.y + ")<br />";
                    output += "Surface gravity: " + inpplanet.surf_grav + "<br />";
                    output += "Orbit zone: " + inpplanet.orbit_zone + "<br />";
                    output += "<iframe src=\"/planetinfo/" + inpplanet.planet_no + "\"></iframe>"
                    

                    return output
                }
            );
        }
    });

    ctx.fillStyle = "rgb(0,0,200)";
    ctx.fillRect(shipson.systemx, shipson.systemy, 4, 4);

    setInterval(
        function() {
            $.ajax("/scanplanet/");

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