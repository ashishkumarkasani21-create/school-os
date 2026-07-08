import math
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import Bus, Route, Stop, StudentBusAssignment, BusLocationLog
from school_os.helpers import school_has_feature

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
        'routes': routes,
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

    return JsonResponse({
        'status': 'live',
        'latitude': lat + offset_lat,
        'longitude': lon + offset_lng,
        'current_stop': start_stop.name,
        'next_stop': end_stop.name,
        'eta_next': f"{int(max(5, (1.0 - fraction) * seconds_per_segment / 2))} mins"
    })
