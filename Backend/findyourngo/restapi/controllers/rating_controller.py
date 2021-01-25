from datetime import datetime

from django.http.response import JsonResponse

from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.parsers import JSONParser

from findyourngo.restapi.models import Ngo, NgoReview
from findyourngo.data_import.data_importer import update_ngo_tw_score


@api_view(['GET'])
def tw_rating(request) -> JsonResponse:
    ngo_id = request.query_params.get('id')

    try:
        ngo = Ngo.objects.get(pk=ngo_id)
    except BaseException:
        return JsonResponse({'error': f'NGO with id {ngo_id} does not exist.'}, status=status.HTTP_400_BAD_REQUEST, safe=False)

    reviews = NgoReview.objects.filter(ngo=ngo)

    total_tw = ngo.tw_score.total_tw_score

    total_review_number = len(reviews)
    reviews_by_rating = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
    }

    for review in reviews:
        reviews_by_rating[review.rating] += 1

    result = {
        'totalTrustworthiness': total_tw,
        'reviewNumberByRating': reviews_by_rating,
        'totalReviewNumber': total_review_number,
    }
    return JsonResponse(result, safe=False)


def convert_reviews(reviews):
    result = []

    for review in reviews:
        user = review.reviewer
        converted_comment = {
            'id': review.id,
            'userId': user.id,
            'userName': user.username,
            'ngoId': review.ngo.id,
            'reviewsByUser': len(NgoReview.objects.filter(reviewer=user)),
            'created': review.create_date,
            'last_edited': review.last_edited,
            'rating': review.rating,
            'text': review.text
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

    reviews = NgoReview.objects.filter(ngo=ngo).order_by('last_edited')

    result = {
        'reviews': convert_reviews(reviews),
        'reviewNumber': len(reviews),
    }
    return JsonResponse(result, safe=False)


@api_view(['GET', 'PUT', 'DELETE'])
def review(request) -> JsonResponse:
    if request.method == 'GET':
        review_id = request.query_params.get('id')
        try:
            review = NgoReview.objects.get(pk=review_id)
            return JsonResponse(convert_reviews([review])[0], safe=False)
        except BaseException:
            return JsonResponse({'error': f'No review found for ID {review_id}'}, status=status.HTTP_400_BAD_REQUEST, safe=False)

    if request.method == 'PUT':
        review = JSONParser().parse(request)
        try:
            user_id = review['userId']

            if request.user.id != user_id:
                return JsonResponse({'error': 'Comments can only be stored / edited for the current user.'})

            user = User.objects.get(pk=user_id)
        except BaseException:
            return JsonResponse({'error': f'No user found for ID {user_id}'}, status=status.HTTP_400_BAD_REQUEST, safe=False)

        review_id = review['reviewId']

        if review_id is not None:
            return update_review(review_id, review)
        else:
            return save_new_review(review, user)

    if request.method == 'DELETE':
        review_id = request.query_params.get('id')
        review = NgoReview.objects.get(pk=review_id)

        user_id = review.reviewer.id
        if request.user.id != user_id:
            return JsonResponse({'error': 'Only own comments can be deleted.'})

        review.delete()
        ngo = Ngo.objects.get(pk=review.ngo.id)
        ngo.number_of_reviews -= 1
        ngo.save()
        update_ngo_tw_score(ngo)
        return JsonResponse({'message': 'Review was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


def update_review(review_id, review) -> JsonResponse:
    rating = review['rating']
    text = review['text']

    update_time = datetime.now()

    try:
        review = NgoReview.objects.get(pk=review_id)
        review.text = text
        review.rating = rating
        review.last_edited = update_time
        review.save()
        update_ngo_tw_score(Ngo.objects.get(pk=review.ngo.id))
        return JsonResponse({'message': 'Review successfully updated'}, status=status.HTTP_200_OK)
    except BaseException:
        return JsonResponse({'error': f'No review found for id {review_id}'}, status=status.HTTP_400_BAD_REQUEST)


def save_new_review(review, user) -> JsonResponse:
    try:
        ngo_id = review['ngoId']
        rating = review['rating']
        text = review['text']

        create_time = datetime.now()

        ngo = Ngo.objects.get(pk=ngo_id)

        NgoReview.objects.create(
            ngo=ngo,
            reviewer=user,
            create_date=create_time,
            last_edited=create_time,
            text=text,
            rating=rating,
        )
        ngo.number_of_reviews += 1
        ngo.save()
        update_ngo_tw_score(ngo)
        return JsonResponse(data={'message': 'Review was successfully stored.'}, status=status.HTTP_200_OK)

    except BaseException as err:
        return JsonResponse({'error': f'Review could not be stored: {err}.'}, status=status.HTTP_400_BAD_REQUEST,
                        safe=False)


@api_view(['GET'])
def user_review_present(request) -> JsonResponse:
    ngo_id = request.query_params.get('ngoId')
    user_id = request.query_params.get('userId')

    try:
        ngo = Ngo.objects.get(pk=ngo_id)
        user = User.objects.get(pk=user_id)
        reviews = NgoReview.objects.filter(ngo=ngo, reviewer=user)
        return JsonResponse(len(reviews) > 0, safe=False)
    except:
        return JsonResponse(False, safe=False)