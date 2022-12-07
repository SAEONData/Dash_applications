window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, context) {
            {
                return ['PELTERP1'].includes(feature.properties.name);
            }
        },
        function1: function(feature, latlng, context) {
            // Figure out if the marker is selected.
            //const selected = context.props.hideout.includes(feature.properties.name);
            // Render selected markers in red.
            //if(selected){return L.circleMarker(latlng, {color: 'red'});}
            // Render non-selected markers in blue.
            //circleOptions.fillColor = 'red'
            return L.circleMarker(latlng, {
                fillColor: 'red',
                fillOpacity: '0.75',
                Opacity: '1'
            });
        },
        function2: function(feature, context) {
            {
                return ['PELTERP1'].includes(feature.properties.name);
            }
        },
        function3: function(feature, latlng, context) {
            // Figure out if the marker is selected
            //const match = context.props.hideout &&  context.props.hideout.properties.name === name;
            const match = context.props.hideout.includes(feature.properties.name);
            const flag = L.icon({
                iconUrl: '/assets/star_red.png',
                iconSize: [16, 16]
            });
            const flag2 = L.icon({
                iconUrl: '/assets/star_green.png',
                iconSize: [16, 16]
            });
            //const selected = context.props.hideout.includes(feature.properties.name);
            // Render selected markers in red.
            if (match) {
                return L.marker(latlng, {
                    icon: flag2
                })
            };
            //L.circleMarker(latlng, {fillColor: 'green', fillOpacity: '0.75',Opacity: '1'});}
            //if(selected){return L.circleMarker(latlng, {fillColor: 'green', fillOpacity: '0.75',Opacity: '1'});}
            // Render non-selected markers in blue.
            //circleOptions.fillColor = 'red'
            return L.marker(latlng, {
                icon: flag
            });
            //L.circleMarker(latlng, {fillColor: 'red', fillOpacity: '0.75',Opacity: '1'});
        }
    }
});