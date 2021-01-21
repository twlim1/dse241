// set the dimensions and margins of the graph
var margin = {top: 30, right: 30, bottom: 30, left: 120},
  width = 650 - margin.left - margin.right,
  height = 450 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#data_viz_1")
.append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
.append("g")
  .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

// Build color scale
var color_men = d3.scaleLinear()
  .range(["#e1f5fe", "#01579b"])
  .domain([1, 22])

var color_women = d3.scaleLinear()
  .range(["#fee3e2", "#b30900"])
  .domain([1, 16])

  var color_pairs = d3.scaleLinear()
  .range(["#ccff90", "#90EE90"])
  .domain([1, 16])

var dynamicSort = function(property) {
    var sortOrder = -1;
    if(property[0] === "-") {
        sortOrder = -1;
        property = property.substr(1);
    }
    return function (a,b) {
        if(sortOrder == -1){
            return b[property].localeCompare(a[property]);
        }else{
            return a[property].localeCompare(b[property]);
        }        
    }
}

const run_men = () => {
  d3.dsv(",", "data/olympics_men_top_15.csv", function(d) {
    return {
      year: d.Year,
      country: d.Country,
      medal: d.Total
    };
  }).then(function(data) {
      showPlot(data, color_men);
  });
}

const run_women = () => {
  d3.dsv(",", "data/olympics_women_top_15.csv", function(d) {
    return {
      year: d.Year,
      country: d.Country,
      medal: d.Total
    };
  }).then(function(data) {
      showPlot(data, color_women);
  });
}

const run_pairs = () => {
  d3.dsv(",", "data/olympics_pairs_top_15.csv", function(d) {
    return {
      year: d.Year,
      country: d.Country,
      medal: d.Total
    };
  }).then(function(data) {
      showPlot(data, color_pairs);
  });
}

const showPlot = (data, color) => {
  // Clear existing graph
  svg.selectAll("g").remove()
  svg.selectAll("rect").remove()

  // Build X scales and axis:
  console.log(data)
  myGroups = Array.from(d3.rollup(data, v => v.length, d => d.year).keys())
  let x = d3.scaleBand()
    .range([ 0, width ])
    .domain(myGroups)
    .padding(0.01);
  svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x).tickSize(0));

  // Build Y scales and axis:
  data.sort(dynamicSort("country"));
  myVars = Array.from(d3.rollup(data, v => v.length, d => d.country).keys())
  var y = d3.scaleBand()
    .range([ height, 0 ])
    .domain(myVars)
    .padding(0.01);
  svg.append("g")
    .call(d3.axisLeft(y).tickSize(0));

  // create a tooltip
  var tooltip = d3.select("#data_viz_1")
    .append("div")
    .style("opacity", 0)
    .attr("class", "tooltip")
    .style("background-color", "white")
    .style("border", "solid")
    .style("border-width", "2px")
    .style("border-radius", "5px")
    .style("padding", "5px")

  // Three function that change the tooltip when user hover / move / leave a cell
  var mouseover = function(event, d) {
    tooltip.style("opacity", 1)
    d3.select(this)
    .style("stroke", "black")
    .style("opacity", 1)
  }

  var mousemove = function(event, d) {
    tooltip
    .html("Medal Won: " + d.medal)
    .style("left", (d3.pointer(event, this)[0]+70) + "px")
    .style("top", (d3.pointer(event, this)[1]) + "px")
  }

  var mouseleave = function(event, d) {
    tooltip.style("opacity", 0)
    d3.select(this)
      .style("stroke", "none")
      .style("opacity", 0.8)
  }

  svg.selectAll()
      .data(data, function(d) {return d.year+':'+d.country;})
      .enter()
      .append("rect")
      .attr("x", function(d) { return x(d.year) })
      .attr("y", function(d) { return y(d.country) })
      .attr("rx", 4)
      .attr("ry", 4)
      .attr("width", x.bandwidth() )
      .attr("height", y.bandwidth() )
      .style("fill", function(d) {return color(d.medal)} )
      .style("stroke-width", 4)
      .style("stroke", "none")
      .style("opacity", 0.8)
      .on("mouseover", mouseover)
      .on("mousemove", mousemove)
      .on("mouseleave", mouseleave)

  // Add title to graph
  svg.append("text")
          .attr("x", 0)
          .attr("y", -50)
          .attr("text-anchor", "left")
          .style("font-size", "22px")
          .text("A d3.js heatmap");

  // Add subtitle to graph
  svg.append("text")
          .attr("x", 0)
          .attr("y", -20)
          .attr("text-anchor", "left")
          .style("font-size", "14px")
          .style("fill", "grey")
          .style("max-width", 400)
          .text("Heat map: more description");
};

run_men();
