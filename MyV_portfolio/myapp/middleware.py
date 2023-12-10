# import logging
# import traceback
# from django.http import JsonResponse

# class EnhancedLogMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.logger = logging.getLogger(__name__)

#     def __call__(self, request):
#         try:
#             response = self.get_response(request)
#         except Exception as e:
#             # エラー情報とトレースバックをログに記録
#             self.logger.error(f"Exception: {e}\nTraceback: {traceback.format_exc()}")
#             response = JsonResponse({"error": "An internal server error occurred"}, status=500)

#         # ログメッセージの構築
#         log_message = f"Path: {request.path}, Method: {request.method}, Status Code: {response.status_code}"

#         # ユーザー情報の追加
#         if hasattr(request, 'user') and request.user.is_authenticated:
#             log_message += f", User: {request.user}"

#         # POSTリクエストデータの記録
#         if request.method == 'POST':
#             # 機密情報をフィルタリング（例：パスワードフィールド）
#             post_data = {k: v for k, v in request.POST.items() if k != 'password'}
#             log_message += f", POST Data: {post_data}"

#         # リダイレクト先のURLの記録
#         if response.status_code == 302:
#             log_message += f", Redirect URL: {response.url}"

#         # リクエストヘッダーの記録
#         log_message += f", Headers: {request.headers}"

#         # セッションデータの記録（機密情報を除外）
#         if hasattr(request, 'session'):
#             session_data = dict(request.session)
#             # 機密情報をフィルタリング
#             filtered_session_data = {k: v for k, v in session_data.items() if k not in ['_auth_user_id', '_auth_user_backend']}
#             log_message += f", Session Data: {filtered_session_data}"

#         # 詳細なログ情報の記録
#         self.logger.info(log_message)

#         return response
