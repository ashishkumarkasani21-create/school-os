import math
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import Bus, Route, Stop, StudentBusAssignment, BusLocationLog
from school_os.helpers import school_has_feature

ROUTE_LOCALIZATIONS = {
    'IN': {
        'Downtown East Route': 'Connaught Place Route',
        'East Terminal Start': 'New Delhi Central Hub',
        'Main Street Stop': 'Rajiv Chowk Crossing',
        'Grand Avenue Stop': 'India Gate Boulevard',
        'Elite School Campus Entrance': 'Silver Jubilee School Gate',
        'North Hill Route': 'Noida Sector 62 Route',
        'North Hill Stop 1': 'Sec-62 Metro Stop',
        'North Hill Stop 2': 'Fortis Crossing Stop',
        'North Hill Campus Stop': 'Amity Campus Stop',
        'West Coast Route': 'Gurgaon Expressway Route',
        'West Coast Stop 1': 'Cyber City Terminal',
        'West Coast Stop 2': 'IFFCO Chowk Crossing',
        'West Coast Campus Stop': 'DLF Phase 3 Stop',
    },
    'US': {
        'Downtown East Route': 'Downtown East Route',
        'East Terminal Start': 'East Terminal Start',
        'Main Street Stop': 'Main Street Stop',
        'Grand Avenue Stop': 'Grand Avenue Stop',
        'Elite School Campus Entrance': 'Elite School Campus Entrance',
        'North Hill Route': 'North Hill Route',
        'North Hill Stop 1': 'North Hill Stop 1',
        'North Hill Stop 2': 'North Hill Stop 2',
        'North Hill Campus Stop': 'North Hill Campus Stop',
        'West Coast Route': 'West Coast Route',
        'West Coast Stop 1': 'West Coast Stop 1',
        'West Coast Stop 2': 'West Coast Stop 2',
        'West Coast Campus Stop': 'West Coast Campus Stop',
    },
    'GB': {
        'Downtown East Route': 'London Bridge Expressway',
        'East Terminal Start': 'King\'s Cross Station',
        'Main Street Stop': 'Piccadilly Circus Circle',
        'Grand Avenue Stop': 'Trafalgar Square Junction',
        'Elite School Campus Entrance': 'Royal Academy Front Gate',
        'North Hill Route': 'Hampstead Heath Route',
        'North Hill Stop 1': 'Highgate Metro Stop',
        'North Hill Stop 2': 'Golders Green Junction',
        'North Hill Campus Stop': 'Hampstead Park Stop',
        'West Coast Route': 'Thames Valley Route',
        'West Coast Stop 1': 'Richmond Green Terminal',
        'West Coast Stop 2': 'Kew Gardens Crossing',
        'West Coast Campus Stop': 'Kingston Riverside Stop',
    },
    'CA': {
        'Downtown East Route': 'Toronto Harbour Route',
        'East Terminal Start': 'Union Station Hub',
        'Main Street Stop': 'Yonge-Dundas Plaza',
        'Grand Avenue Stop': 'CN Tower Parkway',
        'Elite School Campus Entrance': 'Ontario College Entrance',
        'North Hill Route': 'Scarborough Bluffs Route',
        'North Hill Stop 1': 'Kennedy Subway Stop',
        'North Hill Stop 2': 'Guildwood Crossing',
        'North Hill Campus Stop': 'Bluffs Park Stop',
        'West Coast Route': 'Mississauga Transit Route',
        'West Coast Stop 1': 'Square One Terminal',
        'West Coast Stop 2': 'Port Credit Crossing',
        'West Coast Campus Stop': 'Lakeshore Road Stop',
    },
    'EU': {
        'Downtown East Route': 'Seine Paris Rive Gauche',
        'East Terminal Start': 'Gare du Nord Terminal',
        'Main Street Stop': 'Champs-Élysées Avenue',
        'Grand Avenue Stop': 'Place de la Concorde',
        'Elite School Campus Entrance': 'Académie de Paris Gate',
        'North Hill Route': 'Montmartre Route',
        'North Hill Stop 1': 'Sacré-Cœur Metro',
        'North Hill Stop 2': 'Pigalle Crossing',
        'North Hill Campus Stop': 'Place du Tertre Stop',
        'West Coast Route': 'Versailles Route',
        'West Coast Stop 1': 'Palais de Versailles',
        'West Coast Stop 2': 'Grand Trianon Crossing',
        'West Coast Campus Stop': 'Le Parc Stop',
    }
}

@login_required
def bus_tracking_map(request):
    school = request.user.school
    
    # Feature gate: Live bus tracking is a Premium feature
    has_premium_tracking = school_has_feature(school, 'live_bus_tracking')
    
    routes = Route.objects.filter(school=school).prefetch_related('stops')
    buses = Bus.objects.filter(school=school, status='active')

    # Get country from session, default to IN
    selected_country = request.session.get('selected_country', 'IN')
    country_centers = {
        'IN': {'lat': 28.6139, 'lng': 77.2090, 'name': 'Delhi'},
        'US': {'lat': 34.0522, 'lng': -118.2437, 'name': 'Los Angeles'},
        'GB': {'lat': 51.5074, 'lng': -0.1278, 'name': 'London'},
        'CA': {'lat': 43.6532, 'lng': -79.3832, 'name': 'Toronto'},
        'EU': {'lat': 48.8566, 'lng': 2.3522, 'name': 'Paris'},
    }
    center = country_centers.get(selected_country, country_centers['IN'])
    offset_lat = center['lat'] - 34.0522
    offset_lng = center['lng'] - (-118.2437)

    # Localize routes and stop names
    local_map = ROUTE_LOCALIZATIONS.get(selected_country, ROUTE_LOCALIZATIONS['IN'])
    localized_routes = []
    for r in routes:
        loc_stops = []
        for s in r.stops.all().order_by('sequence_order'):
            loc_stops.append({
                'id': s.id,
                'name': local_map.get(s.name, s.name),
                'latitude': s.latitude,
                'longitude': s.longitude,
                'arrival_time': s.arrival_time,
                'sequence_order': s.sequence_order,
            })
        localized_routes.append({
            'id': r.id,
            'name': local_map.get(r.name, r.name),
            'bus': r.bus,
            'driver': r.driver,
            'stops': loc_stops,
        })

    # Get student's specific route if logged in as student or parent
    assigned_route = None
    if request.user.role == 'student':
        assignment = StudentBusAssignment.objects.filter(student=request.user.student_profile).first()
        if assignment: assigned_route = assignment.route
    elif request.user.role == 'parent':
        first_child = request.user.parent_profile.children.first()
        if first_child:
            assignment = StudentBusAssignment.objects.filter(student=first_child).first()
            if assignment: assigned_route = assignment.route

    return render(request, 'transport/bus_tracking.html', {
        'routes': localized_routes,
        'buses': buses,
        'assigned_route': assigned_route,
        'has_premium_tracking': has_premium_tracking,
        'map_center_lat': center['lat'],
        'map_center_lng': center['lng'],
        'offset_lat': offset_lat,
        'offset_lng': offset_lng,
    })

def interpolate_coordinates(lat1, lon1, lat2, lon2, fraction):
    """
    Linearly interpolates between two latitude/longitude points.
    """
    lat = lat1 + (lat2 - lat1) * fraction
    lon = lon1 + (lon2 - lon1) * fraction
    return lat, lon

def get_bus_live_coords(request, bus_id):
    """
    API endpoint that returns simulated live coordinates of a bus moving along its route stops.
    It calculates position based on the current system time to generate active movement.
    """
    bus = get_object_or_404(Bus, id=bus_id)
    route = Route.objects.filter(bus=bus).first()
    
    if not route:
        return JsonResponse({'status': 'offline', 'error': 'No active route assigned to this bus.'})

    # Retrieve country from session to calculate offset
    selected_country = request.session.get('selected_country', 'IN')
    country_centers = {
        'IN': {'lat': 28.6139, 'lng': 77.2090},
        'US': {'lat': 34.0522, 'lng': -118.2437},
        'GB': {'lat': 51.5074, 'lng': -0.1278},
        'CA': {'lat': 43.6532, 'lng': -79.3832},
        'EU': {'lat': 48.8566, 'lng': 2.3522},
    }
    center = country_centers.get(selected_country, country_centers['IN'])
    offset_lat = center['lat'] - 34.0522
    offset_lng = center['lng'] - (-118.2437)

    stops = list(route.stops.all().order_by('sequence_order'))
    if len(stops) < 2:
        lat = 34.0522
        lon = -118.2437
        if stops:
            lat, lon = stops[0].latitude, stops[0].longitude
        return JsonResponse({
            'status': 'live', 
            'latitude': lat + offset_lat, 
            'longitude': lon + offset_lng, 
            'eta_next': '10 mins'
        })

    # Pre-defined path coordinates interpolation logic
    # Use current time seconds (0 to 59) to progress along the path
    now = timezone.now()
    seconds = now.second + (now.microsecond / 1000000.0)
    
    # Let one full loop of all stops take 60 seconds
    num_segments = len(stops) - 1
    seconds_per_segment = 60.0 / num_segments
    
    segment_idx = int(seconds / seconds_per_segment)
    if segment_idx >= num_segments:
        segment_idx = num_segments - 1
        
    segment_seconds = seconds - (segment_idx * seconds_per_segment)
    fraction = segment_seconds / seconds_per_segment

    # Ensure loop works backwards or smoothly if overflow
    start_stop = stops[segment_idx]
    end_stop = stops[segment_idx + 1]
    
    lat, lon = interpolate_coordinates(
        start_stop.latitude, start_stop.longitude,
        end_stop.latitude, end_stop.longitude,
        fraction
    )

    # Log location to database for audit history
    BusLocationLog.objects.create(bus=bus, latitude=lat + offset_lat, longitude=lon + offset_lng)

    local_map = ROUTE_LOCALIZATIONS.get(selected_country, ROUTE_LOCALIZATIONS['IN'])
    current_stop_localized = local_map.get(start_stop.name, start_stop.name)
    next_stop_localized = local_map.get(end_stop.name, end_stop.name)

    return JsonResponse({
        'status': 'live',
        'latitude': lat + offset_lat,
        'longitude': lon + offset_lng,
        'current_stop': current_stop_localized,
        'next_stop': next_stop_localized,
        'eta_next': f"{int(max(5, (1.0 - fraction) * seconds_per_segment / 2))} mins"
    })
