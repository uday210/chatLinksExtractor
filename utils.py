import re
from datetime import datetime
from collections import defaultdict

# Regex patterns for various link types (optimized based on actual usage)
LINK_PATTERNS = [
    r'https://t\.me/\S+',  # Telegram full links (priority)
    r'https?://[^\s]+',  # HTTP/HTTPS links
    r'www\.[^\s]+',  # WWW links
    r't\.me/\S+',  # Short Telegram links
    r'youtu\.be/[^\s]+',  # YouTube short links
    r'youtube\.com/watch[^\s]+',  # YouTube full links
]

# Date patterns for common chat formats
DATE_PATTERNS = [
    r'\[(\d{1,2}/\d{1,2}/\d{2,4}),\s*\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM|am|pm)?\]',  # Telegram format: [DD/MM/YY, HH:MM:SS AM/PM]
    r'\d{1,2}/\d{1,2}/\d{2,4}',  # DD/MM/YYYY or MM/DD/YYYY
    r'\d{1,2}-\d{1,2}-\d{2,4}',  # DD-MM-YYYY
    r'(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{2,4})',  # 12 Jan 2024
]

# Name patterns (common in chats)
NAME_PATTERNS = [
    r'@\w+',  # @username
    r'(?:^|:\s)([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)',  # Names in messages
]


def extract_links(text):
    """Extract all links from text - optimized for Telegram exports"""
    links = []
    for pattern in LINK_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        links.extend(matches)
    
    # Clean up links (remove trailing punctuation and common markers)
    cleaned_links = []
    for link in links:
        # Remove common trailing punctuation
        link = re.sub(r'[,;.\):!"\'<>]+$', '', link)
        # Remove whitespace
        link = link.strip()
        if link and not link.startswith('['):
            cleaned_links.append(link)
    
    return cleaned_links


def extract_names(text):
    """Extract names and usernames from text - optimized for Telegram"""
    names = []
    
    # Extract names from Telegram format: [DD/MM/YY, HH:MM:SS] Name: message
    telegram_names = re.findall(r'^\[\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM|am|pm)?\]\s+([^:]+):', text, re.MULTILINE)
    names.extend(telegram_names)
    
    # Extract @mentions (Telegram style)
    mentions = re.findall(r'@([a-zA-Z0-9_]+)', text, re.IGNORECASE)
    names.extend(mentions)
    
    # Extract names before colons or after "by" (common in chat exports)
    name_from_messages = re.findall(r'^([A-Za-z][A-Za-z\s]+?)(?::|,|\s+has\s+|\s+to\s+)', text, re.MULTILINE)
    names.extend(name_from_messages)
    
    return [name.strip() for name in names if name.strip() and not name.startswith('[')]


def parse_dates(text):
    """Extract dates and associated content from text - optimized for Telegram format"""
    lines = text.split('\n')
    dated_content = defaultdict(list)
    
    current_date = "Unknown"
    
    # Telegram format: [DD/MM/YY, HH:MM:SS AM/PM] Name: message
    telegram_line_pattern = re.compile(r'^\[(\d{1,2}/\d{1,2}/\d{2,4}),\s*\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM|am|pm)?\]')
    
    for line in lines:
        # Try Telegram format first
        telegram_match = telegram_line_pattern.match(line)
        if telegram_match:
            current_date = telegram_match.group(1)
        else:
            # Try other date patterns
            for pattern in DATE_PATTERNS:
                date_match = re.search(pattern, line)
                if date_match:
                    current_date = date_match.group(1) if date_match.lastindex else date_match.group(0)
                    break
        
        # Extract links from this line and associate with current date
        links = extract_links(line)
        if links:
            dated_content[current_date].extend(links)
    
    return dict(dated_content)


def parse_month_year(date_str):
    """Parse date string and return month-year for grouping - handles Telegram format"""
    # Try common date formats (prioritize 2-digit year for Telegram exports)
    formats = [
        '%d/%m/%y', '%m/%d/%y',  # 2-digit year formats
        '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y',  # 4-digit year formats
    ]
    
    # Try to parse known date formats
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.strftime('%B %Y')  # e.g., "January 2024"
        except ValueError:
            continue
    
    # Try to parse month names
    month_names = {
        'jan': 'January', 'feb': 'February', 'mar': 'March', 'apr': 'April',
        'may': 'May', 'jun': 'June', 'jul': 'July', 'aug': 'August',
        'sep': 'September', 'oct': 'October', 'nov': 'November', 'dec': 'December'
    }
    
    for month_abbr, month_full in month_names.items():
        if month_abbr in date_str.lower():
            # Extract year if present
            year_match = re.search(r'\d{4}', date_str)
            if year_match:
                return f"{month_full} {year_match.group(0)}"
            else:
                return month_full
    
    return "Unknown Date"


def group_by_month(dated_links, include_names=False):
    """Group links by month"""
    monthly_data = defaultdict(list)
    
    for date_str, links in dated_links.items():
        month = parse_month_year(date_str)
        for link in links:
            monthly_data[month].append(link)
    
    # Convert to list format for DataFrame
    result = []
    for month in sorted(monthly_data.keys()):
        for link in monthly_data[month]:
            result.append({"Month": month, "Link": link})
    
    return result


def validate_url(url):
    """Check if URL is valid"""
    url_pattern = re.compile(
        r'^https?://' +  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|' +  # domain
        r'localhost|' +  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' +  # IP
        r'(?::\d+)?' +  # port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None
