from collections import defaultdict
from datetime import datetime

from django.http.response import JsonResponse

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.parsers import JSONParser

from findyourngo.restapi.models import Ngo, NgoComment, NgoCommenter


@api_view(['GET'])
def tw_rating(request) -> JsonResponse:
    ngo_id = request.query_params.get('id')

    try:
        ngo = Ngo.objects.get(pk=ngo_id)
    except BaseException:
        return JsonResponse({'error': f'NGO with id {ngo_id} does not exist.'}, status=status.HTTP_400_BAD_REQUEST, safe=False)

    comments = NgoComment.objects.filter(ngo=ngo)

    total_tw = ngo.tw_score.total_tw_score
    base_tw = ngo.tw_score.base_tw_score
    user_tw = ngo.tw_score.user_tw_score

    total_comment_number = len(comments)
    comments_by_rating = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
    }

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


def convertComments(comments):
    result = []

    for comment in comments:
        user = comment.commenter
        converted_comment = {
            'id': comment.id,
            'userId': user.user_id,
            'userName': 'NAME', # TODO
            'ngoId': comment.ngo.id,
            'commentsByUser': user.number_of_comments,
            'created': comment.create_date,
            'last_edited': comment.last_edited,
            'rating': comment.rating,
            'text': comment.text
        }
        result.append(converted_comment)

    return result


@api_view(['GET'])
def userReviews(request) -> JsonResponse:
    ngo_id = request.query_params.get('id')

    try:
        ngo = Ngo.objects.get(pk=ngo_id)
    except BaseException:
        return JsonResponse({'error': f'NGO with id {ngo_id} does not exist.'}, status=status.HTTP_400_BAD_REQUEST, safe=False)

    comments = NgoComment.objects.filter(ngo=ngo).order_by('last_edited')

    result = {
        'comments': convertComments(comments),
        'commentNumber': len(comments),
    }
    return JsonResponse(result, safe=False)


@api_view(['GET', 'PUT', 'DELETE'])
def review(request) -> JsonResponse:
    if request.method == 'GET':
        review_id = request.query_params.get('id')
        try:
            comment = NgoComment.objects.get(pk=review_id)
            return JsonResponse(convertComments([comment])[0], safe=False)
        except BaseException:
            return JsonResponse({'error': f'No review found for ID {review_id}'}, status=status.HTTP_400_BAD_REQUEST, safe=False)

    if request.method == 'PUT':
        review = JSONParser().parse(request)
        try:
            user_id = review['userId']
            user = NgoCommenter.objects.get(user_id=user_id)
        except BaseException:
            return JsonResponse({'error': f'No user found for ID {user_id}'}, status=status.HTTP_400_BAD_REQUEST, safe=False)

        comment_id = review['commentId']

        if comment_id is not None:
            return update_comment(comment_id, review)
        else:
            return save_new_comment(review, user)


    if request.method == 'DELETE':
        review_id = request.query_params.get('id')
        comment = NgoComment.objects.get(pk=review_id)
        comment.commenter.number_of_comments -= 1
        comment.commenter.save()
        comment.delete()
        return JsonResponse({'message': 'Review was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


def update_comment(comment_id, review) -> JsonResponse:
    rating = review['rating']
    text = review['text']

    update_time = datetime.now()

    try:
        comment = NgoComment.objects.get(pk=comment_id)
        comment.text = text
        comment.rating = rating
        comment.last_edited = update_time
        comment.save()
        return JsonResponse({'message': 'Review successfully updated'}, status=status.HTTP_200_OK)
    except BaseException:
        return JsonResponse({'error': f'No review found for id {comment_id}'}, status=status.HTTP_400_BAD_REQUEST)


def save_new_comment(review, user) -> JsonResponse:
    try:
        ngo_id = review['ngoId']
        rating = review['rating']
        text = review['text']

        create_time = datetime.now()

        ngo = Ngo.objects.get(pk=ngo_id)

        NgoComment.objects.create(
            ngo=ngo,
            commenter=user,
            create_date=create_time,
            last_edited=create_time,
            text=text,
            rating=rating,
        )

        user.number_of_comments += 1
        user.save()
        return JsonResponse(data={'message': 'Review was successfully stored.'}, status=status.HTTP_200_OK)

    except BaseException as err:
        return JsonResponse({'error': f'Review could not be stored: {err}.'}, status=status.HTTP_400_BAD_REQUEST,
                        safe=False)