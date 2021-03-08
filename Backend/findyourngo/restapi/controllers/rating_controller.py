from django.http.response import JsonResponse

from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.parsers import JSONParser

from findyourngo.restapi.models import Ngo, NgoReview, NgoTWDataPoint
from findyourngo.data_import.data_importer import update_ngo_tw_score

from datetime import datetime

from findyourngo.trustworthiness_calculator.TWUpdater import TWUpdater
from findyourngo.trustworthiness_calculator.utils import round_to_two_decimal_places


@api_view(['GET'])
def tw_rating(request) -> JsonResponse:
    ngo_id = request.query_params.get('id')

    try:
        ngo = Ngo.objects.get(pk=ngo_id)
    except BaseException:
        return JsonResponse({'error': f'NGO with id {ngo_id} does not exist.'}, status=status.HTTP_400_BAD_REQUEST, safe=False)

    reviews = NgoReview.objects.filter(ngo=ngo)

    total_tw = round_to_two_decimal_places(ngo.tw_score.total_tw_score)

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


def convert_data_points(data_points):
    result = []

    for data_point in data_points:
        converted_data_point = {
            'dailyTwScore': data_point.daily_tw_score,
            'date': data_point.date
        }
        result.append(converted_data_point)

    return result


def generate_missing_data_points(tw_data_points):
    result = []
    for data_point in tw_data_points:
        if len(result) == 0:
            result.append(data_point)
        else:
            last_result = result[len(result)-1]
            while data_point.date > last_result.date and data_point.date.day - last_result.date.day > 1:
                print(last_result.date.month, ' ', last_result.date.day)
                last_result = NgoTWDataPoint(
                    date=datetime(last_result.date.year, last_result.date.month, last_result.date.day + 1).date(),
                    daily_tw_score=last_result.daily_tw_score)
                result.append(last_result)
            result.append(data_point)

    last_result = result[len(result)-1]
    today_date = datetime.today().date()
    while today_date > last_result.date:
        daily_tw_score = round_to_two_decimal_places(last_result.daily_tw_score)
        try:
            last_result = NgoTWDataPoint(date=datetime(last_result.date.year, last_result.date.month, last_result.date.day + 1).date(), daily_tw_score=daily_tw_score)
        except:
            try:
                last_result = NgoTWDataPoint(
                    date=datetime(last_result.date.year, last_result.date.month + 1, 1).date(),
                    daily_tw_score=daily_tw_score)
            except:
                last_result = NgoTWDataPoint(
                    date=datetime(last_result.date.year + 1, 1, 1).date(),
                    daily_tw_score=daily_tw_score)
        result.append(last_result)
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
        TWUpdater()._calculate_tw_without_pagerank_for_ngo(ngo)
        ngo.save()
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


@api_view(['GET'])
def tw_history(request) -> JsonResponse:
    ngo_id = request.query_para

    try:
        ngo = Ngo.objects.get(pk=ngo_id)
        tw_data_points = ngo.tw_score.tw_series.order_by('date').all()
        complete_tw_data_points = generate_missing_data_points(tw_data_points) if len(tw_data_points) > 0 else tw_data_points
        return JsonResponse(convert_data_points(complete_tw_data_points), safe=False)
    except:
        return JsonResponse([], safe=False)

