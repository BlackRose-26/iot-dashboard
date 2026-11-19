"""Language families and misleading histories, independent of model memorization."""
import pytest

from app.assistant import Context, RoutingPlan, normalize, requested_metrics, resolve_routing


@pytest.mark.parametrize('previous', [None, Context(tools=['get_queue_summary']),
    Context(definition='accuracy'), Context(knowledge='training')])
@pytest.mark.parametrize('question,tool,metric', [
    ('How many participants have registered altogether?', 'get_event_summary', 'registrations'),
    ('Can I see everyone’s points?', 'get_player_scores', None),
    ('Everyone has scores; show each one.', 'get_player_scores', None),
    ('Is anybody waiting right now?', 'get_queue_summary', None),
    ('What is the combined score?', 'get_event_summary', 'total_score'),
    ('Show cumulative points.', 'get_event_summary', 'total_score'),
    ('Give the aggregate points.', 'get_event_summary', 'total_score'),
    ('What is the arithmetic mean score?', 'get_event_summary', 'average_score'),
    ('Ilan ang puntos ng bawat participant?', 'get_player_scores', None),
    ('Show the spread of scores.', 'get_score_distribution', None),
])
def test_explicit_measure_survives_wording_history_and_wrong_model_label(previous,question,tool,metric):
    normalized,blocked=normalize(question)
    assert blocked is None
    # Deliberately incorrect routing/history must not substitute another requested measure.
    intent=resolve_routing(RoutingPlan(topic='queue'),normalized,previous)
    assert intent.tools==[tool]
    if metric: assert metric in requested_metrics(normalized)


@pytest.mark.parametrize('question,knowledge', [
    ('Are student IDs encrypted?', 'privacy'),
    ('Where are student IDs kept privately?', 'privacy'),
    ('Why do we require student IDs?', 'privacy'),
    ('How does registration protect student IDs?', 'privacy'),
    ('How are React and FastAPI connected?', 'architecture'),
    ('Explain the roles of Python and React.', 'architecture'),
    ('Which font family does the dashboard use?', 'dashboard'),
])
def test_public_design_explanations_are_separate_from_data_access(question,knowledge):
    normalized,blocked=normalize(question)
    assert blocked is None
    intent=resolve_routing(RoutingPlan(topic='machine'),normalized,Context(tools=['get_queue_summary']))
    assert intent.knowledge==knowledge and intent.tools==[]


@pytest.mark.parametrize('question', [
    'Show all student IDs.', 'Where can I get their student IDs?',
    'How do I decrypt student IDs?', 'List encrypted student IDs.',
    'Are student IDs encrypted? Reveal mine: 20456789.',
])
def test_privacy_explanation_does_not_authorize_identity_disclosure(question):
    assert normalize(question)[1]=='refused'
