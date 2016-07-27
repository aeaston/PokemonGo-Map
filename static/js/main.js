(function () {
    var map, markerCache = {};

    // Label countdown
    (function () {
        function zeroPad(n) {
            return ('0' + n).slice(-2);
        }

        function setLabelTime() {
            $('.label-countdown').each(function (index, element) {
                var difference, minutes, seconds, timestring,
                    disappearsAt = new Date(parseInt(
                        element.getAttribute('disappears-at')
                    ));

                difference = disappearsAt - new Date();
                if (difference < 0) {
                    timestring = '(expired)';
                } else {
                    minutes = Math.floor(difference / (60 * 1000));
                    difference %= (60 * 1000);
                    seconds = Math.floor(difference / 1000);

                    timestring = [
                        '(', zeroPad(minutes), 'm', zeroPad(seconds), 's', ')'
                    ].join('');
                }

                $(element).text(timestring)
            });
        };

        window.setInterval(setLabelTime, 1000);
    })();

    function createMap() {
        var center = new google.maps.LatLng(
            window.POGO.origin_lat, window.POGO.origin_lng
        );
        map = new google.maps.Map(
            document.getElementById('fullmap'), {
                center: center,
                zoom: window.POGO.zoom,
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                zoomControl: true,
                mapTypeControl: true,
                scaleControl: true,
                streetViewControl: true,
                rotateControl: true,
                fullscreenControl: true
        });
        new google.maps.Marker({
            position: center,
            map: map,
            icon: '//maps.google.com/mapfiles/ms/icons/red-dot.png'
        });
    }

    function addMarker(item) {
        if (item.key in markerCache) {
            return;
        }

        var disappearsMs = new Date(item.disappear_time) - new Date();
        if (disappearsMs < 0) {
            return;
        }
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(item.lat, item.lng),
            map: map,
            icon: item.icon,
        });
        markerCache[item.key] = marker;

        var infoWindow = new google.maps.InfoWindow({content: item.infobox});
        marker.addListener('click', infoWindow.open.bind(infoWindow, map, marker));

        window.setTimeout(
            function () {
                markerCache[item.key].setMap(null);
                delete markerCache[item.key];
            },
            disappearsMs
        );
    }

    function updateMap() {
        $.get('/data', function(data) {
            for (var i = 0; i < data.length; i += 1) {
                addMarker(data[i]);
            }
        });
    }

    // Modal functionality
    var Modal = (function () {
        var body = $('body');

        function maybeHideModals(e) {
            if ($(e.target).is('.modal-visible')) {
                body.removeClass('modal-visible');
                $('.modal').addClass('hidden');
            }
        }

        function handleKeypress(e) {
            if (e.which === 27) {
                maybeHideModals(e);
            }
        }

        function showModal(modalElement, e) {
            body.addClass('modal-visible');
            modalElement.removeClass('hidden');
            e.stopPropagation();
        }

        body.on('click', maybeHideModals);
        $(window).on('keyup', handleKeypress);

        return {showModal: showModal};
    })();

    // Settings modal
    (function () {
        var num,
            settingsModal = $('.modal-settings'),
            search = settingsModal.find('.search'),
            results = settingsModal.find('.search-results');

        function filterPokemon() {
            function getPokemonFromText(text) {
                var i, name, ret = [], asNumber = parseInt(text, 10);

                if (1 <= asNumber && asNumber <= 151) {
                    ret.push(asNumber);
                } else if (text) {
                    for (i = 0; i < window.POGO.pokemon.length; i += 1) {
                        name = window.POGO.pokemon[i].toLowerCase();
                        if (name.indexOf(text) === 0) {
                            ret.push(i);
                        }
                    }
                }
                return ret;
            }

            console.log(getPokemonFromText(search.val().trim().toLowerCase()));
        }

        search.val('');
        search.on('keyup', filterPokemon);

        $('.settings').on('click', Modal.showModal.bind(null, settingsModal));
    })();

    // About modal
    (function () {
        var aboutModal = $('.modal-about');
        $('.about').on('click', Modal.showModal.bind(null, aboutModal));
    })();

    window.initMap = function () {
        createMap();
        updateMap();
        $('.refresh').on('click', updateMap);
        if (window.POGO.auto_refresh) {
            window.setInterval(updateMap, window.POGO.auto_refresh);
        }
    }
})();
