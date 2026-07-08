from django.test import TestCase
from django.contrib.auth import get_user_model
from schools.models import School, SubscriptionPlan
from school_os.helpers import school_has_feature

User = get_user_model()

class SchoolOSCoreTests(TestCase):
    def setUp(self):
        # Create Plans
        self.silver_plan = SubscriptionPlan.objects.create(
            name="Silver Plan",
            code="silver",
            features_json='["attendance", "homework", "announcements"]'
        )
        self.platinum_plan = SubscriptionPlan.objects.create(
            name="Platinum Plan",
            code="platinum",
            features_json='["attendance", "homework", "announcements", "live_bus_tracking", "ocr_advanced"]'
        )

        # Create Schools
        self.silver_school = School.objects.create(
            name="Silver Academy",
            code="silver-academy",
            plan=self.silver_plan
        )
        self.platinum_school = School.objects.create(
            name="Platinum College",
            code="platinum-college",
            plan=self.platinum_plan
        )

    def test_user_creation_and_roles(self):
        """Verify users can be created with correct roles and linked to a school."""
        student_user = User.objects.create_user(
            username="stud_test",
            password="testpassword",
            role="student",
            school=self.silver_school
        )
        self.assertEqual(student_user.role, "student")
        self.assertEqual(student_user.school, self.silver_school)
        self.assertTrue(student_user.check_password("testpassword"))

    def test_feature_gating_logic(self):
        """Verify school_has_feature functions correctly based on active plan."""
        # Silver school should have attendance, but not live bus tracking
        self.assertTrue(school_has_feature(self.silver_school, 'attendance'))
        self.assertFalse(school_has_feature(self.silver_school, 'live_bus_tracking'))
        
        # Platinum school should have both
        self.assertTrue(school_has_feature(self.platinum_school, 'attendance'))
        self.assertTrue(school_has_feature(self.platinum_school, 'live_bus_tracking'))
        
        # Test inactive school has no features
        self.silver_school.is_active = False
        self.silver_school.save()
        self.assertFalse(school_has_feature(self.silver_school, 'attendance'))
