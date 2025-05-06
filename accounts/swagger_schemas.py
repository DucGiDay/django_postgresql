from drf_yasg import openapi

# Các tham số dùng chung
PAGE_PARAMETER = openapi.Parameter(
    "page",
    openapi.IN_QUERY,
    description="Số trang",
    type=openapi.TYPE_INTEGER,
)

LIMIT_PARAMETER = openapi.Parameter(
    "limit",
    openapi.IN_QUERY,
    description="Số lượng mục trên mỗi trang",
    type=openapi.TYPE_INTEGER,
)

KEYWORD_PARAMETER = openapi.Parameter(
    "keyword",
    openapi.IN_QUERY,
    description="Tìm kiếm",
    type=openapi.TYPE_STRING,
)

# Schema cho request body
ASSIGN_ROLE_BODY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "role_codes": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_STRING),
            description="Danh sách các mã role (code) cần gắn cho người dùng",
        ),
    },
    required=["role_codes"],
)
