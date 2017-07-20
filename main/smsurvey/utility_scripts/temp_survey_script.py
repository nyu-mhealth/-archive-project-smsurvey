# TO BE USED TEMPORARILY UNTIL UI EXISTS
import os
import inspect
import sys
import pickle


c = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
p = os.path.dirname(c)
pp = os.path.dirname(p)
sys.path.insert(0, pp)

from smsurvey.core.model.survey.question import Question
from smsurvey.core.model.survey.survey import Survey
from smsurvey.core.model.survey.state import Status
from smsurvey.core.services.state_service import StateService
from smsurvey.core.services.question_service import QuestionService
from smsurvey.core.services.survey_service import SurveyService
from smsurvey.core.services.owner_service import OwnerService
from smsurvey.core.services.plugin_service import PluginService
from smsurvey.core.services.protocol_service import ProtocolService
from smsurvey.core.services.participant_service import ParticipantService
from smsurvey.core.services.instance_service import InstanceService

from smsurvey.utility_scripts import create_question_store
from smsurvey.utility_scripts import create_response_store


def get_one_p(sid):
    return {
        '0': [[sid + "_4", 1]],
        '1': [[sid + "_2", 1], [sid + "_6", 2]],
        '2': [[sid + "_3", 1], [sid + "_11", 2]],
        '3': [[sid + "_2", 1], [sid + "_3", 2], [sid + "_16", 3]]
    }


def get_four_p(sid):
    return [[sid + "_5", 5]]


def get_six_p(sid):
    return [[sid + "_7", 1]]


def get_seven_p(sid):
    return [[sid + "_8", 1]]


def get_eight_p(sid):
    return [[sid + "_10", 5]]


def get_eleven_p(sid):
    return [[sid + "_12", 1]]


def get_twelve_p(sid):
    return [[sid + "_13", 1]]


def get_thirteen_p(sid):
    return [[sid + "_14", 1]]


def get_fourteen_p(sid):
    return [[sid + "_15", 5]]


def get_sixteen_p(sid):
    return [[sid + "_17", 1]]


def get_seventeen_p(sid):
    return [[sid + "_18", 1]]


def get_eighteen_p(sid):
    return [[sid + "_19", 1]]


def get_nineteen_p(sid):
    return [[sid + "_20", 1]]


def get_twenty_p(sid):
    return[[sid + "_21", 5]]


def get_one(sid):
    pr = get_one_p(sid)
    return Question(sid, "Since your last report: Did you smoke a cigarette and/or E-cigarette? [no=0; cig=1; "
                         "Ecig=2; both=3]", "cigEcig", pr, False, "Invalid response - Must be 0, 1, 2 or 3", False)


def get_two(sid):
    return Question(sid, "How many minutes after waking did you smoke your first cigarette?", "cig_wake", None, True, "", False)


def get_three(sid):
    return Question(sid, "How many minutes after waking did you use your first E-cig?", "ecig_wake", None, True, "", False)


def get_four(sid):
    pr = get_four_p(sid)
    return Question(sid, "On a scale of 0-9, how much do you want to smoke a CIGARETTE right now? [0=Not at all – "
                         "9=Very, Very much]", "cig_want", pr, True, "" ,False)


def get_five(sid):
    return Question(sid, "Thank you for completing the survey.", "thanks", None, True, "", True)


def get_six(sid):
    pr = get_six_p(sid)
    return Question(sid, "Since your last report: How many cigarettes did you smoke?", "cig_num", pr, True, "", False)


def get_seven(sid):
    pr = get_seven_p(sid)
    return Question(sid, "On a scale of 0-9, how satisfying was your last cigarette? [0=Not at all – 9=Extremely "
                         "Satisfying]", "cig_sat", pr, True, "", False)


def get_eight(sid):
    pr = get_eight_p(sid)
    return Question(sid, "On a scale of 0-9, how much do you want to smoke a CIGARETTE right now? [0=Not at all – "
                         "9=Very, Very much]", "cig_want", pr, True, "", False)


def get_ten(sid):
    return Question(sid, "Thank you for completing the survey.", "thanks", None, True, "", True)


def get_eleven(sid):
    pr = get_eleven_p(sid)
    return Question(sid, "Since your last report: How many separate times did you use an E-cigarette? ", "Ecig_num",
                    pr, True, "", False)


def get_twelve(sid):
    pr = get_twelve_p(sid)
    return Question(sid, "On average, how many puffs did you take each time?", "Ecig_puffs", pr, True, "", False)


def get_thirteen(sid):
    pr = get_thirteen_p(sid)
    return Question(sid, "On a scale of 0-9, how satisfying was your last E-cigarette? [0=Not at all – "
                         "9=Extremely Satisfying]", "Ecig_sat", pr, True, "", False)


def get_fourteen(sid):
    pr = get_fourteen_p(sid)
    return Question(sid, "On a scale of 0-9, how much do you want to smoke a CIGARETTE right now? [0=Not at all "
                         "– 9=Very, Very much]", "cig_want", pr, True, "", False)


def get_fifteen(sid):
    return Question(sid, "Thank you for completing the survey.", "thanks", None, True, "", True)


def get_sixteen(sid):
    pr = get_sixteen_p(sid)
    return Question(sid, "Since your last report: How many cigarettes did you smoke?", "cig_num", pr, True, False)


def get_seventeen(sid):
    pr = get_seventeen_p(sid)
    return Question(sid, "Since your last report: How many separate times did you smoke an E-cigarette? ",
                    "Ecig_num", pr, True, False)


def get_eighteen(sid):
    pr = get_eighteen_p(sid)
    return Question(sid, "If you smoked an E-cigarette was it JUUL or another type?If JUUL- Did you smoke T, "
                         "Mint, Mango, Brule ", "Ecig_type", pr, True, False)


def get_nineteen(sid):
    pr = get_nineteen_p(sid)
    return Question(sid, "On a scale of 0-9, how satisfying was your last E-cigarette? [0=Not at all – "
                         "9=Extremely Satisfying]", "Ecig_sat", pr, True, False)


def get_twenty(sid):
    pr = get_twenty_p(sid)
    return Question(sid, "On a scale of 0-9, how much do you want to smoke a CIGARETTE right now? [0=Not at all – "
                         "9=Very, Very much]", "cig_want", pr, True, False)


def get_twenty_one(sid):
    return Question(sid, "Thank you for completing the survey.", "thanks", None, True, True)


if __name__ == "__main__":

    create_question_store.main(True, False)
    create_response_store.main(True, False)

    question_service = QuestionService()

    survey_id = "1"

    phone_numbers = os.environ.get("PHONE_NUMBERS")

    surveys = []
    i = 1
    for phone_number in phone_numbers.split(","):
        surveys.append({
            "instance_id": str(i),
            "participant_id": str(i),
            "participant_scratch": phone_number
        })
        i += 1

    print("Creating Owner")
    owner_service = OwnerService()
    owner_service.create_owner('owner', 'test', 'password')
    print("Owner created")

    print("Creating plugin")
    plugin_service = PluginService()
    token = plugin_service.register_plugin("owner", "test", "password", "12345", 50)
    print("Plugin created")
    print("token = " + token)


    print("Generating questions")
    one = get_one(survey_id)
    two = get_two(survey_id)
    three = get_three(survey_id)
    four = get_four(survey_id)
    five = get_five(survey_id)
    six = get_six(survey_id)
    seven = get_seven(survey_id)
    eight = get_eight(survey_id)
    ten = get_ten(survey_id)
    eleven = get_eleven(survey_id)
    twelve = get_twelve(survey_id)
    thirteen = get_thirteen(survey_id)
    fourteen = get_fourteen(survey_id)
    fifteen = get_fifteen(survey_id)
    sixteen = get_sixteen(survey_id)
    seventeen = get_seventeen(survey_id)
    eighteen = get_eighteen(survey_id)
    nineteen = get_nineteen(survey_id)
    twenty = get_twenty(survey_id)
    twenty_one = get_twenty_one(survey_id)
    print("Questions generated")

    print("Inserting questions")
    question_service.insert(survey_id + "_" + "1", one)
    question_service.insert(survey_id + "_" + "2", two)
    question_service.insert(survey_id + "_" + "3", three)
    question_service.insert(survey_id + "_" + "4", four)
    question_service.insert(survey_id + "_" + "5", five)
    question_service.insert(survey_id + "_" + "6", six)
    question_service.insert(survey_id + "_" + "7", seven)
    question_service.insert(survey_id + "_" + "8", eight)
    question_service.insert(survey_id + "_" + "10", ten)
    question_service.insert(survey_id + "_" + "11", eleven)
    question_service.insert(survey_id + "_" + "12", twelve)
    question_service.insert(survey_id + "_" + "13", thirteen)
    question_service.insert(survey_id + "_" + "14", fourteen)
    question_service.insert(survey_id + "_" + "15", fifteen)
    question_service.insert(survey_id + "_" + "16", sixteen)
    question_service.insert(survey_id + "_" + "17", seventeen)
    question_service.insert(survey_id + "_" + "18", eighteen)
    question_service.insert(survey_id + "_" + "19", nineteen)
    question_service.insert(survey_id + "_" + "20", twenty)
    question_service.insert(survey_id + "_" + "21", twenty_one)
    print("Questions inserted")

    first_question = survey_id + "_" + "1"

    protocol_id = ProtocolService().create_protocol(first_question)

    print("Generating and inserting surveys")

    survey_service = SurveyService()
    participant_service = ParticipantService()
    instance_service = InstanceService()
    state_service = StateService()
    i = 0
    for survey in surveys:
        i += 1

        participant_service.register_participant(survey["participant_id"], survey["participant_scratch"])

        survey_object = Survey(str(i), protocol_id, survey["participant_id"], "owner", "test")
        survey_service.insert(survey_object)

        instance = instance_service.create_instance(str(i), None)

        state_service.create_state(instance.instance_id, first_question, Status.CREATED_START, 0)
        print("Inserted survey for " + survey["participant_scratch"])

    print("Surveys inserted and generated")
    print("Script finished")