from flask import Blueprint, request, current_app
import requests
import xml.etree.ElementTree as ET
from app.utils.xml_utils import create_error_response, create_xml_response
from app.utils.auth_utils import student_required

bp = Blueprint('external_services', __name__, url_prefix='/api/v1')

# Using the NOAA Weather Service as an example
WEATHER_SERVICE_URL = "https://w1.weather.gov/xml/current_obs/KNYC.xml"


@bp.route('/weather', methods=['GET'])
@student_required
def get_weather():
    """Get weather data from external XML service (requires student or admin role)"""
    try:
        # Fetch XML data from external service
        response = requests.get(WEATHER_SERVICE_URL, timeout=10)
        
        if response.status_code != 200:
            xml_response = create_error_response("Failed to retrieve weather data")
            return xml_response, 500, {'Content-Type': 'application/xml'}
        
        # Parse XML response
        root = ET.fromstring(response.content)
        
        # Extract relevant weather information
        weather_data = {
            'location': root.find('location').text if root.find('location') is not None else 'Unknown',
            'temperature': root.find('temperature_string').text if root.find('temperature_string') is not None else 'Unknown',
            'humidity': root.find('relative_humidity').text if root.find('relative_humidity') is not None else 'Unknown',
            'wind': root.find('wind_string').text if root.find('wind_string') is not None else 'Unknown',
            'observation_time': root.find('observation_time').text if root.find('observation_time') is not None else 'Unknown'
        }
        
        # Return formatted weather data
        xml_response = create_xml_response('success', "Weather data retrieved", {'weather': weather_data})
        return xml_response, 200, {'Content-Type': 'application/xml'}
        
    except Exception as e:
        xml_response = create_error_response(f"Error retrieving weather data: {str(e)}")
        return xml_response, 500, {'Content-Type': 'application/xml'}
