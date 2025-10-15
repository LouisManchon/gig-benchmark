"""
API endpoints pour déclencher le scraping

KEYLOCK A CONFIGURER ICI (on vera a la fin)
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from services.management.scraping_service import scraping_service


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({'status': 'healthy', 'service': 'scraping-api'})


@api_view(['GET'])
@permission_classes([AllowAny])
def list_scrapers(request):
    result = scraping_service.get_available_scrapers()
    return Response(result)


@api_view(['POST'])
@permission_classes([AllowAny])  # Temporairement sans auth pour tester
def trigger_scraping(request):
    scraper = request.data.get('scraper')
    if not scraper:
        return Response({'error': 'scraper field required'}, status=status.HTTP_400_BAD_REQUEST)
    result = scraping_service.send_task(scraper)
    if result['success']:
        return Response(result)
    return Response(result, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def trigger_multiple_scraping(request):
    scrapers = request.data.get('scrapers', [])
    if not scrapers:
        return Response({'error': 'scrapers field required'}, status=status.HTTP_400_BAD_REQUEST)
    result = scraping_service.send_multiple_tasks(scrapers)
    return Response(result)


@api_view(['POST'])
@permission_classes([AllowAny])
def scrape_all_football(request):
    result = scraping_service.scrape_all_football()
    return Response(result)


@api_view(['POST'])
@permission_classes([AllowAny])
def scrape_all_basketball(request):
    result = scraping_service.scrape_all_basketball()
    return Response(result)


@api_view(['POST'])
@permission_classes([AllowAny])
def scrape_all_rugby(request):
    result = scraping_service.scrape_all_rugby()
    return Response(result)


@api_view(['POST'])
@permission_classes([AllowAny])
def scrape_all_tennis(request):
    result = scraping_service.scrape_all_tennis()
    return Response(result)


@api_view(['POST'])
@permission_classes([AllowAny])
def scrape_all(request):
    result = scraping_service.scrape_all()
    return Response(result)