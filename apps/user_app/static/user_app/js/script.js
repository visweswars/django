var geocoder;
var map;
var markers=[];
console.log("google.maps");
function initialize() {
    console.log("initialize");
    geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng(41.8971828, -87.63523709999998);
    var mapOptions = {
        zoom: 14,
        center: latlng
    };
    map = new google.maps.Map(document.getElementById('map'), mapOptions);
};
function addMarker(index,title,address) {
    geocoder.geocode({ 'address': address }, function (results, status) {
        if (status == 'OK') {
            var marker = new google.maps.Marker({
                map: map,
                position: results[0].geometry.location,
                title: title
            });
            markers.push(marker);
            var contentString = '<div id="marker">' +
                '<h4>'+ address + '</h4>' +
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
    console.log("ready");
    $("li").each(function( index ) {
        console.log( $( this ).text() );                
        addMarker(index,"Zillow",$( this ).text());

    });
});