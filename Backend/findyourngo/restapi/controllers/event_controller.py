from datetime import datetime

from django.http.response import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser

from findyourngo.restapi.controllers.connection_controller import forbidden_response, create_connection
from findyourngo.restapi.models import NgoEvent, NgoEventCollaborator, NgoAccount
from findyourngo.restapi.serializers.ngo_serializer import NgoEventSerializer


@api_view(['GET'])
def view_events(request) -> JsonResponse:
    collaborator_id = request.query_params.get('collaborator_id')
    ngo_events = NgoEvent.objects.filter(
        ngoeventcollaborator__collaborator_id=collaborator_id, ngoeventcollaborator__pending=False).union(
        NgoEvent.objects.filter(organizer_id=collaborator_id)
    )
    event_serializer = NgoEventSerializer(ngo_events, many=True)
    return JsonResponse(event_serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_invitations(request) -> JsonResponse:
    try:
        collaborator_id = NgoAccount.objects.get(user__id=request.user.id).ngo.id
        ngo_events = NgoEvent.objects.filter(
            ngoeventcollaborator__collaborator_id=collaborator_id, ngoeventcollaborator__pending=True)
        event_serializer = NgoEventSerializer(ngo_events, many=True)
        return JsonResponse(event_serializer.data, safe=False)
    except:
        return forbidden_response()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event(request) -> JsonResponse:
    try:
        founder_id = NgoAccount.objects.get(user__id=request.user.id).ngo.id
        event_request = JSONParser().parse(request)

        event_name = event_request['event_name']
        start_date = event_request['start_date']
        end_date = event_request['end_date']
        if start_date is None:
            start_date = end_date
        if end_date is None:
            end_date = start_date
        description = event_request['description']
        tags = event_request['tags']
        collaborators = event_request['collaborators']

        event = NgoEvent.objects.create(name=event_name, start_date=start_date, end_date=end_date,
                                        organizer_id=founder_id, description=description, tags=tags)
        NgoEventCollaborator.objects.create(event=event, collaborator_id=founder_id, pending=False)

        for collaborator_id in collaborators:
            NgoEventCollaborator.objects.create(event=event, collaborator_id=collaborator_id)
            create_connection(founder_id, collaborator_id)

        return JsonResponse({'success': 'Event created successfully'})

    except Exception:
        return JsonResponse({'error': 'Event creation failed'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_event(request) -> JsonResponse:
    try:
        founder_id = NgoAccount.objects.get(user__id=request.user.id).ngo.id
        event_request = JSONParser().parse(request)
        event_id = event_request['event_id']
        event = NgoEvent.objects.get(id=event_id)

        if founder_id != event.organizer.id:
            return forbidden_response()

        event.delete()
        return JsonResponse({'success': 'Event deleted successfully'})

    except:
        return JsonResponse({'error': 'Event deletion failed'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def invite_to_event(request) -> JsonResponse:
    try:
        founder_id = NgoAccount.objects.get(user__id=request.user.id).ngo.id
        event_id = request.query_params.get('event_id')
        event = NgoEvent.objects.get(id=event_id)
        if founder_id != event.organizer:
            return forbidden_response()

        collaborators = request.query_params.get('collaborators')
        for collaborator_id in collaborators:
            NgoEventCollaborator.objects.create(event=event, collaborator=collaborator_id)
            create_connection(founder_id, collaborator_id)

        return JsonResponse({'success': 'Invitations sent successfully'})

    except Exception:
        return JsonResponse({'error': 'Inviting failed'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_event(request) -> JsonResponse:
    try:
        collaborator_id = NgoAccount.objects.get(user__id=request.user.id).ngo.id
        event_id = request.query_params.get('event_id')
        event = NgoEvent.objects.get(id=event_id)
        invitation = NgoEventCollaborator.objects.get(event_id=event, collaborator=collaborator_id)
        if not invitation.pending:
            return JsonResponse({'error': 'Invitation already accepted'})

        invitation.pending = False
        invitation.save()
        create_connection(collaborator_id, event.organizer_id)
        return JsonResponse({'success': 'Invitation accepted'})

    except:
        return JsonResponse({'error': 'Invitation could not be accepted'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_event(request) -> JsonResponse:
    try:
        collaborator_id = NgoAccount.objects.get(user__id=request.user.id).ngo.id
        event_id = request.query_params.get('event_id')
        event = NgoEvent.objects.get(id=event_id)
        invitation = NgoEventCollaborator.objects.get(event=event, collaborator=collaborator_id)
        invitation.delete()
        return JsonResponse({'success': 'Event rejected'})

    except Exception:
        return JsonResponse({'error': 'Invitation or event could not be found'})
