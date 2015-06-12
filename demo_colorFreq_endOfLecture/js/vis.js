

			   
function main() {
    $.getJSON("res/freq.json",
        function (jsonData) {
        	// Add the image
        	document.getElementById("img").innerHTML =
        		'<img src="' + jsonData.file + '" class="img-responsive" />';

			// Add the graph
			var freq = jsonData.freq;
			
			var data = _.map(
			   freq,
			   function(value, key) {
			      return { color: key,
			               count: value };
			   }
			);
			
			data = _.first(data, 10);
//			alert( JSON.stringify(data) );
			
			d3.select("#freq")
			  .selectAll("div")
			  .data(data)
			  .enter()
			  .append("div")
			  .style("text-align", "right")
			  .style("width", function (d) { return d.count * 10 + "px";})
			 // .style("height", "5px")
			  .style("background-color", function (d) { return d.color; })
			  .text( function(d) { return d.count; } );
			  		
			
			
        })
        .fail(function (d) { alert("Failed to load JSON!"); })
    ;                              
}
