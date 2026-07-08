def school_features(request):
    """
    Context processor that injects school info and active feature flags 
    into all templates based on the logged-in user's school subscription.
    """
    # Active currency configuration based on country selection
    selected_country = request.session.get('selected_country', 'IN')
    country_currencies = {
        'IN': {'name': 'India', 'symbol': '₹', 'silver': '50,000', 'gold': '75,000', 'platinum': '1,00,000', 'tax': '18% GST'},
        'US': {'name': 'United States', 'symbol': '$', 'silver': '699', 'gold': '999', 'platinum': '1,399', 'tax': '0% Sales Tax'},
        'GB': {'name': 'United Kingdom', 'symbol': '£', 'silver': '549', 'gold': '799', 'platinum': '1,099', 'tax': '20% VAT'},
        'CA': {'name': 'Canada', 'symbol': 'C$', 'silver': '899', 'gold': '1,299', 'platinum': '1,799', 'tax': '5% GST'},
        'EU': {'name': 'Europe', 'symbol': '€', 'silver': '599', 'gold': '849', 'platinum': '1,199', 'tax': '19% MwSt.'},
    }
    active_currency = country_currencies.get(selected_country, country_currencies['IN'])

    base_context = {
        'selected_country': selected_country,
        'active_currency': active_currency,
    }

    if request.user.is_authenticated and hasattr(request.user, 'school') and request.user.school:
        school = request.user.school
        from school_os.helpers import PLAN_FEATURES
        plan_code = school.plan.code.lower() if school.plan else 'silver'
        features = PLAN_FEATURES.get(plan_code, PLAN_FEATURES['silver'])
        
        # Build a helper dictionary for templates to check like: {% if school_features.ocr_advanced %}
        feature_map = {feat: True for feat in features}
        base_context.update({
            'current_school': school,
            'school_features': feature_map,
            'school_plan': plan_code,
        })
        return base_context
        
    base_context.update({
        'current_school': None,
        'school_features': {},
        'school_plan': 'silver',
    })
    return base_context
