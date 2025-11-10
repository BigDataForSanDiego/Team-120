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
        
        // User location
        userLat: 32.7157,  // Default to San Diego
        userLon: -117.1611,
        userAddress: '',
        
        // Filters
        resourceTypes: [
            { value: 'food', label: 'Food' },
            { value: 'shelter', label: 'Shelter' },
            { value: 'restroom', label: 'Restroom' },
            { value: 'medical', label: 'Medical' },
            { value: 'legal', label: 'Legal' },
            { value: 'donation', label: 'Donation' },
            { value: 'other', label: 'Other' }
        ],
        selectedTypes: [],
        openNow: false,
        radiusMiles: 5,
        
        // Initialize
        init() {
            this.initMap();
            this.updateFilters();
        },
        
        // Initialize Leaflet map
        initMap() {
            this.map = L.map('map').setView([this.userLat, this.userLon], 12);
            
            // Add OpenStreetMap tiles
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                maxZoom: 19
            }).addTo(this.map);
            
            // Initialize marker cluster group
            this.markers = L.markerClusterGroup();
            this.map.addLayer(this.markers);
            
            // Add user location marker
            this.updateUserMarker();
        },
        
        // Update user location marker
        updateUserMarker() {
            if (this.userMarker) {
                this.map.removeLayer(this.userMarker);
            }
            
            const userIcon = L.divIcon({
                className: 'user-location-icon',
                html: '<div style="background: #3498db; width: 20px; height: 20px; border-radius: 50%; border: 3px solid white; box-shadow: 0 0 10px rgba(0,0,0,0.3);"></div>',
                iconSize: [20, 20]
            });
            
            this.userMarker = L.marker([this.userLat, this.userLon], { icon: userIcon })
                .addTo(this.map);
        },
        
        // Get user's current location
        getUserLocation() {
            if (navigator.geolocation) {
                this.loading = true;
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        this.userLat = position.coords.latitude;
                        this.userLon = position.coords.longitude;
                        this.map.setView([this.userLat, this.userLon], 13);
                        this.updateUserMarker();
                        this.updateFilters();
                        this.loading = false;
                    },
                    (error) => {
                        console.error('Error getting location:', error);
                        alert('Could not get your location. Using default location.');
                        this.loading = false;
                    }
                );
            } else {
                alert('Geolocation is not supported by your browser.');
            }
        },
        
        // Toggle resource type filter
        toggleType(type) {
            const index = this.selectedTypes.indexOf(type);
            if (index > -1) {
                this.selectedTypes.splice(index, 1);
            } else {
                this.selectedTypes.push(type);
            }
            this.updateFilters();
        },
        
        // Update filters and fetch resources
        async updateFilters() {
            this.loading = true;
            
            // Build query parameters
            const params = new URLSearchParams();
            params.append('lat', this.userLat);
            params.append('lon', this.userLon);
            params.append('radius_m', this.radiusMiles * 1609.34); // Convert miles to meters
            
            if (this.selectedTypes.length > 0) {
                params.append('rtype', this.selectedTypes.join(','));
            }
            
            if (this.openNow) {
                params.append('open_now', 'true');
            }
            
            try {
                const response = await fetch(`/api/resources/?${params.toString()}`);
                const data = await response.json();
                this.resources = data.features || [];
                this.updateMarkers();
            } catch (error) {
                console.error('Error fetching resources:', error);
                alert('Error loading resources. Please try again.');
            } finally {
                this.loading = false;
            }
        },
        
        // Update map markers
        updateMarkers() {
            // Clear existing markers
            this.markers.clearLayers();
            
            // Add new markers
            this.resources.forEach(resource => {
                const coords = resource.geometry.coordinates;
                const lat = coords[1];
                const lon = coords[0];
                
                // Create custom icon based on type
                const iconColor = this.getIconColor(resource.properties.rtype);
                const icon = L.divIcon({
                    className: 'resource-marker',
                    html: `<div style="background: ${iconColor}; width: 30px; height: 30px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px;">${this.getIconText(resource.properties.rtype)}</div>`,
                    iconSize: [30, 30]
                });
                
                const marker = L.marker([lat, lon], { icon: icon });
                
                // Add popup
                marker.bindPopup(`
                    <div style="min-width: 200px;">
                        <h3 style="margin: 0 0 0.5rem 0;">${resource.properties.name}</h3>
                        <p style="margin: 0.25rem 0; text-transform: capitalize;">${resource.properties.rtype}</p>
                        <p style="margin: 0.25rem 0; font-size: 0.9rem;">${resource.properties.address || 'No address'}</p>
                        ${resource.properties.is_open_now === true ? '<span style="color: green; font-weight: bold;">Open Now</span>' : ''}
                        ${resource.properties.is_open_now === false ? '<span style="color: red; font-weight: bold;">Closed</span>' : ''}
                    </div>
                `);
                
                // Add click handler
                marker.on('click', () => {
                    this.selectResource(resource);
                });
                
                this.markers.addLayer(marker);
            });
        },
        
        // Get icon color based on resource type
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
        
        // Get icon text based on resource type
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
        
        // Select a resource to show details
        selectResource(resource) {
            this.selectedResource = resource;
            
            // Center map on selected resource
            const coords = resource.geometry.coordinates;
            this.map.setView([coords[1], coords[0]], 15);
        }
    };
}
