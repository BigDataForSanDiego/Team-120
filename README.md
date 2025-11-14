#### 
![bigdatahackathon4sd](https://github.com/BigDataForSanDiego/bigdataforsandiego.github.io/blob/main/images/big_data_2025_clip.png?raw=true "Big Data Hackathon for San Diego 2025")

<img height="10%" width="10%" alt="HDMA" src="https://github.com/BigDataForSanDiego/bigdataforsandiego.github.io/blob/main/templates/img/hdma2.png?raw=true"> 
# 2025 BIG DATA HACKATHON PROPOSAL FORM

#### Team Number: `Team 120`  

#### Team Name: `Goodfellow`    

#### Team Coordinator GitHub Username: Robert Ashe - nthPerson

#### Team Members `Robert Ashe 'nthPerson', Suyash Chaudhari 'suyashchaudhari161', Jonathan Siegel 'JSiegel0516', Uma Takbhate 'utakbhate0943-dot'

#### Your team's hackathon idea in One sentence:
Good Fellow is a real-time centralized digital platform(Map UI) that connects homeless individuals with available community resources—like food, shelter, medical care, and activities—while enabling resource centers and individual donors to update inventories, manage profiles, and support training and employment opportunities in addition to providing the resources that individuals experiencing homelessness need.

<img width="50%" src="proposal_drawing.png" alt="Proposal Drawing">


#### Core Theme Addressed by the Goodfellow Resource Locator
- Access to Shelter and Resources
> - Solutions to improve on-demand access and availability of shelters, food banks, medical aid, and social services for homeless individuals.
> - Question: How can we develop technological solutions that provide real-time, on-demand information updates on available shelters, food banks, hygiene stations, medical clinics, and social services for people experiencing homelessness?

### Goodfellow: Helping hands, Finding Hope! 

A Django + GeoDjango web application for locating resources (food banks, shelters, medical services, etc.) for people experiencing homelessness in San Diego County.

## Features

### MVP (v0.1) Functionality

- **Anonymous User Access**: 
  - Interactive map with resource markers
  - Filter by resource type (food, shelter, restroom, medical, legal, donation)
  - Distance-based filtering (1-10 miles)
  - "Open now" filter based on hours of operation
  - Detailed resource information cards
  - No login required for browsing
  - Multi-language support (Spanish translation)

- **Service Provider Portal**:
  - Authenticated submission of new resources
  - Edit own resources (if visible or not_visible)
  - Map-based location picker
  - Resource expiration dates
  - View submission status
  - Sign up page

- **Admin Moderation**:
  - Full CRUD operations on all resources
  - Approve/hide/reject resource submissions
  - GeoDjango admin with map widgets
  - Filter by state and resource type
  - Add rejection reasons

## Tech Stack

- **Backend**: Django 5.0.9 + GeoDjango
- **Database**: PostgreSQL + PostGIS
- **API**: Django REST Framework + django-rest-framework-gis
- **Frontend**: 
  - Leaflet.js (map rendering)
  - Alpine.js (lightweight reactivity)
  - HTMX (dynamic updates)
  - Vanilla CSS (no framework)
- **Deployment**: Gunicorn (production server)

## Project Structure

```
resource_locator_mvp/
├── config/                     # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── resources/                  # Main Django app
│   ├── management/
│   │   └── commands/
│   │       └── seed_resources.py
│   ├── migrations/
│   ├── admin.py               # Django admin configuration
│   ├── forms.py               # Provider submission forms
│   ├── models.py              # Resource model
│   ├── provider_views.py      # Provider dashboard views
│   ├── serializers.py         # DRF serializers
│   ├── urls.py                # URL routing
│   └── views.py               # API viewsets
├── templates/
│   ├── base.html
│   ├── home.html              # Anonymous user map page
│   ├── provider/
│   │   ├── dashboard.html
│   │   ├── resource_form.html
│   │   └── resource_confirm_delete.html
│   └── registration/
│       └── login.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── map.js             # Leaflet map logic
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

Resource markers are color-coded by type:
- Food: Green
- Shelter: Red
- Restroom: Blue
- Medical: Purple
- Legal: Orange
- Donation: Teal
- Other: Gray


For questions about this project, please contact the development team.
