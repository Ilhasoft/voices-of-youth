if (jQuery != undefined) {
    var django = {
        'jQuery': jQuery,
    }
}


(function($) {

    $(document).ready(function() {

        try {
            var _ = google;
        } catch (ReferenceError) {
            console.log('geoposition: "google" not defined.  You might not be connected to the internet.');
            return;
        }

        var mapDefaults = {
            'mapTypeId': google.maps.MapTypeId.ROADMAP,
            'scrollwheel': false,
            'streetViewControl': false,
            'panControl': false
        };

        var markerDefaults = {
            'draggable': true,
            'animation': google.maps.Animation.DROP
        };

        $('.geoposition-widget').each(function() {
            var $container = $(this),
                $mapContainer = $('<div class="geoposition-map" />'),
                $addressRow = $('<div class="geoposition-address" />'),
                $searchRow = $('<div class="geoposition-search geoposition-control" />'),
                $searchInput = $('<input>', {'type': 'search', 'placeholder': 'Digite o endereço aqui …'}),
                $latitudeField = $container.find('input.geoposition:eq(0)'),
                $longitudeField = $container.find('input.geoposition:eq(1)'),
                latitude = parseFloat($latitudeField.val()) || null,
                longitude = parseFloat($longitudeField.val()) || null,
                map,
                mapLatLng,
                mapOptions,
                mapCustomOptions,
                markerOptions,
                markerCustomOptions,
                marker;

            $mapContainer.css('height', $container.attr('data-map-widget-height') + 'px');
            mapCustomOptions = JSON.parse($container.attr('data-map-options'));
            markerCustomOptions = JSON.parse($container.attr('data-marker-options'));

            $container.append($searchRow, $mapContainer, $addressRow);

            mapLatLng = new google.maps.LatLng(latitude, longitude);
            mapOptions = $.extend({}, mapDefaults, mapCustomOptions);


            mapOptions['zoom'] = 11;
            if (marks.length)
                mapOptions['center'] = new google.maps.LatLng(marks[0].lat, marks[0].lng);
            else {
                mapOptions['center'] = new google.maps.LatLng(-14.2392976, -53.1805017);
                mapOptions['zoom'] = 3;
            }

            map = new google.maps.Map($mapContainer.get(0), mapOptions);
            markerOptions = $.extend({}, markerDefaults, markerCustomOptions, {
                'map': map
            });

            for (i = 0; i < marks.length; i++) {
                var myLatlng = new google.maps.LatLng(marks[i].lat, marks[i].lng);
                var marker = new google.maps.Marker({
                    position: myLatlng,
                    title: marks[i].name
                });
                marker.setMap(map);
            }

            if (!(latitude === null && longitude === null && markerOptions['position'])) {
                markerOptions['position'] = mapLatLng;
            }
        });
    });
})(django.jQuery);
