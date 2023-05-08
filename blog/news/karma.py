from enum import Enum
from .models import Comment, Post, FavoritePost, User


class KarmaActionCost(Enum):
    SUBMIT_POST = 4
    SUBMIT_COMMENT = 2
    ADD_POST_TO_FAVOURITE = 3
    EVERYDAY_ONLINE_BONUS = 5
    POST_RATING_COST = 3
    COMMENT_RATING_COST = 2

    # BAD KARMA
    POST_WAS_DELETED = 20
    COMMENT_WAS_DELETED = 5


def submit_post(post: Post):
    """Bonus for post creation"""
    post.author.userprofile.plus_karma(KarmaActionCost.SUBMIT_POST.value)


def submit_comment(comment: Comment):
    """Bonus for comment creation"""
    comment.user_submitter.userprofile.plus_karma(KarmaActionCost.SUBMIT_COMMENT.value)


def add_post_to_favourite(post: Post):
    """Bonus for adding post to favorites by any user"""
    post.author.userprofile.plus_karma(KarmaActionCost.ADD_POST_TO_FAVOURITE.value)


def remove_post_from_favourite(post: Post):
    """Remove bonus for remove post from favorites"""
    post.author.userprofile.minus_karma(KarmaActionCost.ADD_POST_TO_FAVOURITE.value)


def post_rating_plus(post: Post):
    """Bonus for positive post rating"""
    post.author.userprofile.plus_karma(KarmaActionCost.POST_RATING_COST.value)


def post_rating_minus(post: Post):
    """Remove bonus for negative coupon rating"""
    post.author.userprofile.minus_karma(KarmaActionCost.POST_RATING_COST.value)


def comment_rating_plus(comment: Comment):
    """Bonus for positive comment rating"""
    comment.user_submitter.userprofile.plus_karma(KarmaActionCost.COMMENT_RATING_COST.value)


def comment_rating_minus(comment: Comment):
    """Remove bonus for negative comment rating"""
    comment.user_submitter.userprofile.minus_karma(KarmaActionCost.COMMENT_RATING_COST.value)


def everyday_bonus(user: User):
    """Bonus for daily site visits"""
    user.userprofile.plus_karma(KarmaActionCost.EVERYDAY_ONLINE_BONUS.value)


def delete_post(post: Post):
    """Remove all bonuses which were given for this post"""
    coupon_submit_karma = KarmaActionCost.SUBMIT_POST.value
    coupon_rating_karma = post.rating * KarmaActionCost.COMMENT_RATING_COST.value if post.rating > 0 else 0
    coupon_favourite_karma = FavoritePost.objects.filter(obj=post).count() * KarmaActionCost.ADD_POST_TO_FAVOURITE.value
    post.author.userprofile.minus_karma(
        KarmaActionCost.POST_WAS_DELETED.value +
        coupon_submit_karma +
        coupon_favourite_karma +
        coupon_rating_karma
    )


def delete_comment(comment: Comment):
    """Remove all bonuses which were given for this comment"""
    comment_submit_karma = KarmaActionCost.SUBMIT_COMMENT.value
    comment_rating = comment.rating * KarmaActionCost.COMMENT_RATING_COST.value if comment.rating > 0 else 0
    comment.user_submitter.userprofile.minus_karma(
        KarmaActionCost.COMMENT_WAS_DELETED.value + comment_rating + comment_submit_karma)
