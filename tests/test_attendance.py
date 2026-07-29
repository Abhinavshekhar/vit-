from apps.api.astra_os.services.attendance import AttendanceSnapshot, attendance_recommendation, safe_skip_count


def test_safe_skip_count_at_healthy_attendance():
    assert safe_skip_count(AttendanceSnapshot(attended=18, total=20, minimum_percent=75)) == 4


def test_recommend_attend_below_threshold():
    recommendation = attendance_recommendation(AttendanceSnapshot(attended=6, total=10, minimum_percent=75))
    assert recommendation["action"] == "attend"
    assert recommendation["classes_needed"] > 0
