from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import SubmitSerializer, ReportSerializer, RegisterSerializer, ProfileSerializer
from .models import Report, Profile
from .tasks import enqueue_scrape_task
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json, os
import stripe

stripe.api_key = os.getenv('STRIPE_SECRET_KEY','')


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})

class SubmitView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = SubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        url = serializer.validated_data['url']
        # Check credits
        profile = request.user.profile
        if profile.credits <= 0:
            return Response({'detail':'No credits. Purchase or refer to get more.'}, status=status.HTTP_402_PAYMENT_REQUIRED)
        report = Report.objects.create(user=request.user, url=url, status='queued')
        profile.credits -= 1
        profile.save()
        enqueue_scrape_task.delay(str(report.id), url, request.user.id)
        return Response(ReportSerializer(report).data, status=status.HTTP_201_CREATED)

class ReportDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, report_id):
        report = get_object_or_404(Report, id=report_id, user=request.user)
        data = ReportSerializer(report).data
        if hasattr(report,'detail') and report.detail.ai_analysis:
            data['ai_analysis'] = report.detail.ai_analysis
            data['features'] = report.detail.features
        return Response(data)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = ProfileSerializer(request.user.profile)
        return Response(serializer.data)


class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # Create a Stripe Checkout Session to purchase credits.
        # Expects JSON body: {"credits": <int>, "unit_price_cents": <int>} or uses default package.
        try:
            body = request.data
            credits = int(body.get('credits', 10))
            # price per credit in cents (example $0.50 per credit)
            price_per_credit_cents = int(body.get('unit_price_cents', 50))
            amount = credits * price_per_credit_cents
            # Create Checkout Session
            success_url = os.getenv('FRONTEND_URL', 'http://localhost:3000') + '/?checkout=success'
            cancel_url = os.getenv('FRONTEND_URL', 'http://localhost:3000') + '/?checkout=cancel'
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                mode='payment',
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': f'{credits} credits for Funnel Audit'},
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                }],
                client_reference_id=str(request.user.username),
                success_url=success_url,
                cancel_url=cancel_url,
            )
            return Response({'session_url': session.url})
        except Exception as e:
            return Response({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        # Minimal stub - verify signature in production
        try:
            payload = request.body.decode('utf-8')
            event = json.loads(payload)
            # Example: simulate checkout.session.completed -> add credits
            if event.get('type') == 'checkout.session.completed':
                client_ref = event.get('data',{}).get('object',{}).get('client_reference_id')
                if client_ref:
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    try:
                        user = User.objects.get(username=client_ref)
                        user.profile.credits += 10
                        user.profile.save()
                    except User.DoesNotExist:
                        pass
            return Response({'ok': True})
        except Exception as e:
            return Response({'error': str(e)}, status=400)

from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from django.db.models import Count
from .serializers import ReportSerializer, ProfileSerializer
from .models import Report, Profile
from django.shortcuts import get_object_or_404

class ReportListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReportSerializer
    def get_queryset(self):
        return Report.objects.filter(user=self.request.user).order_by('-created_at')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def report_detail_public(request, report_id):
    report = get_object_or_404(Report, id=report_id, user=request.user)
    data = ReportSerializer(report).data
    if hasattr(report,'detail') and report.detail.ai_analysis:
        data['ai_analysis'] = report.detail.ai_analysis
        data['features'] = report.detail.features
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_referral(request):
    profile = request.user.profile
    return Response({'referral_code': profile.referral_code, 'credits': profile.credits, 'referred_by': profile.referred_by.username if profile.referred_by else None})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def redeem_referral(request):
    # Manually redeem a referral code for a friend (admin usage limited here)
    code = request.data.get('code')
    if not code:
        return Response({'error':'code required'}, status=400)
    try:
        prof = Profile.objects.get(referral_code=code)
        if prof.user == request.user:
            return Response({'error':'cannot redeem your own code'}, status=400)
        # award credits to both if not already referred
        if request.user.profile.referred_by is None:
            request.user.profile.referred_by = prof.user
            request.user.profile.credits += 1
            prof.credits += 1
            request.user.profile.save()
            prof.save()
            return Response({'ok': True})
        else:
            return Response({'error':'already referred'}, status=400)
    except Profile.DoesNotExist:
        return Response({'error':'invalid code'}, status=404)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_stats(request):
    total_users = Profile.objects.count()
    total_reports = Report.objects.count()
    reports_by_status = Report.objects.values('status').annotate(count=Count('id'))
    return Response({'total_users': total_users, 'total_reports': total_reports, 'reports_by_status': list(reports_by_status)})
