/**************************************************/
/* Vis 1: Heat map
/**************************************************/
// set the dimensions and margins of the graph
var margin_vis_1 = {top: 100, right: 30, bottom: 30, left: 120},
  width_vis_1 = 650 - margin_vis_1.left - margin_vis_1.right,
  height_vis_1 = 520 - margin_vis_1.top - margin_vis_1.bottom;

// append the svg object to the body of the page
var svg_vis_1 = d3.select("#data_viz_1")
.append("svg")
  .attr("width", width_vis_1 + margin_vis_1.left + margin_vis_1.right)
  .attr("height", height_vis_1 + margin_vis_1.top + margin_vis_1.bottom)
.append("g")
  .attr("transform",
        "translate(" + margin_vis_1.left + "," + margin_vis_1.top + ")");

// Build color scale
var color_men = d3.scaleLinear()
  .range(["#e1f5fe", "#01579b"])
  .domain([1, 22])

var color_women = d3.scaleLinear()
  .range(["#fee3e2", "#b30900"])
  .domain([1, 16])

  var color_pairs = d3.scaleLinear()
  .range(["#ccff90", "#90EE90"])
  .domain([1, 5])

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

const show_heatmap = (data, color, gender) => {
  // Clear existing graph
  svg_vis_1.selectAll("g").remove()
  svg_vis_1.selectAll("rect").remove()
  svg_vis_1.selectAll("text").remove()

  // Build X scales and axis:
  myGroups = Array.from(d3.rollup(data, v => v.length, d => d.year).keys())
  let x = d3.scaleBand()
    .range([ 0, width_vis_1 ])
    .domain(myGroups)
    .padding(0.01);
  svg_vis_1.append("g")
    .attr("transform", "translate(0," + height_vis_1 + ")")
    .call(d3.axisBottom(x).tickSize(0));

  // Build Y scales and axis:
  data.sort(dynamicSort("country"));
  myVars = Array.from(d3.rollup(data, v => v.length, d => d.country).keys())
  var y = d3.scaleBand()
    .range([ height_vis_1, 0 ])
    .domain(myVars)
    .padding(0.01);
  svg_vis_1.append("g")
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

  svg_vis_1.selectAll()
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
  svg_vis_1.append("text")
          .attr("x", 0)
          .attr("y", -50)
          .attr("text-anchor", "left")
          .style("font-size", "22px")
          .text("Medals Through Time");

  // Add subtitle to graph
  svg_vis_1.append("text")
          .attr("x", 0)
          .attr("y", -20)
          .attr("text-anchor", "left")
          .style("font-size", "14px")
          .style("fill", "grey")
          .style("max-width", 400)
          .text("Category: " + gender);
};

/**************************************************/
/* Vis 2: Stack Bar Chart 
/**************************************************/
// set the dimensions and margins of the graph
var margin_vis_2 = {top: 100, right: 30, bottom: 90, left: 120},
  width_vis_2 = 650 - margin_vis_2.left - margin_vis_2.right,
  height_vis_2 = 520 - margin_vis_2.top - margin_vis_2.bottom;

// append the svg object to the body of the page
var svg_vis_2 = d3.select("#data_viz_2")
  .append("svg")
    .attr("width", width_vis_2 + margin_vis_2.left + margin_vis_2.right)
    .attr("height", height_vis_2 + margin_vis_2.top + margin_vis_2.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin_vis_2.left + "," + margin_vis_2.top + ")");

const show_barchart = (data, y_axis, gender) => {
  // Clear existing graph
  svg_vis_2.selectAll("g").remove()
  svg_vis_2.selectAll("rect").remove()
  svg_vis_2.selectAll("text").remove()

  // List of medal_types = header of the csv files = soil condition here
  var medal_types = data.columns.slice(0)

  // List of countries = species here = value of the first column called group -> I show them on the X axis
  var countries = d3.map(data, function(d){return(d.Country)})

  // Add X axis
  var x = d3.scaleBand()
      .domain(countries)
      .range([0, width_vis_2])
      .padding([0.2])

  svg_vis_2.append("g")
    .attr("transform", "translate(0," + height_vis_2 + ")")
    .call(d3.axisBottom(x).tickSizeOuter(0))
    .selectAll("text")  
    .style("text-anchor", "start")
    .attr("transform", "rotate(45)" );;;

  // Add Y axis
  var y = d3.scaleLinear()
    .domain([0, y_axis])
    .range([ height_vis_2, 0 ]);

  svg_vis_2.append("g")
    .call(d3.axisLeft(y));

  // color palette = one color per subgroup
  var color = d3.scaleOrdinal()
    .domain(medal_types)
    .range(['#000000','#FFD700','#C0C0C0','#CD7F32'])
    
  //stack the data? --> stack per subgroup
  var stackedData = d3.stack()
    .keys(medal_types)
    (data)

  // Create a tooltip
  var tooltip = d3.select("#data_viz_2")
    .append("div")
    .style("opacity", 0)
    .attr("class", "tooltip")
    .style("background-color", "white")
    .style("border", "solid")
    .style("border-width", "1px")
    .style("border-radius", "5px")
    .style("padding", "10px")

  // Three function that change the tooltip when user hover / move / leave a cell
  var mouseover = function(event, d) {
    var subgroupName = d3.select(this.parentNode).datum().key;
    var subgroupValue = d.data[subgroupName];
    tooltip
        .html(subgroupName + "<br>" + "Medal: " + subgroupValue)
        .style("opacity", 1)
  }

  var mousemove = function(event, d) {
    tooltip
      .style("left", (d3.pointer(event, this)[0]+90) + "px") // It is important to put the +90: other wise the tooltip is exactly where the point is an it creates a weird effect
      .style("top", (d3.pointer(event, this)[1]) + "px")
  }

  var mouseleave = function(event, d) {
    tooltip
      .style("opacity", 0)
  }

  // Show the bars
  svg_vis_2.append("g")
    .selectAll("g")
    // Enter in the stack data = loop key per key = group per group
    .data(stackedData)
    .enter().append("g")
      .attr("fill", function(d) { return color(d.key); })
      .selectAll("rect")
      // enter a second time = loop subgroup per subgroup to add all rectangles
      .data(function(d) { return d; })
      .enter().append("rect")
        .attr("x", function(d) { return x(d.data.Country); })
        .attr("y", function(d) { return y(d[1]); })
        .attr("height", function(d) { 
          return y(d[0]) - y(d[1] ? d[1] : 0); 
        })
        .attr("width",x.bandwidth())
        .attr("stroke", "grey")
      .on("mouseover", mouseover)
      .on("mousemove", mousemove)
      .on("mouseleave", mouseleave)

  // Add title to graph
  svg_vis_2.append("text")
          .attr("x", 0)
          .attr("y", -50)
          .attr("text-anchor", "left")
          .style("font-size", "22px")
          .text("Total Medals By Country");

  // Add subtitle to graph
  svg_vis_2.append("text")
          .attr("x", 0)
          .attr("y", -20)
          .attr("text-anchor", "left")
          .style("font-size", "14px")
          .style("fill", "grey")
          .style("max-width", 400)
          .text("Category: " + gender);
};

/**************************************************/
/* Loading vis based on selection
/**************************************************/
const run_men = () => {
  d3.dsv(",", "data/olympics_top_15_men_yoy.csv", function(d) {
    return {
      year: d.Year,
      country: d.Country,
      medal: d.Total
    };
  }).then(function(data) {
    show_heatmap(data, color_men, 'Men');
  });

  d3.dsv(",", "data/olympics_top_15_men_medal.csv", function(d) {
    return {
      Country: d.Country,
      Gold: d.Gold,
      Silver: d.Silver,
      Bronze: d.Bronze,
    };
  }).then(function(data) {
    show_barchart(data, 260, 'Men');
  });
}

const run_women = () => {
  d3.dsv(",", "data/olympics_top_15_women_yoy.csv", function(d) {
    return {
      year: d.Year,
      country: d.Country,
      medal: d.Total
    };
  }).then(function(data) {
    show_heatmap(data, color_women, 'Women');
  });

  d3.dsv(",", "data/olympics_top_15_women_medal.csv", function(d) {
    return {
      Country: d.Country,
      Gold: d.Gold,
      Silver: d.Silver,
      Bronze: d.Bronze,
    };
  }).then(function(data) {
    show_barchart(data, 110, 'Women');
  });
}

const run_pairs = () => {
  d3.dsv(",", "data/olympics_top_15_pairs_yoy.csv", function(d) {
    return {
      year: d.Year,
      country: d.Country,
      medal: d.Total
    };
  }).then(function(data) {
    show_heatmap(data, color_pairs, 'Mixed Pairs');
  });

  d3.dsv(",", "data/olympics_top_15_pairs_medal.csv", function(d) {
    return {
      Country: d.Country,
      Gold: d.Gold,
      Silver: d.Silver,
      Bronze: d.Bronze,
    };
  }).then(function(data) {
    show_barchart(data, 25, 'Mixed Pairs');
  });
}

run_men();
