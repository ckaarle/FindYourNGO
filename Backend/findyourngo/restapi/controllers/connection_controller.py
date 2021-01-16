from datetime import datetime

from django.http.response import JsonResponse
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from findyourngo.restapi.models import NgoPendingConnection, NgoConnection


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_connections(request) -> JsonResponse:
    reporter_id = request.query_params.get('reporter_id')
    if not is_user_authorized(request, reporter_id):
        return forbidden_response()
    return JsonResponse(NgoConnection.objects.filter(reporter_id=reporter_id))  # TODO: Use pagination


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_incoming_pending_connections(request) -> JsonResponse:
    reporter_id = request.query_params.get('reporter_id')
    if not is_user_authorized(request, reporter_id):
        return forbidden_response()
    return JsonResponse(NgoPendingConnection.objects.filter(connected_ngo_id=reporter_id))  # TODO: Use pagination


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_outgoing_pending_connections(request) -> JsonResponse:
    reporter_id = request.query_params.get('reporter_id')
    if not is_user_authorized(request, reporter_id):
        return forbidden_response()
    return JsonResponse(NgoPendingConnection.objects.filter(reporter_id=reporter_id))  # TODO: Use pagination


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_connection(request) -> JsonResponse:
    reporter_id = request.query_params.get('reporter_id')
    if not is_user_authorized(request, reporter_id):
        return forbidden_response()

    connected_ngo_id = request.query_params.get('connected_ngo_id')
    return create_connection(reporter_id, connected_ngo_id)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_connection(request) -> JsonResponse:
    reporter_id = request.query_params.get('reporter_id')
    if not is_user_authorized(request, reporter_id):
        return JsonResponse({}, status=403)

    connected_ngo_id = request.query_params.get('connected_ngo_id')
    return delete_connection(reporter_id, connected_ngo_id)


def is_user_authorized(request, ngo_id) -> bool:
    try:
        if NgoAccount.objects.get(user=request.user.id) == ngo_id:
            return True
        return False
    except Exception:
        return False


def forbidden_response() -> JsonResponse:
    return JsonResponse({}, status=status.HTTP_403_FORBIDDEN)


def create_connection(reporter_id, connected_ngo_id) -> JsonResponse:
    current_date = datetime.now()
    try:
        NgoConnection.objects.get(reporter_id=reporter_id, connected_ngo_id=connected_ngo_id)
        return JsonResponse({'error': 'Connection already established'})
    except Exception:
        pass

    try:
        NgoPendingConnection.objects.get(reporter_id=reporter_id, connected_ngo_id=connected_ngo_id)
        return JsonResponse({'error': 'Request already pending'})
    except Exception:
        pass

    try:
        prev_request = NgoPendingConnection.objects.get(reporter_id=connected_ngo_id, connected_ngo_id=reporter_id)
        report_date = prev_request.report_date
        NgoConnection.objects.create(reporter_id=reporter_id, connected_ngo_id=connected_ngo_id,
                                     report_date=report_date, approval_date=current_date)
        NgoConnection.objects.create(reporter_id=connected_ngo_id, connected_ngo_id=reporter_id,
                                     report_date=report_date, approval_date=current_date)
        prev_request.delete()
        return JsonResponse({'success': 'Request between NGOs confirmed'})
    except Exception:
        NgoPendingConnection.objects.create(reporter_id=reporter_id, connected_ngo_id=connected_ngo_id,
                                            report_date=current_date)
        return JsonResponse({'success': 'Connection request is now pending'})


def delete_connection(reporter_id, connected_ngo_id) -> JsonResponse:
    try:
        out_connection = NgoConnection.objects.get(reporter_id=reporter_id, connected_ngo_id=connected_ngo_id)
        in_connection = NgoConnection.objects.get(reporter_id=connected_ngo_id, connected_ngo_id=reporter_id)
        out_connection.delete()
        in_connection.delete()
        return JsonResponse({'success': 'Connection removed'})
    except Exception:
        pass

    try:
        prev_request = NgoPendingConnection.objects.get(reporter_id=reporter_id, connected_ngo_id=connected_ngo_id)
        prev_request.delete()
        return JsonResponse({'success': 'Outgoing request removed'})
    except Exception:
        pass

    try:
        prev_request = NgoPendingConnection.objects.get(reporter_id=connected_ngo_id, connected_ngo_id=reporter_id)
        prev_request.delete()
        return JsonResponse({'success': 'Incoming request rejected'})
    except Exception:
        pass

    return JsonResponse({'error': 'No relation between NGOs found'})
