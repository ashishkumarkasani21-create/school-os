def school_features(request):
    """
    Context processor that injects school info and active feature flags 
    into all templates based on the logged-in user's school subscription.
    """
    if request.user.is_authenticated and hasattr(request.user, 'school') and request.user.school:
        school = request.user.school
        from school_os.helpers import PLAN_FEATURES
        plan_code = school.plan.code.lower() if school.plan else 'silver'
        features = PLAN_FEATURES.get(plan_code, PLAN_FEATURES['silver'])
        
        # Build a helper dictionary for templates to check like: {% if school_features.ocr_advanced %}
        feature_map = {feat: True for feat in features}
        return {
            'current_school': school,
            'school_features': feature_map,
            'school_plan': plan_code,
        }
    return {
        'current_school': None,
        'school_features': {},
        'school_plan': 'silver',
    }
