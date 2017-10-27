$(document).ready(function() {
    $('#loadingMap').modal({backdrop: 'static', keyboard: false});

    var map = new google.maps.Map(document.getElementById('map'), {
        mapTypeId: 'roadmap',
        zoom: 1,
        streetViewControl: false,
    });
    map.setTilt(0);
    
    const bounds = new google.maps.LatLngBounds();
    let infoWindow = new google.maps.InfoWindow(), marker, i, j;
    
    Parse.initialize(window.atob(appId), window.atob(jsKey));
    Parse.serverURL = window.atob(apiRoot);

    function formatWithTwoDigits(n) {
        return n > 9 ? '' + n : '0' + n;
    }

    function getIcon(status) {
        if (status === 'ACTIVED') {
            return '/static/img/pa/pa_enabled.png';
        } else if (status === 'DISABLED') {
            return '/static/img/pa/pa_disabled.png';
        } else if (status === 'ALERT') {
            return '/static/img/pa/pa_alert.png';
        }
    }

    function getStatus(status) {
        if (status === 'ACTIVED') {
            return 'Ativo';
        } else if (status === 'DISABLED') {
            return 'Desativo';
        } else if (status === 'ALERT') {
            return 'Alerta';
        }
    }

    function emptyOrNull(text) {
        if (text) {
            return text;
        } else {
            return '-';
        }
    }
    
    const queryCity = new Parse.Query('Cities');
    queryCity.get(cityId).then((data) => {
        return data;
    }).then((city) => {
        const connectionTime = 3;

        const dateUTC = new Date().toJSON().slice(0, 10);
        const dateFrom = new Date(dateUTC + ' 00:00:00');
        const dateTo = new Date(dateUTC + ' 23:59:59');
        const queryMeters = new Parse.Query('ParkingMeters');

        const nowDate = new Date(dateNow);
        const nowSeconds = nowDate.getTime() / 1000;
        
        queryMeters
            .include('lastStatus')
            .include('lastSafeAlert')
            .include('lastDoorAlert')
            .include('lastSummary')
            .equalTo('city', city)
            .equalTo('disabled', false)
            .equalTo('status', true)
            .addDescending('idPa');
        queryMeters.find().then((data) => {
            return data;
        }).then((meters) => {
            const promisesMeters = meters.map((meter) => {
                const promise = new Parse.Promise();
                const latLng = meter.get('latLng');
                const _item = {
                    'id': meter.get('idPa'),
                    'address': meter.get('address'),
                    'latitude': latLng.latitude,
                    'longitude': latLng.longitude,
                    'status': {},
                    'info': '',
                    'lastUpdate': '',
                    'totalSales': 0,
                    'textAlertDoor': '',
                    'textAlertSafe': '',
                    'textAlertStatus': '',
                };

                return meter.fetch().then((data) => {
                    const status = data.get('lastStatus');
                    if (status) {
                        return status.fetch();
                    } else {
                        return Parse.Promise.as(null);
                    }
                }).then((status) => {
                    let meterStatus = 'DISABLED';
                    if (status) {
                        const lastUpdate = status.get('lastUpdate');
                        const lastUpdateDate = new Date(lastUpdate);
                        const lastUpdateSeconds = lastUpdateDate.getTime() / 1000;

                        const d = new Date(1970, 0, 1);
                        d.setSeconds(lastUpdateSeconds - ((city.get('connectionTime') ? city.get('connectionTime') : connectionTime) * 60));

                        if ((lastUpdateSeconds + 10800) > nowSeconds) {
                            meterStatus = 'ACTIVED';
                        }

                        const dateString = ('0' + d.getDate()).slice(-2) + '/' + ('0' + (d.getMonth() + 1)).slice(-2) + '/' + d.getFullYear() + ' - ' + ('0' + d.getHours()).slice(-2) + ':' + ('0' + d.getMinutes()).slice(-2);

                        _item.lastUpdate = dateString;
                        _item.status = {
                            battery: status.get('battery'),
                            charge: status.get('charge'),
                            status: status.get('status'),
                            sensor: status.get('sensor'),
                            coinsAccepted: status.get('coinsAccepted'),
                            coinsRejected: status.get('coinsRejected'),
                            pwm: status.get('pwm'),
                            serial: status.get('serial'),
                            observation: status.get('observation')
                        };

                        const battery = parseFloat(status.get('battery'));
                        const referenceComparation = parseFloat(city.get('referenceComparation'));

                        // if (battery && referenceComparation && (battery < referenceComparation)) {
                        _item['textAlertStatus'] = `Tensão: ${battery}v atual e ${referenceComparation}v esperado`;
                        // }
                    }
                    _item.info = meterStatus;
                    return Parse.Promise.as(_item);
                }).then(() => {
                    const door = meter.get('lastDoorAlert');
                    if (door) {
                        return door.fetch();
                    } else {
                        return Parse.Promise.as(null);
                    }
                }).then((alertDoor) => {
                    if (alertDoor) {
                        switch(alertDoor.get('typeAlert')) {
                            case 1:
                                _item['textAlertDoor'] = 'Porta, Abertura não autorizada';
                                break;
                            case 2:
                                _item['textAlertDoor'] = 'Porta, Fechamento';
                                break;
                            default:
                                _item['textAlertDoor'] = 'Porta, Abertura autorizada';
                        }
                    }
                    return Parse.Promise.as(_item);
                }).then(() => {
                    const safe = meter.get('lastSafeAlert');
                    if (safe) {
                        return safe.fetch();
                    } else {
                        return Parse.Promise.as(null);
                    }
                }).then((safeAlert) => {
                    if (safeAlert) {
                        switch(safeAlert.get('typeAlert')) {
                            case 1:
                                _item['textAlertSafe'] = 'Cofre, Abertura não autorizada';
                                break;
                            case 2:
                                _item['textAlertSafe'] = 'Cofre, Fechamento';
                                break;
                            default:
                                _item['textAlertSafe'] = 'Cofre, Abertura autorizada';
                        }
                    }
                    return Parse.Promise.as(_item);
                }).then(() => {
                    const summary = meter.get('lastSummary');
                    if (summary) {
                        return summary.fetch();
                    } else {
                        return Parse.Promise.as(null);
                    }
                }).then((lastSummary) => {
                    if (lastSummary) {
                        _item['totalSales'] = lastSummary.get('day' + formatWithTwoDigits(nowDate.getDate()));
                    }
                    return Parse.Promise.as(_item);
                }).then((_item) => {
                    var position = new google.maps.LatLng(_item.latitude, _item.longitude);
                    bounds.extend(position);
                    marker = new google.maps.Marker({
                        position: position,
                        map: map,
                        title: `${_item.id}`,
                        icon: getIcon(`${_item.info}`)
                    });

                    j += 1;
                    google.maps.event.addListener(marker, 'click', (function(marker, j) {
                        return function() {
                            let value = (_item.totalSales ? _item.totalSales.toFixed(2) : '0.00');
                            let textLabel = '<p><strong>ID:</strong> ' + _item.id + '</p>' +
                                            '<p><strong>Status:</strong> ' + getStatus(_item.info) + '</p>';
                            if (userType === 'TECHNICIAN') {
                                textLabel += `<p><strong>Último Status:</strong> ${emptyOrNull(_item.textAlertStatus)}</p>`+
                                            `<p><strong>Último Alerta Porta:</strong> ${emptyOrNull(_item.textAlertDoor)}</p>`+
                                            `<p><strong>Último Alerta Cofre:</strong> ${emptyOrNull(_item.textAlertSafe)}</p>`;
                            } else {
                                textLabel += `<p><strong>Tensão da bateria:</strong> ${emptyOrNull(_item.status.battery)}</p>` +
                                            `<p><strong>Em carga:</strong> ${emptyOrNull(_item.status.charge)}</p>` +
                                            `<p><strong>Status do Leitor:</strong> ${emptyOrNull(_item.status.status)}</p>` +
                                            `<p><strong>Sensores do Leitor:</strong> ${emptyOrNull(_item.status.sensor)}</p>` +
                                            `<p><strong>Moedas Aceitas:</strong> ${emptyOrNull(_item.status.coinsAccepted)}</p>` +
                                            `<p><strong>Moedas Recusadas:</strong> ${emptyOrNull(_item.status.coinsRejected)}</p>` +
                                            `<p><strong>PWM:</strong> ${emptyOrNull(_item.status.pwm)}</p>` +
                                            `<p><strong>Serial do Leitor:</strong> ${emptyOrNull(_item.status.serial)}</p>` +
                                            `<p><strong>Observações:</strong> ${emptyOrNull(_item.status.observation)}</p>`+
                                            `<p><strong>Última conexão:</strong> ${emptyOrNull(_item.lastUpdate)}</p>` +
                                            `<p><strong>Valor arrecadado (dia):</strong> R$ ${value}</p>`;
                            }
                            textLabel += `<p><strong>Localização:</strong> ${emptyOrNull(_item.address)}</p>`;
                            infoWindow.setContent(textLabel);
                            infoWindow.open(map, marker);
                        }
                    })(marker, j));

                    map.fitBounds(bounds);
                    promise.resolve(null);
                    return promise;
                });
            });

            const promisesOutlets = new Parse.Promise();
            const queryUser = new Parse.Query(Parse.User);

            queryUser.equalTo('status', 'LICENSED');
            queryUser.find().then((users) => {
                const queryOutlets = new Parse.Query('Outlets');
                queryOutlets
                    .include('city')
                    .include('user')
                    .equalTo('city', city)
                    .equalTo('disabled', false)
                    .exists('latLng')
                    .containedIn('user', users)
                    .addDescending('name');
                queryOutlets.find().then((_outlets) => {
                    const promises = _outlets.map((outlet) => {
                        const promise = new Parse.Promise();
                        const latLng = outlet.get('latLng');
                        const position = new google.maps.LatLng(latLng.latitude, latLng.longitude);
                        
                        bounds.extend(position);
                        marker = new google.maps.Marker({
                            position: position,
                            map: map,
                            title: outlet.get('name'),
                            icon: '/static/img/pa/outlet.png'
                        });
                        
                        i += 1;
                        google.maps.event.addListener(marker, 'click', (function(marker, i) {
                            return function() {
                                infoWindow.setContent('<p><strong>Nome:</strong> ' + outlet.get('name') + '</p><p><strong>Endereço:</strong> ' + outlet.get('address') + '</p>');
                                infoWindow.open(map, marker);
                            }
                        })(marker, i));
                        
                        map.fitBounds(bounds);
                        promise.resolve(null);
                        return promise;
                    });

                    Promise.all(promises).then(() => {
                        promisesOutlets.resolve(null);
                    });
                });
            });

            Promise.all(promisesMeters, promisesOutlets).then(() => {
                $('#loadingMap').modal('hide');
                setTimeout(function() { window.location.reload() }, 300000);
            });

            const result = [];
            const queryMeters = new Parse.Query("ParkingMeters");

            for (let i = 1; i <= 10; i += 1) {
                result[i] = {
                    totalSales: 0,
                    totalVacancies: 0,
                    percent: 0,
                    color: ''
                };
            }

            queryMeters
                .equalTo("city", city)
                .equalTo("disabled", false)
                .equalTo("status", true);
    
            queryMeters.find().then((data) => {
                return data;
            }).then((meters) => {
                const promises = meters.map((meter) => {
                    const promise = new Parse.Promise();
    
                    const querySales = new Parse.Query("ParkingMetersSales");
                    querySales
                        .equalTo('parking', meter)
                        .equalTo('closed', false)
                        .greaterThan('price', 0)
                        .greaterThanOrEqualTo('createdAt', dateFrom)
                        .lessThanOrEqualTo('createdAt', dateTo);
    
                    querySales.each((sales) => {
                        const timeFinish = sales.get('dateTimeFinish');
                        const timeFinishDate = new Date(timeFinish);
                        const timeFinishSeconds = timeFinishDate.getTime() / 1000;
    
                        if (nowSeconds < timeFinishSeconds) {
                            result[meter.get('setor')].totalSales += 1;
                        }
                    }).done(() => {
                        return Parse.Promise.as(null);
                    }).then(() => {
                        if (meter.get('qttOfVacancies')) {
                            result[meter.get('setor')].totalVacancies += meter.get('qttOfVacancies');
                        }
                        promise.resolve(null);
                    });
    
                    return promise;
                });

                Promise.all(promises).then(() => {
                    result.map((sector, index) => {
                        const totalSales = parseInt(sector['totalSales']);
                        const totalVacancies = parseInt(sector['totalVacancies']);
                        const sectorPercent = totalSales * 100 / totalVacancies;
                        
                        const formatPercent = (num) => {
                            return Number(num / 100).toLocaleString(undefined, {style: 'percent', minimumFractionDigits:2});
                        }
    
                        try {
                            if (sectorPercent < parseInt(city.get('utilizationRed'))) {
                                $('#sector_' + index).addClass('txt_red').text(formatPercent(sectorPercent));
                            } else if (city.get('utilizationYellowFrom') >= sectorPercent && sectorPercent <= parseInt(city.get('utilizationYellowTo'))) {
                                $('#sector_' + index).addClass('txt_yellow').text(formatPercent(sectorPercent));
                            } else if (sectorPercent > parseInt(city.get('utilizationGreen'))) {
                                $('#sector_' + index).addClass('txt_green').text(formatPercent(sectorPercent));
                            } else {
                                $('#sector_' + index).addClass('txt_red').text(formatPercent(0));
                            }
                        } catch(err) {
                            $('#sector_' + index).addClass('txt_red').text(formatPercent(0));
                        }
                    });
                });
            });
        });
    });
});