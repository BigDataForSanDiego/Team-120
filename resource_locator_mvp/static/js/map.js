// Alpine.js component for resource map
function resourceMap() {
    return {
        // Map instance
        map: null,
        markers: null,

        // State
        resources: [],
        selectedResource: null,
        loading: false,
        autoCenter: true, // ✅ Only recenter once on load or when user clicks Recenter

        // User location (default to San Diego)
        userLat: 32.7157,
        userLon: -117.1611,
        userAddress: '',

        // ✅ All resource types (used for buttons + filters)
        resourceTypes: [
            { value: 'food', label: 'Food' },
            { value: 'shelter', label: 'Shelter' },
            { value: 'restroom', label: 'Restroom' },
            { value: 'medical', label: 'Medical' },
            { value: 'legal', label: 'Legal' },
            { value: 'donation', label: 'Donation' },
            { value: 'other', label: 'Other' }
        ],

        // Filters
        selectedTypes: [],
        openNow: false,
        radiusMiles: 5,

        // Initialize component
        init() {
            this.initMap();
            this.getUserLocation(); // load user location first
            this.updateFilters();   // then load data
        },

        // Convert to Title Case for display
        // Be defensive: coerce non-strings (numbers, proxies) and trim whitespace
        toTitleCase(value) {
            if (value === null || value === undefined) return '';
            const str = String(value).trim();
            if (!str) return '';
            return str
                .toLowerCase()
                .replace(/\b\w/g, c => c.toUpperCase());
        },


        // Initialize Leaflet map
        initMap() {
            this.map = L.map('map').setView([this.userLat, this.userLon], 12);


            // Add OpenStreetMap tiles
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution:
                    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                maxZoom: 19
            }).addTo(this.map);

            // Marker cluster group
            this.markers = L.markerClusterGroup();
            this.map.addLayer(this.markers);

            // User marker
            this.updateUserMarker();
        },

        // ✅ Keep user location marker constant
        updateUserMarker() {
            if (this.userMarker) {
                this.map.removeLayer(this.userMarker);
            }


            const userIcon = L.divIcon({
                className: 'user-location-icon',
                html: '<div style="background: #3498db; width: 20px; height: 20px; border-radius: 50%; border: 3px solid white; box-shadow: 0 0 10px rgba(0,0,0,0.3);"></div>',
                iconSize: [20, 20]
            });

            this.userMarker = L.marker([this.userLat, this.userLon], { icon: userIcon }).addTo(this.map);
        },

        // ✅ Get user's current location — centers only once
        getUserLocation() {
            if (navigator.geolocation) {
                this.loading = true;
                navigator.geolocation.getCurrentPosition(
                    (pos) => {
                        this.userLat = pos.coords.latitude;
                        this.userLon = pos.coords.longitude;

                        // Center map only first time or when autoCenter is re-enabled
                        if (this.autoCenter) {
                            this.map.setView([this.userLat, this.userLon], 13);
                            this.autoCenter = false;
                        }

                        this.updateUserMarker();
                        this.loading = false;
                    },
                    (err) => {
                        console.error('Error getting location:', err);
                        alert('Could not get your location. Using default San Diego.');
                        this.loading = false;
                    }
                );
            } else {
                alert('Geolocation is not supported by your browser.');
            }
        },

        // ✅ Toggle a resource type filter
        toggleType(type) {
            const index = this.selectedTypes.indexOf(type);
            if (index > -1) {
                this.selectedTypes.splice(index, 1);
            } else {
                this.selectedTypes.push(type);
            }
            this.updateFilters();
        },



        // ✅ Fetch resources around current location (no recentering)
        async updateFilters() {
            this.loading = true;

            const params = new URLSearchParams();
            params.append('lat', this.userLat);
            params.append('lon', this.userLon);
            params.append('radius_m', this.radiusMiles * 1609.34);

            if (this.selectedTypes.length > 0) {
                params.append('rtype', this.selectedTypes.join(','));
            }


            if (this.openNow) {
                params.append('open_now', 'true');
            }

            const url = `/api/resources/?${params.toString()}`;
            console.log('[DEBUG] Fetching:', url);

            try {
                const res = await fetch(url);
                const data = await res.json();

                // Handle both paginated and plain GeoJSON
                if (data.results && data.results.features) {
                    this.resources = data.results.features;
                } else if (data.features) {
                    this.resources = data.features;
                } else {
                    this.resources = [];
                }

                this.updateMarkers();

                if (this.resources.length === 0) {
                    console.warn('⚠️ No resources found for:', params.toString());
                } else {
                    console.log(`✅ Loaded ${this.resources.length} resources`);
                }
            } catch (error) {
                console.error('❌ Error fetching resources:', error);
                alert('Error loading resources. Please try again.');
            } finally {
                this.loading = false;
            }
        },

        // ✅ Update map markers (does not move user marker)
        updateMarkers() {
            this.markers.clearLayers();

            this.resources.forEach(resource => {
                const coords = resource.geometry.coordinates;
                const lat = coords[1];
                const lon = coords[0];

                // Choose icon color by type
                const iconColor = this.getIconColor(resource.properties.rtype);
                const icon = L.divIcon({
                    className: 'resource-marker',
                    html: `<div style="background: ${iconColor}; width: 30px; height: 30px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px;">${this.getIconText(resource.properties.rtype)}</div>`,
                    iconSize: [30, 30]
                });

                const marker = L.marker([lat, lon], { icon });

                // Popup info (all details live in callout)
                const name = this.toTitleCase(resource.properties.name || '');
                const address = this.toTitleCase(resource.properties.address || '');
                const phone = resource.properties.phone || '';
                const email = resource.properties.email || '';
                const website = resource.properties.website || '';

                const mapsHref = `https://www.google.com/maps/dir/?api=1&destination=${lat},${lon}`;

                let popupHtml = `
                    <div style="min-width: 240px; max-width: 320px;">
                        <h3 style="margin: 0 0 0.5rem 0; text-transform: capitalize;">${name}</h3>
                        <p style="margin: 0.25rem 0; text-transform: capitalize;">${resource.properties.rtype || ''}</p>
                        <p style="margin: 0.25rem 0; font-size: 0.95rem;">
                            ${address ? `<a href="${mapsHref}" target="_blank" rel="noopener">${address}</a>` : 'No address'}
                        </p>
                        ${resource.properties.is_open_now === true ? '<span style="color: green; font-weight: bold;">Open Now</span>' : ''}
                        ${resource.properties.is_open_now === false ? '<span style="color: red; font-weight: bold;">Closed</span>' : ''}
                        ${phone ? `<p style="margin: 0.25rem 0;"><a href="tel:${phone}">${phone}</a></p>` : ''}
                        ${email ? `<p style="margin: 0.25rem 0;"><a href="mailto:${email}">${email}</a></p>` : ''}
                        ${website ? `<p style="margin: 0.25rem 0;"><a href="${website}" target="_blank" rel="noopener">Visit Website</a></p>` : ''}
                    </div>
                `;

                marker.bindPopup(popupHtml);

                // Do not change zoom or open modal on marker click
                // Leaflet will open the bound popup by default
                this.markers.addLayer(marker);
            });

            // If we added markers, fit the map to show them all with padding.
            try {
                const layerCount = this.markers.getLayers().length;
                if (layerCount > 0) {
                    const bounds = this.markers.getBounds();
                    // bounds may be invalid if only a single point; fitBounds handles single-point bounds as well
                    if (bounds && (typeof bounds.isValid === 'function' ? bounds.isValid() : true)) {
                        this.map.fitBounds(bounds, { padding: [50, 50] });
                    }
                } else {
                    // No markers: reset view to user location at default zoom
                    this.map.setView([this.userLat, this.userLon], 12);
                }
            } catch (err) {
                console.warn('Error fitting map to markers:', err);
            }
        },

        // Icon colors by resource type
        getIconColor(type) {
            const colors = {
                food: '#27ae60',
                shelter: '#e74c3c',
                restroom: '#3498db',
                medical: '#9b59b6',
                legal: '#f39c12',
                donation: '#1abc9c',
                other: '#95a5a6'
            };
            return colors[type] || '#95a5a6';
        },

        // Label text (letter) by resource type
        getIconText(type) {
            const icons = {
                food: 'F',
                shelter: 'S',
                restroom: 'R',
                medical: 'M',
                legal: 'L',
                donation: 'D',
                other: 'O'
            };
            return icons[type] || 'O';
        },

        // When user clicks a marker
        selectResource(resource) {
            // Used by list clicks: center on resource and show its popup
            this.selectedResource = resource;
            const coords = resource.geometry.coordinates;
            const lat = coords[1];
            const lon = coords[0];

            // Center map on the selected resource (keep current zoom)
            this.map.panTo([lat, lon]);

            // Find the marker for this resource and open its popup
            const target = this.markers.getLayers().find(m => {
                const p = m.getLatLng && m.getLatLng();
                return p && p.lat === lat && p.lng === lon;
            });
            if (target) {
                if (typeof this.markers.zoomToShowLayer === 'function') {
                    this.markers.zoomToShowLayer(target, () => target.openPopup());
                } else if (target.openPopup) {
                    target.openPopup();
                }
            }
        }
    };
}
