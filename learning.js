// var path = d3.geoPath();
var data = [3, 17, 2, 146, 5]

// define function to scale points
var scaleLinearly = d3.scaleLinear()
    .domain([0, d3.max(data)])
    .range([0, 420])

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
    .style("width", function (d) { return scaleLinearly(d) + "px"; })
    // another selector
    .text(function (d) { return d; })
    .style("background-color", "blue")
    .style("color", "white");

// now with SVG
var barHeight = 20;
// select svg element
var svgChart = d3.select('.svgchart')
    // specify height and width of svg element.
    .attr('width', 420)
    .attr('height', barHeight * data.length);

// initiate data join. This means defining the selection to which we will join data
// no g elements exist as child elements of the svg element, but we have defined the type of element we will be adding
var barElements = svgChart.selectAll('g')
    // join the data array defined above to our selector
    .data(data)
    // this function gives us a selection that represents all the data with no corresponding DOM element in the selection
    .enter()
    // this appends a new DOM element (in this case, g) for each new bound data point
    // this returns a new selection containing all of the new elements that have been added
    .append('g')
    // add a transform attribute to each bound data point in the selection
    // translate simply moves the element by (x,y) from the top left corner of the container
    .attr('transform', function (d, i) { return 'translate(0, ' + i * barHeight + ')' });

// now we append a couple of child elements to each g element in the selector
// since we are using append we cannot keep chaining methods as append is returning a new selector
barElements.append('rect')
    // now we are working with a selector containing all of the rect elements that were appended
    // give all the rect elements an attribute of width. I'm guessing x gives you the data point?
    .attr('width', scaleLinearly)
    .attr('height', barHeight - 1);

// now add the text elements to each bar (g) element
barElements.append('text')
    // set the x position of this text element to be 3px from the end of the bar
    .attr('x', function (d) { return scaleLinearly(d) - 3; })
    // set the y position to be halfway down the bar
    .attr('y', barHeight / 2)
    // set dy, which is a shift along the y axis. This is useful for vertically aligning text, since it can be specified in em
    .attr('dy', '.35em')
    // and finally, set the text for this text element. just return data point
    .text(function (d) { return d; });

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