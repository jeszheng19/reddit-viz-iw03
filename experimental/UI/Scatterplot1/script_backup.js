
var data2 = [];
var a = {};
a['Annualized Return'] = 0.0770203710991655;
a['Annualized Standard Deviation'] = 0.0694461870173684;
a['Maximum Drawdown'] = 0.292688394529575;
a['Title'] = 'title a';
data2.push(a);
var b = {};
b['Annualized Return'] = 0.0767109922711062;
b['Annualized Standard Deviation'] = 0.0870559916457339;
b['Maximum Drawdown'] = 0.11676813742079;
b['Title'] = 'title b';
data2.push(b);
var c = {};
c['Annualized Return'] = 0.0326542894911763;
c['Annualized Standard Deviation'] = 0.190869128421505;
c['Maximum Drawdown'] = 0.495619599274476;
c['Title'] = 'title c';
data2.push(c);

function draw_scatterplot(data, div_id) {
  var body = d3.select('body')
  var selectData = [ { "text" : "Annualized Return" },
                     { "text" : "Annualized Standard Deviation" },
                     { "text" : "Maximum Drawdown" },
                   ]


// TODO move the selects out into index.html

  // Select X-axis Variable
  var span = body.append('span')
    .text('Select X-Axis variable: ')
  var yInput = body.append('select')
      .attr('id','xSelect')
      .on('change',xChange)
    .selectAll('option')
      .data(selectData)
      .enter()
    .append('option')
      .attr('value', function (d) { return d.text })
      .text(function (d) { return d.text ;})
  body.append('br')

  // Select Y-axis Variable
  var span = body.append('span')
      .text('Select Y-Axis variable: ')
  var yInput = body.append('select')
      .attr('id','ySelect')
      .on('change',yChange)
    .selectAll('option')
      .data(selectData)
      .enter()
    .append('option')
      .attr('value', function (d) { return d.text })
      .text(function (d) { return d.text ;})
  body.append('br')

  // Variables
  var body = d3.select('body')
  var margin = { top: 50, right: 50, bottom: 50, left: 50 }
  var h = 500 - margin.top - margin.bottom
  var w = 500 - margin.left - margin.right
  var formatPercent = d3.format('.2%')

  // Scales
  var colorScale = d3.scale.category20()
  var xScale = d3.scale.linear()
    .domain([
      d3.min([0,d3.min(data,function (d) { return d['Annualized Return'] })]),
      d3.max([0,d3.max(data,function (d) { return d['Annualized Return'] })])
      ])
    .range([0,w])
  var yScale = d3.scale.linear()
    .domain([
      d3.min([0,d3.min(data,function (d) { return d['Annualized Return'] })]),
      d3.max([0,d3.max(data,function (d) { return d['Annualized Return'] })])
      ])
    .range([h,0])
  // SVG
  var svg = body.append('svg')
      .attr('height',h + margin.top + margin.bottom)
      .attr('width',w + margin.left + margin.right)
    .append('g')
      .attr('transform','translate(' + margin.left + ',' + margin.top + ')')
  // X-axis
  var xAxis = d3.svg.axis()
    .scale(xScale)
    .tickFormat(formatPercent)
    .ticks(5)
    .orient('bottom')
  // Y-axis
  var yAxis = d3.svg.axis()
    .scale(yScale)
    .tickFormat(formatPercent)
    .ticks(5)
    .orient('left')
  // Circles
  var circles = svg.selectAll('circle')
      .data(data)
      .enter()
    .append('circle')
      .attr('cx',function (d) { return xScale(d['Annualized Return']) })
      .attr('cy',function (d) { return yScale(d['Annualized Return']) })
      .attr('r','7')
      .attr('stroke','black')
      .attr('stroke-width',1)
      .attr('fill',function (d,i) { return colorScale(i) }) // COLOR DECIDED HERE.
      .on('mouseover', function () {
        d3.select(this)
          .transition()
          .duration(500)
          .attr('r',13)
          .attr('stroke-width',3)
      })
      .on('mouseout', function () {
        d3.select(this)
          .transition()
          .duration(500)
          .attr('r',7)
          .attr('stroke-width',1)
      })
    .append('title') // TOOLTIP FOR EACH CIRCLE
      .text(function (d) { return d['Title'] +
                           '\nReturn: ' + formatPercent(d['Annualized Return']) +
                           '\nStd. Dev.: ' + formatPercent(d['Annualized Standard Deviation']) +
                           '\nMax Drawdown: ' + formatPercent(d['Maximum Drawdown'])
                         })
  // X-axis
  svg.append('g')
      .attr('class','axis')
      .attr('id','xAxis')
      .attr('transform', 'translate(0,' + h + ')')
      .call(xAxis)
    .append('text') // X-axis Label
      .attr('id','xAxisLabel')
      .attr('y',-10)
      .attr('x',w)
      .attr('dy','.71em')
      .style('text-anchor','end')
      .text('Annualized Return')
  // Y-axis
  svg.append('g')
      .attr('class','axis')
      .attr('id','yAxis')
      .call(yAxis)
    .append('text') // y-axis Label
      .attr('id', 'yAxisLabel')
      .attr('transform','rotate(-90)')
      .attr('x',0)
      .attr('y',5)
      .attr('dy','.71em')
      .style('text-anchor','end')
      .text('Annualized Return')

  function yChange() {
    var value = this.value // get the new y value
    yScale // change the yScale
      .domain([
        d3.min([0,d3.min(data,function (d) { return d[value] })]),
        d3.max([0,d3.max(data,function (d) { return d[value] })])
        ])
    yAxis.scale(yScale) // change the yScale
    d3.select('#yAxis') // redraw the yAxis
      .transition().duration(1000)
      .call(yAxis)
    d3.select('#yAxisLabel') // change the yAxisLabel
      .text(value)
    d3.selectAll('circle') // move the circles
      .transition().duration(1000)
      .delay(function (d,i) { return i*100})
        .attr('cy',function (d) { return yScale(d[value]) })
  }

  function xChange() {
    var value = this.value // get the new x value
    xScale // change the xScale
      .domain([
        d3.min([0,d3.min(data,function (d) { return d[value] })]),
        d3.max([0,d3.max(data,function (d) { return d[value] })])
        ])
    xAxis.scale(xScale) // change the xScale
    d3.select('#xAxis') // redraw the xAxis
      .transition().duration(1000)
      .call(xAxis)
    d3.select('#xAxisLabel') // change the xAxisLabel
      .transition().duration(1000)
      .text(value)
    d3.selectAll('circle') // move the circles
      .transition().duration(1000)
      .delay(function (d,i) { return i*100})
        .attr('cx',function (d) { return xScale(d[value]) })
  }
}

draw_scatterplot(data2, '#pos_neg_scatterplot');
