var map = d3.geomap.choropleth()
    .geofile('foreign-lawyers/USA.json')
    .projection(d3.geo.albersUsa)
    .column('Percent')
    .unitId('fips')
    .scale(900)
    .legend(true);

d3.csv('foreign-lawyers/aus-states.csv', function(error, data) {
    d3.select('#map')
        .datum(data)
        .call(map.draw, map);
});
