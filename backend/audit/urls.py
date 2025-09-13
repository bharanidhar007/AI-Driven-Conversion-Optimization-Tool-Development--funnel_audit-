from django.urls import path
from .views import SubmitView, ReportDetailView, RegisterView, ProfileView, StripeWebhookView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('reports/', ReportListView.as_view(), name='report-list'),
    path('report-detail/<uuid:report_id>/', report_detail_public, name='report-detail-public'),
    path('me/referral/', my_referral, name='my-referral'),
    path('me/redeem/', redeem_referral, name='redeem-referral'),
    path('admin/stats/', admin_stats, name='admin-stats'),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('submit/', SubmitView.as_view(), name='submit'),
    path('report/<uuid:report_id>/', ReportDetailView.as_view(), name='report-detail'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('stripe/webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
]
