from .models import Bid

# get the rating score for the current writer to display in star form
def get_rating(request):
    try:
        user = request.user
        rating = user.rating_set.all()

        agg = 0
        count = 0
        for rating in rating:
            agg = agg + rating.score
            count += 1
            avg = agg/count
        return {'rating': avg}
    except:
        return {'rating': 0}

