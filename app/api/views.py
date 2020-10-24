from app.api import api
from app.api.controllers.main_controller import login, register, get_messages_by_user_id, add_message, \
    delete_messages_by_id

from app.api.utils import PostCaller, NonSecurePostCaller, GetCaller


class LoginView(NonSecurePostCaller):
    def worker(self, *args, **kwargs):
        return login(self.request_body)


class RegisterView(NonSecurePostCaller):
    def worker(self, *args, **kwargs):
        return register(self.request_body)


class GetMessagesByUserId(GetCaller):
    def worker(self, *args, **kwargs):
        return get_messages_by_user_id(self.request.args)


class RemoveMessageById(PostCaller):
    def worker(self, *args, **kwargs):
        return delete_messages_by_id(self.request_body)


class AddMessage(PostCaller):
    def worker(self, *args, **kwargs):
        return add_message(self.request_body)


class DeleteMessagesById(PostCaller):
    def worker(self, *args, **kwargs):
        return delete_messages_by_id(self.request_body)


login_view = LoginView.as_view('login_view')
register_view = RegisterView.as_view('register_view')
get_messages_by_user_id_view = GetMessagesByUserId.as_view('get_messages_by_user_id_view')
remove_message_by_id_view = RemoveMessageById.as_view('remove_message_by_id_view')
add_message_view = AddMessage.as_view('add_message_view')
delete_messages_view = DeleteMessagesById.as_view('delete_messages_view')

api.add_url_rule(
    '/v1/login',
    view_func=login_view,
    methods=['POST']
)

api.add_url_rule(
    '/v1/register',
    view_func=register_view,
    methods=['POST']
)

api.add_url_rule(
    '/v1/get_all_messages',
    view_func=get_messages_by_user_id_view,
    methods=['GET']
)

api.add_url_rule(
    '/v1/remove_message_by_id',
    view_func=remove_message_by_id_view,
    methods=['POST']
)

api.add_url_rule(
    '/v1/add_message',
    view_func=add_message_view,
    methods=['POST']
)

api.add_url_rule(
    '/v1/delete_messages',
    view_func=delete_messages_view,
    methods=['POST']
)
