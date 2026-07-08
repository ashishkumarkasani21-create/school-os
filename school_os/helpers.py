# Plan feature definitions
PLAN_FEATURES = {
    'silver': {
        'academics_basic',
        'attendance',
        'homework',
        'announcements',
        'fee_view',
    },
    'gold': {
        'academics_basic',
        'attendance',
        'homework',
        'announcements',
        'fee_view',
        'accounting_reports',
        'timetable',
        'exams',
        'leave_requests',
        'ocr_basic',
        'bus_static',
    },
    'platinum': {
        'academics_basic',
        'attendance',
        'homework',
        'announcements',
        'fee_view',
        'accounting_reports',
        'timetable',
        'exams',
        'leave_requests',
        'ocr_basic',
        'bus_static',
        'ocr_advanced',
        'live_bus_tracking',
        'advanced_analytics',
        'audit_logs',
    }
}

def school_has_feature(school, feature_name):
    """
    Checks if a school has access to a specific feature based on its subscription plan.
    """
    if not school or not school.is_active:
        return False
    
    # Get subscription plan (default to silver if not set)
    plan_code = 'silver'
    if school.plan:
        plan_code = school.plan.code.lower()
    
    features = PLAN_FEATURES.get(plan_code, PLAN_FEATURES['silver'])
    return feature_name in features
