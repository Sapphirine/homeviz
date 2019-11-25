// HomeViz Javascript
// Set dimensions of map
var margin = {top: 10, bottom: 10, left: 10, right:10},
    width = parseInt(d3.select('.viz').style('width')) - margin.left - margin.right,
    mapRatio = 0.5,
    height = width * mapRatio,
    active = d3.select(null);

// Create SVG object for map
var svg = d3.select('.viz').append('svg')
  .attr('class', 'center-container')
  .attr('height', height + margin.top + margin.bottom)
  .attr('width', width + margin.left + margin.right);

// Create rect container for map
svg.append('rect')
  .attr('class', 'background center-container')
  .attr('height', height + margin.top + margin.bottom)
  .attr('width', width + margin.left + margin.right)
  .on('click', clicked);

// Create tooltip 
var tooltip = d3.select("body").append("div") 
  .attr("class", "tooltip")       
  .style("opacity", 0);

// Update location of inds
var dropdown = d3.select("#dropdown")
  .style("top", 100 + "px")
  .style("left", width * 0.8 + "px");

// Load counties data
d3.json('https://cdn.jsdelivr.net/npm/us-atlas@3/counties-10m.json').then(DrawMap);

// Set projection
var projection = d3.geoAlbersUsa()
    .translate([width /2 , height / 2])
    .scale(width/1.2);

// Resize path 
var path = d3.geoPath().projection(projection);

// Create container for states
var g = svg.append("g")
    .attr('class', 'center-container center-items us-state')
    .attr('transform', 'translate('+margin.left+','+margin.top+')')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)

// Function to draw map
function DrawMap(us) {
	console.log(us);
			
	data = data_all['state_all']
	data_label = "Median Home Price: "
	data1 = data_all['county_all']
       		
	var lowColor = '#98f692'//'#f9f9f9'
	var highColor = '#bc2a66'//'#bc2a66'
	var keys = Object.keys(data);
	var norm = 0.8;
	var minVal = Math.min.apply(null, keys.map(function(x) { return data[x]} ));
	var maxVal = Math.max.apply(null, keys.map(function(x) { return data[x]} ));
	var ramp = d3.scaleLinear().domain([minVal,maxVal*norm]).range([lowColor,highColor])

	// add a legend
	var w = width/10, h = height/2;
	var key = d3.select("g")
		.append("svg")
		.attr("width", w)
		.attr("height", h)
		.attr("class", "legend");
	var legend = key.append("defs")
		.append("svg:linearGradient")
		.attr("id", "gradient")
		.attr("x1", "100%")
		.attr("y1", "0%")
		.attr("x2", "100%")
		.attr("y2", "100%")
		.attr("spreadMethod", "pad");
	legend.append("stop")
		.attr("offset", "0%")
		.attr("stop-color", highColor)
		.attr("stop-opacity", 1);
	legend.append("stop")
		.attr("offset", "100%")
		.attr("stop-color", lowColor)
		.attr("stop-opacity", 1);
	key.append("rect")
		.attr("width", w/4)
		.attr("height", h)
		.style("fill", "url(#gradient)")
		.attr("transform", "translate(0,10)");
	var y = d3.scaleLinear()
		.range([h, 0])
		.domain([minVal, maxVal]);
	var yAxis = d3.axisRight(y);
	key.append("g")
		.attr("class", "y axis")
		.attr("transform", "translate(" + w/3.5 + "," + 10 + ")")
		.call(yAxis)

  // Draw counties
	g.append("g")
        .attr("id", "counties")
        .selectAll("path")
        .data(topojson.feature(us, us.objects.counties).features)
        .enter().append("path")
        .attr("d", path)
        .attr("class", "county-boundary")
        .style("fill", function(d){return ramp(data1[d.id])})
        .on("click", reset)
        .on("mouseover", function(d){
        	tooltip.transition()
        	.duration(900)
        	.style("opacity", 0.8);
        	tooltip.html(d.properties.name + "<br/>" + data_label + data1[d.id]) 
        	.style("left", (d3.event.pageX) + "px")
        	.style("top", (d3.event.pageY - 28) + "px");
        })
        .on("mouseout", function(d){
        	tooltip.transition()
        	.duration(500)
        	.style("opacity", 0);
        });

  // Draw states
  g.append("g")
      .attr("id", "states")
      .selectAll("path")
      .data(topojson.feature(us, us.objects.states).features)
      .enter().append("path")
      .attr("d", path)
      .attr("class", "state")
      // .style("fill", function(d){return ramp(data[d.properties.name])})
      .on("click", clicked)
      .on("mouseover", function(d){
      	tooltip.transition()
      	.duration(900)
      	.style("opacity", 0.8);
      	tooltip.html(d.properties.name + "<br/>" + data_label + data[d.properties.name])
      	.style("left", (d3.event.pageX) + "px")
      	.style("top", (d3.event.pageY - 28) + "px");
      })
      .on("mouseout", function(d){
      	tooltip.transition()
      	.duration(500)
      	.style("opacity", 0);
      });
  
  // Fill states with colors                     
  g.selectAll(".state").transition()
  	.style("fill", function(d){return ramp(data[d.properties.name])})
  	.duration(2000);

  // Draw state borders
  g.append("path")
      .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; }))
      .attr("id", "state-borders")
      .attr("d", path);

  var picklist = ['all', '1bed', '2bed', '3bed', '4bed', '5bed', 'sqft'];
  var caption = ['Median Home Price: ', '1Bed Home Price: ', '2Bed Home Price: ', '3Bed Home Price: ', 
                '4Bed Home Price: ', '5Bed+ Home Price: ', 'Home Price by Sqft: '];

  var display = {};
  for (i = 0; i < picklist.length; i++){
    display[picklist[i]] = caption[i]
  };
  console.log(display)

  // Update map if ind is changed
	d3.select("#dropdown")
		.on("change", function(){
			var selection = document.getElementById("dropdown")
			var selected = selection.options[selection.selectedIndex].value

      data = data_all["state_" + selected]
      data1 = data_all["county_" + selected]
      data_label = display[selected]

    	keys = Object.keys(data)
    	minVal = Math.min.apply(null, keys.map(function(x) { return data[x]} ))
    	maxVal = Math.max.apply(null, keys.map(function(x) { return data[x]} ))
    	ramp = d3.scaleLinear().domain([minVal,maxVal*norm]).range([lowColor,highColor])				
      UpdateMap(data, data1)
  });

  // Add cities to map
  // d3.csv("{% static "1000-largest-us-cities.csv" %}").then(function(cities){
  d3.csv("static/1000-largest-us-cities.csv").then(function(cities){
  	console.log(cities)
  	g.selectAll("circle")
  		.data(cities)
  		.enter()
  		.append('circle')
  		.attr("transform", function(d){
  			return 'translate('+ projection([d.longitude, d.latitude])+')';
  		})
  		.attr("class", "city")
  		.attr("r", function(d){
  			return Math.sqrt(parseInt(d.Population) * 0.00004);
  		})
  		.style("fill", "yellow")
  		.style("stroke", "gray")
  		.style("stroke-width", 0.25)
  		.style("opacity", 0.5)
  		.append("title")
  		.text(function(d){
  			return d.name + "\nPopulation: " + d.Population;
  		});
  });

  // Function to update map when ind is changed
  function UpdateMap(data, data1) {
    g.selectAll(".county-boundary").transition()
    	.style("fill", function(d){return ramp(data1[d.id])})
    	.duration(1000);

    g.selectAll(".state").transition()
        .style("fill", function(d){return ramp(data[d.properties.name])})
        .duration(1000);
                     
    // update legend
    y = d3.scaleLinear()
      .range([h, 0])
      .domain([minVal, maxVal]);
    yAxis = d3.axisRight(y);
    key.select("g")
      .call(yAxis)
  }
}

function clicked(d) {
    if (d3.select('.background').node() === this) return reset();

    if (active.node() === this) return reset();

    active.classed("active", false);
    active = d3.select(this).classed("active", true);

    var bounds = path.bounds(d),
        dx = bounds[1][0] - bounds[0][0],
        dy = bounds[1][1] - bounds[0][1],
        x = (bounds[0][0] + bounds[1][0]) / 2,
        y = (bounds[0][1] + bounds[1][1]) / 2,
        scale = .9 / Math.max(dx / width, dy / height),
        translate = [width / 2 - scale * x, height / 2 - scale * y];

    g.transition()
        .duration(500)
        .style("stroke-width", 1.5 / scale + "px")
        .attr("transform", "translate(" + translate + ")scale(" + scale + ")");

    g.selectAll(".city")
    	.style("fill", "black")
    	.style("stroke-width", 0.1)
    	.attr("r", 5 / scale);
}


function reset() {
    active.classed("active", false);
    active = d3.select(null);

    g.transition()
        // .delay(100)
        .duration(500)
        .style("stroke-width", "1.5px")
        .attr('transform', 'translate('+margin.left+','+margin.top+')');

    g.selectAll(".city")
    	.style("fill", "yellow")
    	.style("stroke-width", 0.25)
    	.attr("r", function(d){
			return Math.sqrt(parseInt(d.Population) * 0.00004);
		})

}
