var geocoder;
var map;
var markers=[];
function initialize() {
    geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng(41.8971828, -87.63523709999998);
    var mapOptions = {
        zoom: 12,
        center: latlng
    };
    map = new google.maps.Map(document.getElementById('map'), mapOptions);
};
function addMarker(index,address) {
    geocoder.geocode({ 'address': address }, function (results, status) {
        if (status == 'OK') {
            map.setCenter(results[0].geometry.location);
            var marker = new google.maps.Marker({
                map: map,
                position: results[0].geometry.location,
                title: address
            });
            markers.push(marker);
            var contentString = '<div class="marker">' +
                '<p>'+ address + '</p>' +
                '</div>';
            var infowindow = new google.maps.InfoWindow({
                content: contentString
            });
            if(index===0) {
                infowindow.open(map, marker);
            }
            marker.addListener('click', function () {
                infowindow.open(map, marker);
            });
        }
    });
};
$(document).ready(function () {
    $("#listings li").each(function( index ) {
        initialize();
        var address = $(this).text().replace(/\s+$/,"").replace(/^\s+/,"");
        addMarker(index,address);
    });
});