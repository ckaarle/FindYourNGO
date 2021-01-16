from datetime import datetime

from django.http.response import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from findyourngo.restapi.controllers.connection_controller import is_user_authorized, forbidden_response,\
    create_connection
from findyourngo.restapi.models import NgoEvent, NgoEventCollaborator


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_events(request) -> JsonResponse:
    collaborator_id = request.query_params.get('collaborator_id')
    if not is_user_authorized(request, collaborator_id):
        return forbidden_response()
    return JsonResponse(NgoEvent.objects.filter(ngoeventcollaborator__collaborator=collaborator_id)
                        .filter(ngoeventcollaborator__pending=False))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_invitations(request) -> JsonResponse:
    collaborator_id = request.query_params.get('collaborator_id')
    if not is_user_authorized(request, collaborator_id):
        return forbidden_response()
    return JsonResponse(NgoEvent.objects.filter(ngoeventcollaborator__collaborator=collaborator_id)
                        .filter(ngoeventcollaborator__pending=True))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event(request) -> JsonResponse:
    founder_id = request.query_params.get('collaborator_id')
    if not is_user_authorized(request, founder_id):
        return forbidden_response()

    event_name = request.query_params.get('event_name')
    current_date = datetime.now()
    collaborators = request.query_params.get('collaborators')

    try:
        event = NgoEvent.objects.create(name=event_name, date=current_date, organizer=founder_id)
        NgoEventCollaborator.objects.create(event=event, collaborators=founder_id, pending=False)

        for collaborator_id in collaborators:
            NgoEventCollaborator.objects.create(event=event, collaborators=collaborator_id)
            create_connection(founder_id, collaborator_id)

        return JsonResponse({'success': 'Event created successfully'})

    except Exception:
        return JsonResponse({'error': 'Event creation failed'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_event(request) -> JsonResponse:
    founder_id = request.query_params.get('collaborator_id')
    if not is_user_authorized(request, founder_id):
        return forbidden_response()

    event_id = request.query_params.get('event_id')

    try:
        event = NgoEvent.objects.get(id=event_id)
        if founder_id != event.organizer:
            return forbidden_response()

        event.delete()
        return JsonResponse({'success': 'Event deleted successfully'})

    except Exception:
        return JsonResponse({'error': 'Event deletion failed'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def invite_to_event(request) -> JsonResponse:
    founder_id = request.query_params.get('collaborator_id')
    if not is_user_authorized(request, founder_id):
        return forbidden_response()

    event_id = request.query_params.get('event_id')
    collaborators = request.query_params.get('collaborators')

    try:
        event = NgoEvent.objects.get(id=event_id)
        if founder_id != event.organizer:
            return forbidden_response()

        for collaborator_id in collaborators:
            NgoEventCollaborator.objects.create(event=event, collaborator=collaborator_id)
            create_connection(founder_id, collaborator_id)

        return JsonResponse({'success': 'Invitations sent successfully'})

    except Exception:
        return JsonResponse({'error': 'Inviting failed'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_event(request) -> JsonResponse:
    collaborator_id = request.query_params.get('collaborator_id')
    if not is_user_authorized(request, collaborator_id):
        return forbidden_response()

    event_id = request.query_params.get('event_id')
    try:
        event = NgoEvent.objects.get(id=event_id)
        invitation = NgoEventCollaborator.objects.get(event=event, collaborator=collaborator_id)
        if not invitation.pending:
            return JsonResponse({'error': 'Invitation already accepted'})

        invitation.pending = False
        create_connection(collaborator_id, event.organizer)
        return JsonResponse({'success': 'Invitation accepted'})

    except Exception:
        return JsonResponse({'error': 'Invitation could not be accepted'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_event(request) -> JsonResponse:
    collaborator_id = request.query_params.get('collaborator_id')
    if not is_user_authorized(request, collaborator_id):
        return forbidden_response()

    event_id = request.query_params.get('event_id')
    try:
        event = NgoEvent.objects.get(id=event_id)
        invitation = NgoEventCollaborator.objects.get(event=event, collaborator=collaborator_id)
        invitation.delete()
        return JsonResponse({'success': 'Event rejected'})

    except Exception:
        return JsonResponse({'error': 'Invitation or event could not be found'})
