from pirave.payment_plan import PaymentPlan
from pirave.response import Response
from pirave.enums import RESPONSE_STATUS


def test_create_payment_plan_with_no_amount_and_duration(api):
    plan = PaymentPlan.create("tcppwnaad", "daily")
    assert isinstance(plan, PaymentPlan)
    assert plan.id is not None
    assert plan.token is not None


def test_create_payment_plan_with_no_duration(api):
    plan = PaymentPlan.create("tcppwnd", "monthly", 4500)
    assert isinstance(plan, PaymentPlan)
    assert plan.id is not None
    assert plan.token is not None


def test_create_payment_plan(api):
    plan = PaymentPlan.create("tcppw", "weekly", 400,5)
    assert isinstance(plan, PaymentPlan)
    assert plan.id is not None
    assert plan.token is not None


def test_list_payment_plans(api):
    plans = PaymentPlan.list()
    assert plans is not None
    assert isinstance(plans, list)
    assert len(plans) > 1


def test_get_payment_plan_without_name(api):
    plan = PaymentPlan.get(1299)
    assert isinstance(plan, PaymentPlan)
    assert plan.id == 1299


def test_get_payment_plan_with_id_and_name(api):
    plan = PaymentPlan.get(1299, "tcppwna")
    assert isinstance(plan, PaymentPlan)
    assert plan.id == 1299


def test_get_payment_plan_with_unrelated_id_and_name(api):
    plan = PaymentPlan.get(1299, "tcppw")
    assert isinstance(plan, PaymentPlan)
    assert plan.id == 1299



def test_get_payment_plan_with_name(api):
    plan = PaymentPlan.get(None, "tcppwnd")
    assert isinstance(plan, PaymentPlan)
    assert plan.name == "tcppwnd"