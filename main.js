var svg = d3.select("svg");
// var path = d3.geoPath();
var data = [3, 17, 2, 146, 5]

// define function to scale points
var scaleLinearly = d3.scale.linear()
                    .domain()

// select container element
d3.select(".chart")
    // initiate the data join. Defining the selection to which we will join data.
    // so even though no divs may exist underneath the chart node, we have defined the type of element we will be adding by instantiating this selector
    .selectAll("div")
    // join the data array defined above to our selector. 
    .data(data)
    // the enter selection represents all the data with no corresponding DOM element in the selection
    // in our case, this is all of them
    .enter()
    // appends a new DOM element of the specified type for each new bound data point
    // IMPORTANT - this returns a new selection containing the appended elements
    // since this is all of the elements we want to manipulate, we can just continue chaining methods afterwards
    .append("div")
    // the style selector applies the specified style attribute which is the first parameter
    // it also takes a function of (d) or even (d,i) as the second parameter, in which d is the data point (and i is the index of the data point)
    // each iteration of the function must return a string which will be the value for that attribute
    .style("width", function (d) { return d * 10 + "px"; })
    // another selector
    .text(function (d) { return d; })
    .style("background-color", "blue")
    .style("color", "white")






// d3.selectAll("p")
//     .data([2, 4, 16, 24])
//     .transition()
//     .duration(750)
//     .delay(function (d, i) { return i * 10; })
//     .style("font-size", function (d) { return d + "px" });

// d3.json("https://unpkg.com/us-atlas@1/us/10m.json", function (error, us) {
//     if (error) throw error;

//     svg.append("path")
//         .attr("stroke-width", 0.5)
//         .attr("d", path(topojson.mesh(us, us.objects.states, function (a, b) { return a !== b; })));

//     svg.append("path")
//         .attr("d", path(topojson.feature(us, us.objects.nation)));

//     svg.append("circle")
//         .attr()
// });