from collections import defaultdict

from django.http.response import JsonResponse

from rest_framework.decorators import api_view
from rest_framework import status

from findyourngo.restapi.models import Ngo, NgoComment


@api_view(['GET'])
def tw_rating(request) -> JsonResponse:
    ngo_id = request.query_params.get('id')
    print(f'-----------------{ngo_id}')

    try:
        ngo = Ngo.objects.get(pk=ngo_id)
    except BaseException:
        return JsonResponse({'error': f'No comments found for NGO with id {ngo_id}'}, status=status.HTTP_400_BAD_REQUEST, safe=False)

    comments = NgoComment.objects.filter(ngo_id=ngo_id)

    total_tw = ngo.tw_score.total_tw_score
    base_tw = ngo.tw_score.base_tw_score
    user_tw = ngo.tw_score.user_tw_score

    total_comment_number = len(comments)
    comments_by_rating = defaultdict(int)

    for comment in comments:
        comments_by_rating[comment.rating] += 1

    result = {
        'totalTrustworthiness': total_tw,
        'baseTrustworthiness': base_tw,
        'userTrustworthiness': user_tw,
        'commentNumberByRating': comments_by_rating,
        'totalCommentNumber': total_comment_number,
    }
    return JsonResponse(result, safe=False)

