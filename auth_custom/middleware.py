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
        # Danh sách các đường dẫn cần kiểm tra token
        self.protected_paths = [
            "/api/",
            # "/api/accounts/",  # Thêm 1 số API bắt đầu khác nếu cần
        ]

    def __call__(self, request):
        # Chỉ kiểm tra token cho các API bắt đầu là 1 trong list protected_paths
        if any(request.path.startswith(path) for path in self.protected_paths):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Token "):
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
                print("duck4:", request.headers)
            except ExpiredSignatureError:
                return JsonResponse({"error": "Token has expired."}, status=401)
            except InvalidTokenError:
                return JsonResponse({"error": "Invalid token."}, status=401)

        # Tiếp tục xử lý request
        response = self.get_response(request)
        return response


# class RoleMiddleware:
#     """
#     Middleware để kiểm tra role của tài khoản từ token.
#     """

#     def __init__(self, get_response):
#         self.get_response = get_response
#         # Danh sách các đường dẫn cần kiểm tra role
#         self.protected_paths = {
#             "/api/admin/": ["ADMIN"],  # Chỉ role ADMIN được phép truy cập
#             "/api/manager/": ["MANAGER", "ADMIN"],  # Role MANAGER hoặc ADMIN được phép truy cập
#         }

#     def __call__(self, request):
#         # Kiểm tra nếu đường dẫn nằm trong danh sách cần bảo vệ
#         for path, allowed_roles in self.protected_paths.items():
#             if request.path.startswith(path):
#                 auth_header = request.headers.get("Authorization")
#                 if not auth_header or not auth_header.startswith("Token "):
#                     return JsonResponse(
#                         {"error": "Authentication credentials were not provided."},
#                         status=401,
#                     )

#                 token_key = auth_header.split(" ")[1]
#                 try:
#                     # Giải mã token
#                     payload = jwt.decode(
#                         token_key, settings.SECRET_KEY, algorithms=["HS256"]
#                     )
#                     user_id = payload.get("user_id")

#                     # Lấy thông tin tài khoản từ cơ sở dữ liệu
#                     account = Account.objects.get(id=user_id)
#                     user_roles = account.roles.values_list("code", flat=True)

#                     # Kiểm tra nếu user có ít nhất một role được phép
#                     if not any(role in allowed_roles for role in user_roles):
#                         return JsonResponse(
#                             {"error": "You do not have permission to access this resource."},
#                             status=403,
#                         )

#                     # Gắn thông tin user vào request
#                     request.userReq = {
#                         "user_id": account.id,
#                         "username": account.username,
#                         "roles": list(user_roles),
#                     }

#                 except ExpiredSignatureError:
#                     return JsonResponse({"error": "Token has expired."}, status=401)
#                 except InvalidTokenError:
#                     return JsonResponse({"error": "Invalid token."}, status=401)
#                 except Account.DoesNotExist:
#                     return JsonResponse({"error": "User not found."}, status=404)

#         # Tiếp tục xử lý request
#         response = self.get_response(request)
#         return response
