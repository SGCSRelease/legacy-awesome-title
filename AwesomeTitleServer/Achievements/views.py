from functools import lru_cache

from flask import render_template, jsonify

from ..cookie import add_cookies
from ..db import Achievement, AchievementCategory
from .defaults import (
    DefaultAchievementCategories,
    get_category_idx,
)


COOKIE_NAME_FOR_HIDE_JUMBOTRON = "HIDE_JUMBOTRON"


def add_routes(app):
    app.route("/achievements/")(Achievements)
    app.route("/api/achivements/hide_jumbotron/")(Hide_Jumbotron_for_Achievements)


def Achievements():
    return render_template("achievements.html")


def Hide_Jumbotron_for_Achievements():
    return add_cookies({
        COOKIE_NAME_FOR_HIDE_JUMBOTRON: "Yes",
    })


@lru_cache(1)
def get_default_category_dict():
    categories = {}
    for key, value in DefaultAchievementCategories.__members__.items():
        if 'Hidden' not in key:
            categories[get_category_idx(value)] = value.value[0]
    return categories



def get_archivements_list():
    @lru_cache(None)
    def get_category_from_idx(idx):
        # TODO: MOVE IT
        found = AchievementCategory.query.get(idx)
        if not found:
            return None
        return found

    ret = []
    for achievement in Achievement.query.all():
        if get_category_idx(
            DefaultAchievementCategories.Hidden_At_List
        ) not in achievement.getCategories():
            ret.append(
                    (
                        achievement.idx,
                        achievement.name,
                        achievement.description,
                        ','.join(
                            [
                                '#' + get_category_from_idx(c).display_name for c in achievement.getCategories()
                            ]
                        ),
                    )
            )
    return ret 
