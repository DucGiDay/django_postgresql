from django.http import JsonResponse
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from django.conf import settings


class TokenMiddleware:
    """
    Middleware để kiểm tra token từ request.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Danh sách các đường dẫn không cần check authorize
        self.not_protected_paths = [
            "/api/auth/",
            # "/any-not-auth-api/",  # Thêm 1 số API bắt đầu khác nếu cần
        ]

    def __call__(self, request):
        # Chỉ kiểm tra token cho các API bắt đầu là '/api/' và ko bắt đầu bằng 1 trong list not_protected_paths
        is_check_auth = request.path.startswith("/api/") and not any(
            request.path.startswith(path) for path in self.not_protected_paths
        )

        if is_check_auth:
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JsonResponse(
                    {"error": "Authentication credentials were not provided."},
                    status=401,
                )
            token_key = auth_header.split(" ")[1]
            try:
                payload = jwt.decode(
                    token_key, settings.SECRET_KEY, algorithms=["HS256"]
                )
                request.userReq = {
                    "user_id": payload.get("user_id"),
                    "username": payload.get("username"),
                }  # Gắn user vào request để sử dụng trong view
            except ExpiredSignatureError:
                return JsonResponse({"error": "Token has expired."}, status=401)
            except InvalidTokenError:
                return JsonResponse({"error": "Invalid token."}, status=401)

        # Tiếp tục xử lý request
        response = self.get_response(request)
        return response
