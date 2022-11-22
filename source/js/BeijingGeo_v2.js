const BeijingGeoJson = {
    "type": "FeatureCollection",
    "features": [
};


<script>
    var width = 960,
    height = 600;

    var rateById = d3.map();

    var quantize = d3.scale.quantize()
    .domain([0, .15])
    .range(d3.range(9).map(function(i) { return "q" + i + "-9"; }));

    var projection = d3.geoAlbersUsa()
    .scale(1280)
    .translate([width / 2, height / 2]);

    var path = d3.geoPath()
    .projection(projection);

    var svg = d3.select("body svg");
    var constituencies = svg.selectAll("path, polygon");

    d3.queue()
    .defer(d3.csv, "https://github.com/Yinghzzz/document/blob/main/data3.csv", function(d) {   rateById.set(d.id, +d.rate); });

    function ready(error, us) {
    if (error) throw error;

    constituencies.data(function(d){return d.id;})
    .enter().append("path")
    .attr("class", function(d) { return quantize(rateById.get(d.id)); })
    .attr("d", path);

    svg.append("path")
    .datum(topojson.mesh(constituencies, constituencies.d.id, function(a, b) { return a !== b; }))
    .attr("class", "constituency")
    .attr("d", path);
}

    d3.select(self.frameElement).style("height", height + "px");

</script>