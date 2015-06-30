var map = d3.geomap.choropleth()
    .geofile('foreign-lawyers/USA.json')
    .colors(colorbrewer.YlGnBu[9])
    .projection(d3.geo.albersUsa)
    .column('Percent')
    .format(function(d) {
        return d3.format(',.03f')(d) + '%';
    })
    .unitId('fips')
    .scale(900)
    .legend(true);

d3.csv('foreign-lawyers/aus-states.csv', function(error, data) {
    d3.select('#map')
        .datum(data)
        .call(map.draw, map);
});
