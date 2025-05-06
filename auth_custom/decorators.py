import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from django.http import JsonResponse
from django.conf import settings
from accounts.models import Account

def check_role(required_roles):
    """
    Decorator để kiểm tra role của tài khoản từ token.
    :param required_roles: Danh sách các role được phép truy cập
    """
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JsonResponse(
                    {"error": "Authentication credentials were not provided."},
                    status=401,
                )

            token_key = auth_header.split(" ")[1]
            try:
                # Giải mã token
                payload = jwt.decode(
                    token_key, settings.SECRET_KEY, algorithms=["HS256"]
                )
                roles = payload.get("roles")

                # Kiểm tra nếu user có ít nhất một role được phép
                if not any(role in required_roles for role in roles):
                    return JsonResponse(
                        {"error": "You do not have permission to access this resource."},
                        status=403,
                    )

            except ExpiredSignatureError:
                return JsonResponse({"error": "Token has expired."}, status=401)
            except InvalidTokenError:
                return JsonResponse({"error": "Invalid token."}, status=401)
            except Account.DoesNotExist:
                return JsonResponse({"error": "User not found."}, status=404)

            # Tiếp tục xử lý view
            return view_func(request, *args, **kwargs)

        return wrapped_view
    return decorator