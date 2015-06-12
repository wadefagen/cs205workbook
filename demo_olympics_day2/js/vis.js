
// d3 world map code from http://techslides.com/d3-map-starter-kit

function main() {
    $.getJSON("res/goldMedals.json", function (jsonData) {

var graticule = d3.geo.graticule();
var width = document.getElementById('container').offsetWidth;
var height = width / 2;

var topo,projection,path,svg,g;


projection = d3.geo.mercator()
               .translate([(width/2), (height/2)])
			   .scale( width / 2 / Math.PI);

path = d3.geo.path().projection(projection);

svg = d3.select("#container").append("svg")
        .attr("width", width)
		.attr("height", height)
		.append("g");

g = svg.append("g");

d3.json("js/world-topo-min.json", function(error, world) {
	var countries = topojson.feature(world, world.objects.countries).features;
	topo = countries;
	draw(topo);
});

var color = d3.interpolateHsl("white", "red");
var max = 552;


function draw(topo) {
  svg.append("path")
     .datum(graticule)
     .attr("class", "graticule")
     .attr("d", path);

  g.append("path")
   .datum({type: "LineString", coordinates: [[-180, 0], [-90, 0], [0, 0], [90, 0], [180, 0]]})
   .attr("class", "equator")
   .attr("d", path);

  var country = g.selectAll(".country").data(topo);
  country.enter().insert("path")
      .attr("class", "country")
      .attr("d", path)
      .attr("id", function(d, i) { return d.id; })
      .attr("title", function(d, i) { return d.properties.name; })
      .style("fill", function(d, i) {
        var country = d.properties.name;
      	return color( Math.log10(jsonData[country]) / Math.log10(max) );
      });
 }

	
		
    }).fail(function (d) { alert("Failed to load JSON!"); });                              
}
