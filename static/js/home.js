// HomeViz Javascript
// By: Enoch Shum

function home(data_all, hist_all){
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

    // Add dropbox
    var categories = {"all": "All", "1bed": "1 Bedroom", "2bed": "2 Bedrooms", 
                    "3bed": "3 Bedrooms", "4bed": "4 Bedrooms", "5bedOrMore": "5 Bedrooms+",
                    "medianPerSqft": "Median Per Sqft", "singleFamily": "Single Family", 
                    "condo": "Condos/Co-op", "topTier": "Top Tier", "bottomTier": "Bottom Tier"};
    categories = d3.entries(categories)

    var menu = d3.select("#menu")
        .append("select")
        .attr("id", "dropdown")
        .attr("class", "select-style")
        .selectAll("option")
        .data(categories)
        .enter().append("option")
        .attr("value", function(d){
          return d.key;
        })
        .text(function(d){
          return d.value;
        });

    d3.select("#dropdown")
        .style("top", 100 + "px")
        .style("left", width * 0.8 + "px");

    // Load counties data
    Promise.resolve(d3.json('https://cdn.jsdelivr.net/npm/us-atlas@3/counties-10m.json')).then(DrawMap);

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
        hist = hist_all['state_all']
        hist1 = hist_all['county_all']
        // console.log(hist)
             		
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
                d3.select(this).style('fill-opacity', 0.7);
              	tooltip.transition()
                  	.duration(900)
                  	.style("opacity", 1);
                tooltip.html(d.properties.name + "<br/>" + data_label + data1[d.id]) 
                  	.style("left", (d3.event.pageX) + "px")
                  	.style("top", (d3.event.pageY - 28) + "px");
                line_plot(hist1[d.id])
            })
            .on("mouseout", function(d){
                d3.select(this).style('fill-opacity', 1);
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
                d3.select(this).style('fill-opacity', 0.7);
              	tooltip.transition()
                  	.duration(900)
                  	.style("opacity", 0.8);
                tooltip.html("State: " + d.properties.name + "<br/>" + data_label + data[d.properties.name])
                  	.style("left", (d3.event.pageX + 30) + "px")
                  	.style("top", (d3.event.pageY - 28) + "px");
                line_plot(hist[d.properties.name])
            })
            .on("mouseout", function(d){
                d3.select(this).style('fill-opacity', 1);
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

        var picklist = ['all', '1bed', '2bed', '3bed', '4bed', '5bedOrMore', 'medianPerSqft', 'singleFamily', 
                        'condo', 'topTier', 'bottomTier'];
        var caption = ['Median Home Price: ', '1Bed Home Price: ', '2Bed Home Price: ', '3Bed Home Price: ', 
                      '4Bed Home Price: ', '5Bed+ Home Price: ', 'Home Price Per Sqft: ', 'Single Family Home Price: ',
                      'Condo/Co-op Home Price: ', 'Top Tier Home Price: ', 'Bottom Tier Home Price: '];

        var display = {};
        for (i = 0; i < picklist.length; i++){
            display[picklist[i]] = caption[i]
        };
        console.log(display)

        // Update map if dropdown menu is changed
      	d3.select("#dropdown")
        		.on("change", function(){
          			var selection = document.getElementById("dropdown")
          			var selected = selection.options[selection.selectedIndex].value

                data = data_all["state_" + selected]
                data1 = data_all["county_" + selected]
                data_label = display[selected]
                hist = hist_all["state_" + selected]
                hist1 = hist_all["county_" + selected]

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

    //Update scale (zoom to counties) when clicked
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
          	.attr("r", 2 / scale);
    }

    //Reset map when clicked again
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

    //Historical data of a single state as input
    function line_plot(hist){
        // set the dimensions and margins of the graph
        var margin = {top: 10, right: 40, bottom: 20, left: 50},
            width = 200 - margin.left - margin.right,
            height = 80 - margin.top - margin.bottom;

        // append the svg object to the body of the page
        var svg = d3.select(".tooltip")
          .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
          .append("g")
            .attr("transform",
                  "translate(" + margin.left + "," + margin.top + ")");

        //Read the data
        hist = d3.entries(hist, function(d){
            return { date : d3.timeParse("%Y_%m")(d.key.slice(1,8)), value : d.value }
        })
            // Add X axis --> it is a date format
        // console.log(hist)
        var x = d3.scaleTime()
          .domain(d3.extent(hist, function(d) { return d3.timeParse("%Y_%m")(d.key.slice(1,8)); }))
          .range([ 0, width ]);
        svg.append("g")
          .style("font", "8px sans-serif")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x).ticks(4));

        // Add Y axis
        var y = d3.scaleLinear()
          .domain([0, d3.max(hist, function(d) { return +d.value; })])
          .range([ height, 0 ]);
        svg.append("g")
          .style("font", "8px sans-serif")
          .call(d3.axisLeft(y).ticks(3));

        // Add the line
        svg.append("path")
          .datum(hist)
          .attr("id", "line")
          .attr("fill", "none")
          .attr("stroke", "steelblue")
          // .attr("stroke-width", 4)
          .attr("d", d3.line()
            .x(function(d) { return x(d3.timeParse("%Y_%m")(d.key.slice(1,8))) })
            .y(function(d) { return y(d.value) })
          )
        
        // Add some animation
        d3.selectAll("#line").style("opacity","0");
        d3.selectAll("#line").style("opacity","1");
        var totalLength = d3.select("#line").node().getTotalLength();
        d3.selectAll("#line")
          .attr("stroke-dasharray", totalLength + " " + totalLength)
          .attr("stroke-dashoffset", totalLength)
          .transition()
              .duration(1000)
              .attr("stroke-dashoffset", 0)
              .style("stroke-width",3)

        }


    // function line_plot_bottom(hist){
    //     // set the dimensions and margins of the graph
    //     var margin = {top: 10, right: 30, bottom: 30, left: 60},
    //         width = 200 - margin.left - margin.right,
    //         height = 70 - margin.top - margin.bottom;

    //     // append the svg object to the body of the page
    //     var svg = d3.select(".viz")
    //       .append("svg")
    //         .attr("width", width + margin.left + margin.right)
    //         .attr("height", height + margin.top + margin.bottom)
    //       .append("g")
    //         .attr("transform",
    //               "translate(" + margin.left + "," + margin.top + ")");

    //     //Read the data
    //     hist_data = hist['Washington']
    //     data = d3.entries(hist_data, function(d){
    //         return { date : d3.timeParse("%Y_%m")(d.key.slice(1,8)), value : d.value }
    //     })
    //         // Add X axis --> it is a date format
    //     console.log(data)
    //     var x = d3.scaleTime()
    //       .domain(d3.extent(data, function(d) { return d3.timeParse("%Y_%m")(d.key.slice(1,8)); }))
    //       .range([ 0, width ]);
    //     svg.append("g")
    //       .style("font", "8px sans-serif")
    //       .attr("transform", "translate(0," + height + ")")
    //       .call(d3.axisBottom(x).ticks(4));

    //     // Add Y axis
    //     var y = d3.scaleLinear()
    //       .domain([0, d3.max(data, function(d) { return +d.value; })])
    //       .range([ height, 0 ]);
    //     svg.append("g")
    //       .style("font", "8px sans-serif")
    //       .call(d3.axisLeft(y).ticks(3));

    //     // Add the line
    //     svg.append("path")
    //       .datum(data)
    //       .attr("id", "line")
    //       .attr("fill", "none")
    //       .attr("stroke", "steelblue")
    //       // .attr("stroke-width", 4)
    //       .attr("d", d3.line()
    //         .x(function(d) { return x(d3.timeParse("%Y_%m")(d.key.slice(1,8))) })
    //         .y(function(d) { return y(d.value) })
    //       )
        
    //     // Add some animation
    //     d3.selectAll("#line").style("opacity","0");
    //     d3.selectAll("#line").style("opacity","1");
    //     var totalLength = d3.select("#line").node().getTotalLength();
    //     d3.selectAll("#line")
    //       .attr("stroke-dasharray", totalLength + " " + totalLength)
    //       .attr("stroke-dashoffset", totalLength)
    //       .transition()
    //           .duration(2000)
    //           .attr("stroke-dashoffset", 0)
    //           .style("stroke-width",3)

    //     }
}