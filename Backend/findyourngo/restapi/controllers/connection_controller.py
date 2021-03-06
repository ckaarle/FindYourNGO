from datetime import datetime

from django.http.response import JsonResponse
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from findyourngo.restapi.models import NgoPendingConnection, NgoConnection, NgoAccount, Ngo
from findyourngo.restapi.serializers.ngo_serializer import NgoSerializer


@api_view(['GET'])
def view_connections(request) -> JsonResponse:
    try:
        requested_ngo = request.query_params.get('requested_ngo')
        ngos = Ngo.objects.filter(connected_ngo__reporter=requested_ngo)
        ngo_serializer = NgoSerializer(ngos, many=True)
        return JsonResponse(ngo_serializer.data, safe=False)  # TODO: Use pagination
    except Exception as e:
        print(e)
        return forbidden_response()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_incoming_pending_connections(request) -> JsonResponse:
    try:
        requesting_ngo = NgoAccount.objects.get(user__id=request.user.id).ngo
        ngos = Ngo.objects.filter(reporter_pending__connected_ngo=requesting_ngo)
        ngo_serializer = NgoSerializer(ngos, many=True)
        return JsonResponse(ngo_serializer.data, safe=False)  # TODO: Use pagination
    except Exception as e:
        print(e)
        return forbidden_response()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_outgoing_pending_connections(request) -> JsonResponse:
    try:
        requesting_ngo = NgoAccount.objects.get(user__id=request.user.id).ngo
        ngos = Ngo.objects.filter(connected_ngo_pending__reporter=requesting_ngo)
        ngo_serializer = NgoSerializer(ngos, many=True)
        return JsonResponse(ngo_serializer.data, safe=False)  # TODO: Use pagination
    except Exception as e:
        print(e)
        return forbidden_response()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_connection_type(request, requested_ngo) -> JsonResponse:
    try:
        reporter = NgoAccount.objects.get(user__id=request.user.id).ngo.id
        if reporter == requested_ngo:
            return JsonResponse({'type': 'self'})
        if len(list(NgoConnection.objects.filter(reporter_id=reporter, connected_ngo_id=requested_ngo))) > 0:
            return JsonResponse({'type': 'connected'})
        if len(list(NgoPendingConnection.objects.filter(reporter_id=reporter, connected_ngo_id=requested_ngo))) > 0:
            return JsonResponse({'type': 'requesting'})
        if len(list(NgoPendingConnection.objects.filter(reporter_id=requested_ngo, connected_ngo_id=reporter))) > 0:
            return JsonResponse({'type': 'requested'})
        return JsonResponse({'type': 'none'})
    except Exception as e:
        print(e)
        return forbidden_response()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_connection(request) -> JsonResponse:
    try:
        reporter_id = NgoAccount.objects.get(user__id=request.user.id).ngo.id
        connected_ngo_id = request.query_params.get('ngo_id')
        if reporter_id == connected_ngo_id:
            return forbidden_response()
        return create_connection(reporter_id, connected_ngo_id)
    except Exception as e:
        print(e)
        return forbidden_response()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_connection(request) -> JsonResponse:
    try:
        reporter_id = NgoAccount.objects.get(user__id=request.user.id).ngo.id
        connected_ngo_id = request.query_params.get('ngo_id')
        return delete_connection(reporter_id, connected_ngo_id)
    except Exception as e:
        print(e)
        return forbidden_response()


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
