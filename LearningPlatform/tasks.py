from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_test_result_notification(test_result_id):
    from courses.models import TestResult
    try:
        test_result = TestResult.objects.get(id=test_result_id)
        logger.info(f"Notification sent for TestResult {test_result.id}: {test_result.score}")
        return f"Notification sent for TestResult {test_result.id}"
    except TestResult.DoesNotExist:
        logger.error(f"TestResult {test_result_id} not found")
        return f"TestResult {test_result_id} not found"
