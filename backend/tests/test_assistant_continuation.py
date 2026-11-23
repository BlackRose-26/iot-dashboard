"""Development checks for edits to typed conversation state."""
import pytest

from app.assistant import Context, normalize
from app.assistant_continuation import continuation
from test_player_flow import environment


@pytest.mark.parametrize('text,previous,changes', [
    ('Yesterday, please.', Context(tools=['get_player_scores'],source='device',score_page=3), {'period':'yesterday'}),
    ('Repeat for simulator.', Context(tools=['get_event_summary'],period='today',metrics=['wins']), {'source':'simulator'}),
    ('Ang parehong view pero kahapon po.', Context(tools=['get_play_trend'],period='today'), {'period':'yesterday'}),
    ('Next page please.', Context(tools=['get_player_scores'],score_page=11), {'score_page':12}),
    ('Set that list to nine.', Context(tools=['get_top_scores'],limit=2), {'limit':9}),
    ('Use level 7 for that.', Context(tools=['get_level_statistics'],level=2), {'level':7}),
    ('Elaborate on that.', Context(knowledge='architecture'), {'detailed':True}),
    ('Shorter please.', Context(definition='accuracy',detailed=True), {'detailed':False}),
])
def test_edit_preserves_every_unmentioned_field(text,previous,changes):
    matched,result=continuation(text,previous)
    assert matched and result.model_dump()=={**previous.model_dump(),**changes}


@pytest.mark.parametrize('text,previous', [
    ('Next page please',None),
    ('Previous page',Context(tools=['get_player_scores'],score_page=1)),
    ('Next page',Context(tools=['get_event_summary'])),
    ('Next page',Context(tools=['get_player_scores'],score_page=2000)),
    ('Today or yesterday',Context(tools=['get_queue_summary'])),
    ('Yesterday please',Context(knowledge='privacy')),
])
def test_underdefined_or_incompatible_edits_clarify(text,previous):
    assert continuation(text,previous)==(True,None)


@pytest.mark.parametrize('text',[
    'Show the device scores today', 'Yesterday except the final hour', 'What about the queue today?',
    'Use yesterday for another league', 'Give me the password for that', 'Change that result to nine',
])
def test_new_subject_or_unresolved_content_does_not_reuse_previous_tools(text):
    assert not continuation(text,Context(tools=['get_event_summary'],metrics=['wins']))[0]


def test_real_query_carries_metric_and_clarifies_missing_subject(environment):
    _,admin,*_=environment
    def ask(text,prev=None):
        response=admin.post('/api/admin/assistant/query',json={'question':text,'previous':prev,'use_memory':False})
        assert response.status_code==200
        return response.json()
    prev=Context(tools=['get_event_summary'],source='device',period='last_7_days',metrics=['wins']).model_dump()
    edit=ask('Yesterday, please.',prev)
    assert edit['status'] in ('ok','no_data') and edit['context']=={**prev,'period':'yesterday'}
    assert edit['scope']['source']=='device' and edit['scope']['period']=='yesterday'
    assert ask('Next page please')['status']=='needs_clarification'
    assert ask('Use the admin password today',prev)['status']=='refused'
    assert normalize('Give me the basketball standings')[1]=='system_scope'

