"""."""

from enum import Enum
from functools import lru_cache

from ..db import (
    db,
    Achievement,
    AchievementCategory,
)
from .funcs import (
    FUNCTIONS,
    AddFunction,
)


class DefaultAchievementCategories(Enum):
    """미리 정의된 업적 분류."""

    No_Limitation = (
        "신청식",
        "신청식 업적을 위한 카테고리입니다.",
    )
    Manual_Approval = (
        "수동 승인식",
        "수동 승인식 업적을 위한 카테고리입니다.",
    )
    Automatic_Approval = (
        "자동 승인식",
        "자동 승인식 업적을 위한 카테고리입니다.",
    )
    Hidden_At_List = (
        "",
        "숨겨진 업적들 입니다, 리스트에만 숨겨져있어요.",
    )
    Hidden = (
        "",
        "아예 안보여요. 프로필에도요. 제작자들을 보관하기 위해서 씁시다.",
    )
    # Hidden은 Hidden_At_List와 같이 씁시다.


class DefaultAchievements(Enum):
    """미리 정의된 업적들."""

    Newbie_1_Egg = (
        "달걀",
        "- 어서오세요 AwesomeTitle에!",
        (
            DefaultAchievementCategories.Automatic_Approval,
            DefaultAchievementCategories.Hidden_At_List,
        ),
        "Newbie_1_Egg",
    )
    Newbie_2_Chick = (
        "병아리",
        "- AwesomeTitle을 사용중이시군요! (프로필을 채우시고, 친구에게 별명을 선사하면 받을 수 있어요.)",
        (
            DefaultAchievementCategories.Automatic_Approval,
            DefaultAchievementCategories.Hidden_At_List,
        ),
        "Newbie_2_Chick",
    )
    Newbie_3_Chicken = (
        "닭", 
        "- 친구들도 AwesomeTitle을 사용하네요! (친구들에게 별명을 10번 이상 선사하여야해요.)",
        (
            DefaultAchievementCategories.Automatic_Approval,
            DefaultAchievementCategories.Hidden_At_List,
        ),
        "Newbie_3_Chicken",
    )
    Newbie_4_FriedChicken = (
        "치킨",
        "- 치킨은 맛있죠. 암요. (친구들에게 병명을 10번 이상 추천 받으셨네요. 짝짝)",
        (
            DefaultAchievementCategories.Automatic_Approval,
            DefaultAchievementCategories.Hidden_At_List,
        ),
        "Newbie_4_FriedChicken",
    )
    Newbie_5_CEO = (
        "사장님",
        "- 치킨을 맛있게 튀길 수 있습니다. (?????)",
        (
            DefaultAchievementCategories.Automatic_Approval,
            DefaultAchievementCategories.Hidden_At_List,
        ),
        "Newbie_5_CEO",
    )

    Major_1_COMPUTER = (
        "컴퓨터공학과",
        "- 컴공입니다.",
        (
            DefaultAchievementCategories.No_Limitation,
        ),
        None,
    )
    Major_2_BUSINESS = (
        "경영학과",
        "- 경영학과에요.",
        (
            DefaultAchievementCategories.No_Limitation,
        ),
        None,
    )
    # ...

    Year_09 = (
        "09학번",
        "",
        (
            DefaultAchievementCategories.No_Limitation,
        ),
        None,
    )
    Year_10 = (
        "10학번",
        "",
        (
            DefaultAchievementCategories.No_Limitation,
        ),
        None,
    )
    Year_11 = (
        "11학번",
        "",
        (
            DefaultAchievementCategories.No_Limitation,
        ),
        None,
    )
    Year_12 = (
        "12학번",
        "",
        (
            DefaultAchievementCategories.No_Limitation,
        ),
        None,
    )
    Year_13 = (
        "13학번",
        "",
        (
            DefaultAchievementCategories.No_Limitation,
        ),
        None,
    )
    Year_14 = (
        "14학번",
        "",
        (
            DefaultAchievementCategories.No_Limitation,
        ),
        None,
    )
    Year_15 = (
        "15학번",
        "",
        (
            DefaultAchievementCategories.No_Limitation,
        ),
        None,
    )
    Year_16 = (
        "16학번",
        "",
        (
            DefaultAchievementCategories.No_Limitation,
        ),
        None,
    )
    # ...

    Language_C = (
        "C",
        "",
        (
            DefaultAchievementCategories.No_Limitation,
        ),
        None,
    )
    Language_Python = (
        "Python",
        "",
        (
            DefaultAchievementCategories.No_Limitation,
        ),
        None,
    )
    # ...

    DevEnv_OSX = (
        "OS X",
        "- 개발환경으로 맥(OS X)을 써요.",
        (
            DefaultAchievementCategories.No_Limitation,
        ),
        None,
    )
    DevEnv_Linux = (
        "Linux",
        "- 개발환경으로 리눅스(OS X)를 써요.",
        (
            DefaultAchievementCategories.No_Limitation,
        ),
        None,
    )
    DevEnv_Windows = (
        "Windows",
        "- 개발환경으로 윈도우(Windows)를 써요.",
        (
            DefaultAchievementCategories.No_Limitation,
        ),
        None,
    )
    # ...

    ACMICPC_User = (
        "ACM ICPC 플레이어",
        "- 프로필에 ACM ICPC 계정을 추가해주세요!",
        (
            DefaultAchievementCategories.Automatic_Approval,
        ),
        "ACMICPC_User",
    )
    ACMICPC_Over_100 = (
        "파워 ACM ICPC 플레이어",
        "- ACM 문제를 100문제 이상 풀었어요!",
        (
            DefaultAchievementCategories.Automatic_Approval,
        ),
        "ACMICPC_Over_100",
    )
    # ...

    AwesomeTitle_Committer = (
        "AwesomeTitle Committer",
        "- AwesomeTitle을 만들었어요.",
        (
            DefaultAchievementCategories.Automatic_Approval,
        ),
        "AwesomeTitle_Committer",
    )
    AwesomeTitle_Bug_Reporter = (
        "AwesomeTitle Bug Reporter",
        "- AwesomeTitle을 만드는데 도움을 주었어요.",
        (
            DefaultAchievementCategories.Automatic_Approval,
        ),
        "AwesomeTitle_Bug_Reporter",
    )
    AwesomeTitle_Password_Forgotten = (
        "비밀번호를 모르겠어요?",
        "- 저는 AwesomeTitle의 비밀번호를 잊어버린적이 있습니다.",
        (
            DefaultAchievementCategories.Automatic_Approval,
        ),
        "AwesomeTitle_Password_Forgotten",
    )
    # ...


def update_default_categories():
    for new_category_name, new_category_item in (
            DefaultAchievementCategories.__members__.items()
    ):
        found = AchievementCategory.query.filter(
                AchievementCategory.name == new_category_name,
        ).first()
        if not found:
            found = AchievementCategory()
            found.name = new_category_name
        found.display_name = new_category_item.value[0]
        found.description = new_category_item.value[1]
        db.session.add(found)
    # TODO: Remove the others.
    db.session.commit()


@lru_cache(None)
def get_category_idx(category, _raise=True):
    found = AchievementCategory.query.filter(
            AchievementCategory.name == category.name,
    ).first()
    if found:
        return found.idx
    if _raise:
        raise Exception("Not Found")
    return None


def update_default_achievement():
    for _, achievement in (
            DefaultAchievements.__members__.items()
    ):
        name, description, categories, func = achievement.value
        found = Achievement.query.filter(
                Achievement.name == name,
        ).first()
        if not found:
            found = Achievement()
            found.name = name
        # TODO: found.logo_url = None
        found.description = description
        found._categories = str([get_category_idx(c) for c in categories])
        found.checker_func = func if func else None
        db.session.add(found)
    db.session.commit()


@AddFunction
def Newbie_1_Egg():
    # TODO: '달걀' 타이틀을 획득하기 위한 조건!
    pass


@AddFunction
def Newbie_2_Chick():
    # TODO: '병아리' 타이틀을 획득하기 위한 조건!
    pass


@AddFunction
def Newbie_3_Chicken():
    # TODO: '닭' 타이틀을 획득하기 위한 조건!
    pass


@AddFunction
def Newbie_4_FriedChicken():
    # TODO: '치킨' 타이틀을 획득하기 위한 조건!
    pass


@AddFunction
def Newbie_5_CEO():
    # TODO: '사장님' 타이틀을 획득하기 위한 조건!
    pass


@AddFunction
def ACMICPC_User():
    # TODO: 'ACM ICPC 사용자' 타이틀을 획득하기 위한 조건!
    pass


@AddFunction
def ACMICPC_Over_100():
    # TODO: '파워 ACM ICPC 플레이어' 타이틀을 획득하기 위한 조건!
    pass


@AddFunction
def AwesomeTitle_Comitter():
    # TODO:
    pass


@AddFunction
def AwesomeTitle_Bug_Reporter():
    # TODO:
    pass


@AddFunction
def AwesomeTitle_Password_Forgotten():
    # TODO:
    pass

